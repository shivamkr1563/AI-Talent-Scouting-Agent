import json
import os
from openai import OpenAI
from .json_utils import extract_json


def get_client():
    """Get OpenRouter client."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return None
    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.io/api/v1"
    )


def score_candidates(jd_summary: dict, candidates: list[dict]) -> list[dict]:
    """
    Score candidates with detailed reasoning and explainability.
    Returns list of {id, match_score, match_breakdown, interest_context}
    """
    client = get_client()
    if client is None:
        raise ValueError("OPENROUTER_API_KEY not set")
    
    # Build comprehensive prompt with scoring criteria
    prompt = f"""Analyze candidate-to-job fit for a senior recruiter. Score based on MULTIPLE factors.

JOB REQUIREMENTS:
- Title: {jd_summary.get('title', 'Not specified')}
- Required Skills: {', '.join(jd_summary.get('top_skills', []))}
- Experience: {jd_summary.get('experience_years', 'Not specified')} years
- Seniority: {jd_summary.get('seniority_level', 'mid-level')}
- Domain: {jd_summary.get('domain', 'Not specified')}

CANDIDATES TO SCORE:
{json.dumps(candidates, indent=2)}

SCORING CRITERIA (0-100 for each):
1. Skill Match: Do they have required + nice-to-have skills?
2. Experience Alignment: Years & relevant background
3. Profile Fit: Job type, location, overall career trajectory
4. Cultural Fit: Based on background/summary

For each candidate, provide:
{{
  "candidate_id": <id>,
  "match_score": <0-100>,
  "skill_match_score": <0-100>,
  "experience_alignment": <0-100>,
  "profile_fit": <0-100>,
  "cultural_fit": <0-100>,
  "reasoning": ["reason1", "reason2", ...],
  "strengths": ["strength1", "strength2", ...],
  "gaps": ["gap1", "gap2", ...],
  "recommendation": "Strong Match | Good Fit | Potential | Review"
}}

Return ONLY valid JSON array with NO markdown formatting."""

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=3000
    )
    
    result = extract_json(response.choices[0].message.content)
    
    # Ensure each has combined score
    for item in result:
        if isinstance(item, dict):
            if "match_score" not in item:
                item["match_score"] = (
                    item.get("skill_match_score", 0) * 0.4 +
                    item.get("experience_alignment", 0) * 0.3 +
                    item.get("profile_fit", 0) * 0.2 +
                    item.get("cultural_fit", 0) * 0.1
                )
    
    return result if isinstance(result, list) else [result]


def calculate_match_breakdown(scoring_details: dict) -> dict:
    """Convert raw scores to detailed breakdown."""
    return {
        "skill_match_score": int(scoring_details.get("skill_match_score", 0)),
        "experience_alignment": int(scoring_details.get("experience_alignment", 0)),
        "profile_fit": int(scoring_details.get("profile_fit", 0)),
        "cultural_fit": int(scoring_details.get("cultural_fit", 0)),
        "overall_match_score": int(scoring_details.get("match_score", 0)),
        "reasoning": scoring_details.get("reasoning", []),
        "strengths": scoring_details.get("strengths", []),
        "gaps": scoring_details.get("gaps", [])
    }
