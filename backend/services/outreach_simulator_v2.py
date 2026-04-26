import json
import os
import asyncio
import logging
from openai import AsyncOpenAI
from .json_utils import extract_json
from . import mock_services

logger = logging.getLogger(__name__)


def get_client():
    """Get OpenRouter async client."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return None
    return AsyncOpenAI(
        api_key=api_key,
        base_url="https://openrouter.io/api/v1"
    )


async def simulate_outreach(candidate: dict, jd_title: str, jd_company: str = "", match_score: int = None, gaps: list = None) -> dict:
    """
    Simulate a 3-turn recruiter-candidate conversation with sentiment analysis.
    Falls back to mock data if API fails.
    
    Args:
        candidate: Candidate profile
        jd_title: Job title
        jd_company: Company name
        match_score: Candidate's match score (0-100). If provided, generates realistic responses based on fit.
        gaps: List of skill gaps. If provided, candidate may express concerns about missing skills.
    """
    client = get_client()
    if client is None:
        logger.warning("No API key, using mock outreach")
        return mock_services.simulate_outreach(candidate, jd_title, jd_company, match_score or 75, gaps or [])
    
    # Build match context for the prompt
    match_context = ""
    if match_score is not None:
        match_context = f"""
MATCH QUALITY ANALYSIS:
- Overall Match Score: {match_score}/100
- Match Level: {'Excellent (Perfect fit)' if match_score >= 80 else 'Good (Strong background)' if match_score >= 60 else 'Moderate (Potential with learning)' if match_score >= 40 else 'Low (Significant gaps)'}
- Skill Gaps: {', '.join(gaps) if gaps else 'None identified'}

CRITICAL: Generate responses that reflect this match quality:
- 80-100: Candidate is very enthusiastic, sees perfect fit, asks advanced questions, highly confident
- 60-79: Candidate is interested but may ask clarifying questions about unfamiliar tech
- 40-59: Candidate shows hesitation, explicitly mentions missing skills, asks about training/support
- 0-39: Candidate is cautious, sets realistic expectations, may politely indicate concerns
"""
    
    prompt = f"""You are a thoughtful recruiter. Simulate a 3-turn conversation with a candidate 
evaluating their genuine interest in a role. Be realistic - conversations vary significantly based on skill match.{match_context}

ROLE INFO:
- Title: {jd_title}
- Company: {jd_company or 'A tech company'}

CANDIDATE INFO:
{json.dumps(candidate, indent=2)}

CONVERSATION RULES:
1. Turn 1 (Recruiter): Hook them with compelling role highlights
2. Turn 2 (Candidate): Response based on their profile, match quality, and any skill gaps
3. Turn 3 (Recruiter): Address their concerns or close if interested

IMPORTANT - Make responses UNIQUE and REALISTIC based on skill match:

IF Excellent Match (80-100%):
- Very enthusiastic and confident
- Shows genuine excitement about specific role aspects
- Asks advanced technical questions
- References relevant project experience
- Example: "I'm really excited about this! FastAPI backend work is exactly my strength."

IF Good Match (60-79%):
- Interested with clarifying questions
- May ask about new/unfamiliar technologies
- Shows willingness to learn
- Example: "I'm interested! I have Django experience. Can you tell me more about your FastAPI adoption?"

IF Moderate Match (40-59%):
- Shows hesitation but genuine interest
- Explicitly mentions missing skills/concerns
- Asks about training and support
- Example: "I'm interested, but I notice you need Rust. I don't have that experience. Would training be provided?"

IF Poor Match (0-39%):
- Politely indicates significant concerns
- Sets realistic expectations about ramp-up time
- May express doubt about fit
- Example: "I appreciate the opportunity, but I'm honestly concerned about the WebAssembly requirement..."

