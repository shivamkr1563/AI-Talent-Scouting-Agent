import json
import os
from openai import OpenAI
from .json_utils import extract_json

# Lazy initialization - only create client if API key exists
client = None

def get_client():
    global client
    if client is None:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return None
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.io/api/v1"
        )
    return client

def score_candidates(jd_summary: dict, candidates: list[dict]) -> list[dict]:
    """
    Score candidates based on JD requirements using OpenRouter API.
    Build prompt with all candidates, ask model to return match scores + reasons.
    Return list of {id, match_score, match_reason}
    """
    client = get_client()
    if client is None:
        raise ValueError("OPENROUTER_API_KEY not set")
    
    prompt = f"""Score these candidates against the job description.
    
JD Title: {jd_summary['title']}
Skills Required: {', '.join(jd_summary['top_skills'])}
Experience: {jd_summary['experience']}

Candidates: {json.dumps(candidates)}

Return ONLY valid JSON array with format: [{{id, match_score (0-100), match_reason}}]"""
    
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return extract_json(response.choices[0].message.content)
