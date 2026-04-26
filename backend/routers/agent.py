from fastapi import APIRouter
from models.schemas import RunAgentRequest, AgentResult
from services import jd_parser, candidate_matcher, outreach_simulator
from services import mock_services
import json
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")

# Check if we should use mock mode
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

@router.post("/run", response_model=AgentResult)
async def run_agent(req: RunAgentRequest):
    try:
        logger.info(f"Request received: {len(req.job_description)} chars (MOCK_MODE: {MOCK_MODE})")
        
        # 1. Parse JD
        logger.info("Step 1: Parsing JD...")
        try:
            parsed = jd_parser.parse_jd(req.job_description)
        except Exception as e:
            logger.warning(f"JD Parser failed, using mock: {e}")
            parsed = mock_services.parse_jd(req.job_description)
        logger.info(f"Step 1 complete: {parsed['title']}")

        # 2. Load mock candidates
        logger.info("Step 2: Loading candidates...")
        file_path = os.path.join(os.path.dirname(__file__), "../data/mock_candidates.json")
        logger.info(f"File path: {file_path}, exists: {os.path.exists(file_path)}")
        with open(file_path) as f:
            candidates = json.load(f)
        logger.info(f"Step 2 complete: {len(candidates)} candidates loaded")

        # 3. Score candidates
        logger.info("Step 3: Scoring candidates...")
        try:
            scores = candidate_matcher.score_candidates(parsed, candidates)
        except Exception as e:
            logger.warning(f"Candidate matcher failed, using mock: {e}")
            scores = mock_services.score_candidates(parsed, candidates)
        logger.info(f"Step 3 complete: {len(scores)} scores")

        # 4. Simulate outreach for each
        logger.info("Step 4: Simulating outreach...")
        results = []
        for i, cand in enumerate(candidates):
            logger.info(f"  Processing candidate {i+1}/{len(candidates)}: {cand['name']}")
            score = next(s for s in scores if s["id"] == cand["id"])
            try:
                outreach = outreach_simulator.simulate_outreach(cand, parsed["title"])
            except Exception as e:
                logger.warning(f"Outreach simulator failed for {cand['name']}, using mock: {e}")
                outreach = mock_services.simulate_outreach(cand, parsed["title"])
            results.append({**cand, **score, **outreach})
        logger.info(f"Step 4 complete: {len(results)} outreaches simulated")

        # 5. Sort by combined score
        logger.info("Step 5: Sorting results...")
        results.sort(key=lambda x: x["match_score"] * 0.5 + x["interest_score"] * 0.5, reverse=True)
        logger.info("Step 5 complete: Results sorted")
        
        response = {"parsed_jd": parsed, "candidates": results}
        logger.info("✅ Request completed successfully")
        return response
        
    except Exception as e:
        logger.error(f"❌ Error in run_agent: {e}", exc_info=True)
        raise