Return JSON:
{{
  "conversation": [
    {{"role": "recruiter", "text": "...", "sentiment": "professional"}},
    {{"role": "candidate", "text": "...", "sentiment": "interested|neutral|skeptical|enthusiastic"}},
    {{"role": "recruiter", "text": "...", "sentiment": "professional"}},
    {{"role": "candidate", "text": "...", "sentiment": "interested|neutral|skeptical|enthusiastic"}}
  ],
  "interest_score": <0-100>,
  "likelihood": "high|medium|low",
  "reasoning": ["reason1", "reason2"],
  "positive_signals": ["signal1", "signal2"],
  "concerns": ["concern1", "concern2"],
  "personality_fit": "high|medium|low"
}}

Return ONLY valid JSON. NO markdown."""

    try:
        response = await client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=1500
        )
        
        result = extract_json(response.choices[0].message.content)
        
        # Ensure structure
        if isinstance(result, dict):
            return {
                "conversation": result.get("conversation", []),
                "interest_score": int(result.get("interest_score", 50)),
                "likelihood": result.get("likelihood", "medium"),
                "reasoning": result.get("reasoning", []),
                "positive_signals": result.get("positive_signals", []),
                "concerns": result.get("concerns", []),
                "personality_fit": result.get("personality_fit", "medium")
            }
        
        return mock_services.simulate_outreach(candidate, jd_title, jd_company, match_score or 75, gaps or [])
        
    except Exception as e:
        logger.warning(f"Outreach simulation API failed: {e}, using mock")
        return mock_services.simulate_outreach(candidate, jd_title, jd_company, match_score or 75, gaps or [])


async def simulate_outreach_batch(candidates: list, jd_title: str, jd_company: str = "", scores: list = None) -> list:
    """
    Simulate outreach for multiple candidates concurrently with error handling.
    Uses match scores to generate realistic, varied conversations.
    
    Args:
        candidates: List of candidate profiles
        jd_title: Job title
        jd_company: Company name
        scores: List of match scores with gaps info. Format: [{"id": 1, "match_score": 85, "gaps": [...]}, ...]
    """
    # Build a lookup for quick access to scores
    score_lookup = {}
    if scores:
        for score in scores:
            candidate_id = score.get("id", score.get("candidate_id"))
            score_lookup[candidate_id] = score
    
    # Create tasks with match scores
    tasks = []
    for idx, cand in enumerate(candidates):
        cand_id = cand.get("id", idx + 1)
        score_data = score_lookup.get(cand_id, {})
        match_score = score_data.get("match_score", 75)
        gaps = score_data.get("gaps", [])
        
        tasks.append(
            simulate_outreach(cand, jd_title, jd_company, match_score, gaps)
        )
    
    # Run with concurrency limit
    semaphore = asyncio.Semaphore(3)
    
    async def bounded_task(task):
        async with semaphore:
            return await task
    
    bounded_tasks = [bounded_task(task) for task in tasks]
    results = await asyncio.gather(*bounded_tasks, return_exceptions=True)
    
    # Process results (should be minimal exceptions now due to mock fallback)
    processed = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Outreach failed for candidate {i}: {result}")
            cand_id = candidates[i].get("id", i + 1)
            score_data = score_lookup.get(cand_id, {})
            processed.append(mock_services.simulate_outreach(
                candidates[i], 
                jd_title, 
                jd_company,
                score_data.get("match_score", 75),
                score_data.get("gaps", [])
            ))
        else:
            processed.append(result)
    
    return processed


def calculate_interest_breakdown(outreach_result: dict) -> dict:
    """Convert outreach result to structured breakdown."""
    likelihood_scores = {
        "high": 85,
        "medium": 60,
        "low": 30
    }
    
    adjusted_score = max(
        outreach_result.get("interest_score", 50),
        likelihood_scores.get(outreach_result.get("likelihood", "medium"), 60)
    )
    
    return {
        "initial_engagement": min(100, int(outreach_result.get("interest_score", 50) * 1.2)),
        "opportunity_appeal": min(100, 70 + len(outreach_result.get("positive_signals", [])) * 5),
        "conversation_quality": 75,  # Default quality score
        "overall_interest_score": int(adjusted_score),
        "likelihood": outreach_result.get("likelihood", "medium"),
        "reasoning": outreach_result.get("reasoning", []),
        "positive_signals": outreach_result.get("positive_signals", []),
        "concerns": outreach_result.get("concerns", [])
    }
