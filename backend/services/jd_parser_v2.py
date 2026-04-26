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


def parse_jd(jd_text: str) -> dict:
    """
    Parse job description and extract detailed, structured information.
    Returns comprehensive parsed JD with explainability.
    """
    client = get_client()
    if client is None:
        raise ValueError("OPENROUTER_API_KEY not set")
    
    prompt = f"""Extract and analyze job description details. Be precise and comprehensive.

JD TEXT:
{jd_text}

Extract and provide structured JSON with:

{{
  "title": "Job title",
  "company": "Company name or 'Not specified'",
  "experience_years": <number>,
  "experience_description": "e.g., 5+ years in backend development",
  "seniority_level": "junior|mid|senior|lead|staff",
  "domain": "Backend|Frontend|Full-stack|ML|Data|DevOps|Mobile|QA",
  "job_type": "full-time|contract|part-time|remote|hybrid",
  "location": "City or 'Remote' or null",
  "must_have_skills": ["skill1", "skill2", ...],
  "nice_to_have_skills": ["skill3", "skill4", ...],
  "top_skills": ["most_important_skill", ...],
  "key_responsibilities": ["Responsibility 1", "Responsibility 2", ...],
  "responsibilities_summary": "Brief summary of main duties",
  "team_size": "Small (1-5)|Medium (5-15)|Large (15+)" or null,
  "requirements_clarity": "clear|moderate|vague",
  "salary_mentioned": true|false,
  "domain_analysis": "Detailed domain classification",
  "confidence_score": 0.9
}}

Be thorough but realistic. If information is missing, set to null or reasonable default.
Return ONLY valid JSON."""

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,  # Low temp for consistency
        max_tokens=1500
    )
    
    parsed = extract_json(response.choices[0].message.content)
    
    # Ensure required fields
    if isinstance(parsed, dict):
        return {
            "title": parsed.get("title", "Not specified"),
            "company": parsed.get("company", "Not specified"),
            "experience_years": parsed.get("experience_years", 3),
            "experience_description": parsed.get("experience_description", ""),
            "seniority_level": parsed.get("seniority_level", "mid"),
            "domain": parsed.get("domain", "Full-stack"),
            "job_type": parsed.get("job_type", "full-time"),
            "location": parsed.get("location"),
            "must_have_skills": parsed.get("must_have_skills", parsed.get("top_skills", [])),
            "nice_to_have_skills": parsed.get("nice_to_have_skills", []),
            "top_skills": parsed.get("top_skills", parsed.get("must_have_skills", [])),
            "key_responsibilities": parsed.get("key_responsibilities", []),
            "responsibilities_summary": parsed.get("responsibilities_summary", ""),
            "confidence_score": float(parsed.get("confidence_score", 0.8))
        }
    
    raise ValueError("Failed to parse JD")


def analyze_jd_requirements(parsed_jd: dict) -> dict:
    """Analyze parsed JD to create candidate matching profile."""
    return {
        "required_experience_range": (
            parsed_jd.get("experience_years", 3),
            parsed_jd.get("experience_years", 3) + 2
        ),
        "required_seniority": parsed_jd.get("seniority_level", "mid"),
        "must_have_skills": parsed_jd.get("must_have_skills", []),
        "nice_to_have_skills": parsed_jd.get("nice_to_have_skills", []),
        "domain_focus": parsed_jd.get("domain", "Full-stack"),
        "team_environment": f"Role focuses on {parsed_jd.get('domain', 'general')} work",
        "flexibility": {
            "location": "remote" in str(parsed_jd.get("job_type", "")).lower(),
            "contract_based": "contract" in str(parsed_jd.get("job_type", "")).lower(),
        }
    }
