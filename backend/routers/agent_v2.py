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
            
            # Step 4: Simulate outreach (concurrent)
            logger.info("[AGENT] Simulating outreach conversations...")
            step4_start = time.time()
            outreach_results = await self._simulate_outreach(candidates, parsed_jd)
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
    
    async def _simulate_outreach(self, candidates: list, jd: dict) -> list:
        """Simulate outreach with concurrency."""
        try:
            # Use async batch processing
            results = await outreach_simulator_v2.simulate_outreach_batch(
                candidates,
                jd.get("title", ""),
                jd.get("company", "")
            )
            logger.info(f"Completed outreach for {len(results)} candidates")
            return results
        except Exception as e:
            logger.warning(f"Outreach simulation failed: {e}, using mock")
            results = []
            for cand in candidates:
                results.append(mock_services.simulate_outreach(cand, jd.get("title", ""), jd.get("company", "")))
            return results
    
    def _combine_results(self, candidates: list, scores: list, 
                         outreach: list, jd: dict) -> list:
        """Combine scores and outreach into ranked results."""
        results = []
        
        for i, cand in enumerate(candidates):
            score_data = next((s for s in scores if s.get("id") == cand.get("id")), {})
            outreach_data = outreach[i] if i < len(outreach) else {}
            
            # Build match breakdown
            match_breakdown = ScoringBreakdown(
                skill_match_score=score_data.get("skill_match_score", 0),
                experience_alignment=score_data.get("experience_alignment", 0),
                profile_fit=score_data.get("profile_fit", 0),
                cultural_fit=score_data.get("cultural_fit", 0),
                overall_match_score=score_data.get("match_score", 0),
                reasoning=score_data.get("reasoning", []),
                strengths=score_data.get("strengths", []),
                gaps=score_data.get("gaps", [])
            )
            
            match_score = int(score_data.get("match_score", 50))
            
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
            
            # Calculate combined score
            combined_score = match_score * 0.6 + interest_score * 0.4
            
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
                recommendation=self._get_recommendation(match_score, interest_score)
            )
            results.append(result)
        
        # Sort by combined score
        results.sort(key=lambda x: x.combined_score, reverse=True)
        
        # Set ranks
        for idx, result in enumerate(results):
            result.rank = idx + 1
        
        return results
    
    def _get_recommendation(self, match_score: int, interest_score: int) -> str:
        """Determine recommendation based on scores."""
        avg_score = (match_score + interest_score) / 2
        
        if avg_score >= 80 and interest_score >= 70:
            return "Strong Match"
        elif avg_score >= 70:
            return "Good Fit"
        elif avg_score >= 60:
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
