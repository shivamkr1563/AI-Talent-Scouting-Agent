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


async def simulate_outreach(candidate: dict, jd_title: str, jd_company: str = "") -> dict:
    """
    Simulate a 3-turn recruiter-candidate conversation with sentiment analysis.
    Falls back to mock data if API fails.
    """
    client = get_client()
    if client is None:
        logger.warning("No API key, using mock outreach")
        return mock_services.simulate_outreach(candidate, jd_title, jd_company)
    
    prompt = f"""You are a thoughtful recruiter. Simulate a 3-turn conversation with a candidate 
evaluating their genuine interest in a role. Be realistic - some candidates are interested, 
some are not, some are lukewarm.

ROLE INFO:
- Title: {jd_title}
- Company: {jd_company or 'A tech company'}

CANDIDATE INFO:
{json.dumps(candidate, indent=2)}

CONVERSATION RULES:
1. Turn 1 (Recruiter): Hook them with compelling role highlights
2. Turn 2 (Candidate): Response based on their profile, interests, and concerns
3. Turn 3 (Recruiter): Address their concerns or close if interested

Be realistic - responses should vary by candidate background:
- Early career: More likely enthusiastic
- Senior/Lead: More discerning, asks about team/growth
- Multiple roles: May be less interested
- Domain mismatch: May politely decline
- Perfect fit: Enthusiastic

Return JSON:
{{
  "conversation": [
    {{"role": "recruiter", "text": "...", "sentiment": "professional"}},
    {{"role": "candidate", "text": "...", "sentiment": "interested|neutral|skeptical|enthusiastic"}},
    {{"role": "recruiter", "text": "...", "sentiment": "professional"}}
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
        
        return mock_services.simulate_outreach(candidate, jd_title, jd_company)
        
    except Exception as e:
        logger.warning(f"Outreach simulation API failed: {e}, using mock")
        return mock_services.simulate_outreach(candidate, jd_title, jd_company)


async def simulate_outreach_batch(candidates: list, jd_title: str, jd_company: str = "") -> list:
    """
    Simulate outreach for multiple candidates concurrently with error handling.
    """
    tasks = [
        simulate_outreach(cand, jd_title, jd_company) 
        for cand in candidates
    ]
    
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
            processed.append(mock_services.simulate_outreach(candidates[i], jd_title, jd_company))
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
