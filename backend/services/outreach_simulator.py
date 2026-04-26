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

def simulate_outreach(candidate: dict, jd_title: str) -> dict:
    """
    Prompt OpenRouter to simulate 3-turn recruiter<>candidate conversation.
    Return {conversation: [], interest_score, interest_reason}
    """
    client = get_client()
    if client is None:
        raise ValueError("OPENROUTER_API_KEY not set")
    
    prompt = f"""Simulate a 3-turn recruiter-candidate conversation for:
    
Candidate: {json.dumps(candidate)}
Job Title: {jd_title}

Return ONLY valid JSON: {{conversation: [{{role, text}}...], interest_score (0-100), interest_reason}}"""
    
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return extract_json(response.choices[0].message.content)
