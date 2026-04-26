from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.schemas_v2 import (
    RunAgentRequest, AgentResult, ErrorResponse, ExecutionMetrics,
    JDAnalysis, ScoringBreakdown, InterestBreakdown, CandidateResult
)
from services import jd_parser_v2, candidate_matcher_v2, outreach_simulator_v2
from services.database import db
from services import mock_services
import json
import os
import logging
import asyncio
import time
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v2", tags=["talent-scouting"])


class AgentOrchestrator:
    """Orchestrates the entire talent scouting workflow."""
    
    def __init__(self):
        self.start_time = None
        self.metrics = {}
    
    async def run_agent(self, request: RunAgentRequest) -> dict:
        """Execute complete talent scouting workflow."""
        self.start_time = time.time()
        
        try:
            # Step 1: Parse JD
            logger.info(f"[AGENT] Starting workflow for: {request.job_description[:100]}...")
            step1_start = time.time()
            
            parsed_jd = await self._parse_jd(request.job_description)
            self.metrics["jd_parsing_time"] = time.time() - step1_start
            
            # Step 2: Load candidates
            logger.info("[AGENT] Loading candidates...")
            step2_start = time.time()
            candidates = self._load_candidates(request.max_candidates)
            self.metrics["candidate_loading_time"] = time.time() - step2_start
            
            # Step 3: Score candidates
            logger.info(f"[AGENT] Scoring {len(candidates)} candidates...")
            step3_start = time.time()
            scores = await self._score_candidates(parsed_jd, candidates)
            self.metrics["candidate_scoring_time"] = time.time() - step3_start
            
            # Step 4: Simulate outreach (concurrent) - pass scores for realistic conversations
            logger.info("[AGENT] Simulating outreach conversations...")
            step4_start = time.time()
            outreach_results = await self._simulate_outreach(candidates, parsed_jd, scores)
            self.metrics["outreach_time"] = time.time() - step4_start
            
            # Step 5: Combine and rank
            logger.info("[AGENT] Combining results and ranking...")
            candidates_results = self._combine_results(
                candidates, scores, outreach_results, parsed_jd
            )
            
            # Store results
            await self._store_results(parsed_jd, candidates_results)
            
            # Build response
            self.metrics["total_time_seconds"] = time.time() - self.start_time
            self.metrics["candidates_processed"] = len(candidates)
            self.metrics["errors_encountered"] = 0
            
            return {
                "parsed_jd": parsed_jd,
                "candidates": candidates_results,
                "metrics": self.metrics
            }
            
        except Exception as e:
            logger.error(f"[AGENT] Workflow failed: {str(e)}", exc_info=True)
            self.metrics["errors_encountered"] = self.metrics.get("errors_encountered", 0) + 1
            raise
    
    async def _parse_jd(self, jd_text: str) -> dict:
        """Parse job description with error handling."""
        try:
            return jd_parser_v2.parse_jd(jd_text)
        except Exception as e:
            logger.warning(f"JD parser failed: {e}, using mock services")
            return mock_services.parse_jd(jd_text)
    
    def _load_candidates(self, max_count: int = 10) -> List[dict]:
        """Load candidates from database or mock data."""
        try:
            # Try database first
            db_candidates = db.get_all_candidates()
            if db_candidates:
                logger.info(f"Loaded {len(db_candidates)} candidates from database")
                return db_candidates[:max_count]
        except Exception as e:
            logger.warning(f"Database error: {e}")
        
        # Fallback to mock data
        file_path = os.path.join(os.path.dirname(__file__), "../data/mock_candidates.json")
        try:
            with open(file_path) as f:
                candidates = json.load(f)
                logger.info(f"Loaded {len(candidates)} candidates from mock data")
                return candidates[:max_count]
        except Exception as e:
            logger.error(f"Failed to load candidates: {e}")
            return []
    
    async def _score_candidates(self, jd: dict, candidates: list) -> list:
        """Score candidates with explainability."""
        try:
            scores = candidate_matcher_v2.score_candidates(jd, candidates)
            logger.info(f"Scored {len(scores)} candidates")
            return scores
        except Exception as e:
            logger.warning(f"Scoring failed: {e}, using mock")
            return mock_services.score_candidates(jd, candidates)
    
    async def _simulate_outreach(self, candidates: list, jd: dict, scores: list = None) -> list:
        """Simulate outreach with concurrency, using match scores to generate realistic conversations."""
        try:
            # Use async batch processing with scores for realistic conversations
            results = await outreach_simulator_v2.simulate_outreach_batch(
                candidates,
                jd.get("title", ""),
                jd.get("company", ""),
                scores
            )
            logger.info(f"Completed outreach for {len(results)} candidates")
            return results
        except Exception as e:
            logger.warning(f"Outreach simulation failed: {e}, using mock")
            results = []
            for idx, cand in enumerate(candidates):
                # Get match score if available
                score_data = None
                if scores:
                    score_data = next((s for s in scores if s.get("id") == cand.get("id")), None)
                
                match_score = score_data.get("match_score", 75) if score_data else 75
                gaps = score_data.get("gaps", []) if score_data else []
                
                results.append(mock_services.simulate_outreach(
                    cand, 
                    jd.get("title", ""), 
                    jd.get("company", ""),
                    match_score,
                    gaps
                ))
            return results
    
    def _combine_results(self, candidates: list, scores: list, 
                         outreach: list, jd: dict) -> list:
        """Combine scores, role fit, and outreach into ranked results with improved ranking logic."""
        results = []
        
        # Detect job role from JD
        jd_text = jd.get("title", "") + " " + jd.get("domain", "") + " " + " ".join(jd.get("top_skills", []))
        job_role = mock_services.detect_job_role(jd_text, jd.get("top_skills", []))
        logger.info(f"[COMBINE] Detected job role: {job_role}")
        logger.info(f"[COMBINE] Job skills: {jd.get('top_skills', [])}")
        
        for i, cand in enumerate(candidates):
            score_data = next((s for s in scores if s.get("id") == cand.get("id")), {})
            outreach_data = outreach[i] if i < len(outreach) else {}
            candidate_skills = cand.get("skills", [])
            
            # Detect candidate domain
            candidate_domain = mock_services.detect_candidate_domain(candidate_skills)
            
            # Calculate role fit with improved scoring (returns 0-100 score + explanation)
            role_fit_score, role_fit_explanation = mock_services.calculate_role_fit_score(
                job_role, candidate_domain,
                candidate_skills=candidate_skills,
                job_skills=jd.get("top_skills", [])
            )
            
            # Calculate skill match with normalization
            skill_match_score, matched_skills_count, missing_skills = mock_services.calculate_skill_match_score(
                jd.get("top_skills", []), candidate_skills
            )
            
            # Generate ranking explanation
            ranking_explanation = mock_services.generate_ranking_explanation(
                cand, job_role, role_fit_score, role_fit_explanation,
                skill_match_score, missing_skills, 0  # Combined score calculated below
            )
            
            logger.info(f"[COMBINE] {cand.get('name', f'Candidate {i+1}')}: "
                       f"domain={candidate_domain}, role_fit={role_fit_score}/100, "
                       f"skill_match={skill_match_score}/100")
            
            # Build match breakdown with improved role fit
            match_breakdown = ScoringBreakdown(
                skill_match_score=skill_match_score,
                experience_alignment=score_data.get("experience_alignment", 0),
                profile_fit=score_data.get("profile_fit", 0),
                cultural_fit=score_data.get("cultural_fit", 0),
                overall_match_score=score_data.get("match_score", 0),
                role_fit_score=role_fit_score,
                candidate_domain=candidate_domain,
                reasoning=score_data.get("reasoning", []) + [role_fit_explanation] if role_fit_explanation else score_data.get("reasoning", []),
                strengths=score_data.get("strengths", []),
                gaps=score_data.get("gaps", missing_skills)
            )
            
            match_score = int(score_data.get("match_score", skill_match_score))
            skill_match_normalized = skill_match_score / 100.0  # Normalize to 0-1
            role_fit_normalized = role_fit_score / 100.0  # Normalize to 0-1
            
            # Build interest breakdown
            interest_breakdown = InterestBreakdown(
                initial_engagement=min(100, int(outreach_data.get("interest_score", 50) * 1.2)),
                opportunity_appeal=70,
                conversation_quality=75,
                overall_interest_score=int(outreach_data.get("interest_score", 50)),
                likelihood=outreach_data.get("likelihood", "medium"),
                reasoning=outreach_data.get("reasoning", []),
                positive_signals=outreach_data.get("positive_signals", []),
                concerns=outreach_data.get("concerns", [])
            )
            
            interest_score = int(outreach_data.get("interest_score", 50))
            interest_normalized = interest_score / 100.0  # Normalize to 0-1
            
            # ╔════════════════════════════════════════════════════════════════╗
            # ║ IMPROVED RANKING FORMULA: Equal weight to Skill & Role         ║
            # ║ Final Score = (0.4 × Skill Match) +                            ║
            # ║              (0.4 × Role Fit) +                                ║
            # ║              (0.2 × Interest Score)                            ║
            # ║                                                                ║
            # ║ Sort by: 1. Final Score (desc)                                ║
            # ║          2. Role Fit (desc) - tie-breaker                      ║
            # ║          3. Matched Skills (desc) - tie-breaker                ║
            # ╚════════════════════════════════════════════════════════════════╝
            combined_score = (skill_match_normalized * 0.4 + 
                            role_fit_normalized * 0.4 + 
                            interest_normalized * 0.2) * 100
            
            # Build candidate result
            result = CandidateResult(
                id=cand.get("id", i+1),
                name=cand.get("name", f"Candidate {i+1}"),
                title=cand.get("title", ""),
                skills=cand.get("skills", []),
                experience_years=cand.get("experience_years", 0),
                location=cand.get("location"),
                summary=cand.get("summary"),
                match_score=match_score,
                match_breakdown=match_breakdown,
                interest_score=interest_score,
                interest_breakdown=interest_breakdown,
                conversation=outreach_data.get("conversation", []),
                combined_score=combined_score,
                rank=0,  # Will be set after sorting
                recommendation=self._get_recommendation(skill_match_score, interest_score, role_fit_score)
            )
            
            # Store additional metadata for sorting
            result._matched_skills_count = matched_skills_count
            result._role_fit_score = role_fit_score
            
            results.append(result)
        
        # Sort by: 1. combined_score (desc), 2. role_fit (desc), 3. matched_skills (desc)
        results.sort(key=lambda x: (
            x.combined_score,
            x._role_fit_score,
            x._matched_skills_count
        ), reverse=True)
        
        # Set ranks
        for idx, result in enumerate(results):
            result.rank = idx + 1
        
        return results
    
    def _get_recommendation(self, skill_match_score: int, interest_score: int, role_fit_score: int = None) -> str:
        """Determine recommendation based on scores with role fit consideration."""
        if role_fit_score is None:
            role_fit_score = 50  # Default if not provided
        
        # Weighted average: skill (40%) + role fit (40%) + interest (20%)
        avg_score = (skill_match_score * 0.4 + role_fit_score * 0.4 + interest_score * 0.2)
        
        if avg_score >= 80 and role_fit_score >= 75 and interest_score >= 70:
            return "Strong Match"
        elif avg_score >= 70 and role_fit_score >= 60:
            return "Good Fit"
        elif avg_score >= 60 or role_fit_score >= 65:
            return "Potential"
        else:
            return "Review"
    
    async def _store_results(self, jd: dict, candidates: list):
        """Store results in database for analytics."""
        try:
            jd_id = db.save_jd(
                jd.get("title", ""),
                jd.get("company", ""),
                "",  # Full description not stored
                jd
            )
            
            for cand in candidates:
                db.save_scoring_result(
                    jd_id, cand.id,
                    cand.match_score,
                    cand.match_breakdown.dict(),
                    cand.interest_score,
                    cand.interest_breakdown.dict(),
                    [c.dict() for c in cand.conversation] if cand.conversation else []
                )
            
            db.save_agent_run(jd_id, self.metrics.get("total_time_seconds", 0),
                            len(candidates), self.metrics.get("errors_encountered", 0))
            
            logger.info(f"Stored results for {len(candidates)} candidates")
        except Exception as e:
            logger.warning(f"Failed to store results: {e}")


# API Routes
@router.post("/run", response_model=AgentResult)
async def run_agent(request: RunAgentRequest):
    """
    Run complete AI Talent Scouting Agent.
    
    Takes a job description, discovers matching candidates,
    engages them conversationally, and returns ranked shortlist.
    """
    try:
        orchestrator = AgentOrchestrator()
        result = await orchestrator.run_agent(request)
        
        return AgentResult(
            parsed_jd=result["parsed_jd"],
            candidates=result["candidates"],
            metrics=ExecutionMetrics(**result["metrics"])
        )
        
    except Exception as e:
        logger.error(f"Agent execution failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats():
    """Get system statistics."""
    try:
        stats = db.get_stats()
        return {"status": "ok", "stats": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0-production"
    }
