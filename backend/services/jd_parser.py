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

def parse_jd(jd_text: str) -> dict:
    """Parse a job description and extract structured information using OpenRouter."""
    client = get_client()
    if client is None:
        raise ValueError("OPENROUTER_API_KEY not set")
    
    prompt = f"""Extract structured info from job descriptions. Return ONLY valid JSON. No markdown.

Schema: {{title, company, top_skills[], experience, domain}}

JD: {jd_text}"""
    
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return extract_json(response.choices[0].message.content)
