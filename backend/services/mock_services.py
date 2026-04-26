"""
Mock implementations of AI services for testing/demo purposes.
Simulates the API responses without calling external AI providers.
Returns data in exact format expected by orchestrator.
"""

import json
import random
from typing import Dict, List


def parse_jd(jd_text: str) -> Dict:
    """Mock JD parser - returns realistic sample data matching v2 schema."""
    jd_lower = jd_text.lower()
    
    # Determine seniority and experience from keywords
    if "senior" in jd_lower or "lead" in jd_lower or "principal" in jd_lower or "4+" in jd_lower:
        seniority = "senior"
        experience_years = 4 if "4+" in jd_lower else 5
    elif "junior" in jd_lower or "entry" in jd_lower or "entry-level" in jd_lower:
        seniority = "junior"
        experience_years = 1
    else:
        # Extract experience from "3+" or "3-5" patterns
        seniority = "mid"
        experience_years = 3
        if "3+" in jd_lower or "3 years" in jd_lower:
            experience_years = 3
        elif "5+" in jd_lower or "5 years" in jd_lower:
            experience_years = 5
        elif "2+" in jd_lower or "2 years" in jd_lower:
            experience_years = 2
    
    # Extract job title and domain - check more specific keywords first
    if "backend" in jd_lower or "backend engineer" in jd_lower or "back-end" in jd_lower:
        title = "Backend Engineer"
        domain = "Backend"
        # Extract actual skills mentioned in JD
        if "fastapi" in jd_lower:
            must_have = ["Python", "FastAPI", "PostgreSQL"]
            nice_to_have = ["Docker", "Kubernetes", "AWS"]
            top_skills = ["Python", "FastAPI", "PostgreSQL", "AWS"]
        elif "django" in jd_lower:
            must_have = ["Python", "Django", "PostgreSQL"]
            nice_to_have = ["Docker", "AWS", "Redis"]
            top_skills = ["Python", "Django", "PostgreSQL", "AWS"]
        else:
            must_have = ["Python", "REST APIs", "SQL"]
            nice_to_have = ["Docker", "Kubernetes", "AWS"]
            top_skills = ["Python", "REST APIs", "SQL", "AWS"]
    elif "react" in jd_lower or "frontend" in jd_lower or "front-end" in jd_lower:
        title = "React Developer"
        domain = "Frontend"
        must_have = ["React", "TypeScript", "REST APIs"]
        nice_to_have = ["Tailwind CSS", "Next.js", "Testing"]
        top_skills = ["React", "TypeScript", "REST APIs", "Tailwind CSS"]
    elif "devops" in jd_lower or "dev-ops" in jd_lower:
        title = "DevOps Engineer"
        domain = "DevOps"
        must_have = ["Docker", "Kubernetes", "CI/CD"]
        nice_to_have = ["Terraform", "AWS", "monitoring"]
        top_skills = ["Docker", "Kubernetes", "CI/CD", "AWS"]
    elif "ml" in jd_lower or "machine learning" in jd_lower or "pytorch" in jd_lower or "tensorflow" in jd_lower:
        title = "ML Engineer"
        domain = "ML"
        must_have = ["Python", "PyTorch", "TensorFlow"]
        nice_to_have = ["Deep Learning", "Computer Vision", "NLP"]
        top_skills = ["Python", "PyTorch", "Machine Learning", "TensorFlow"]
    elif "python" in jd_lower:
        # If only Python mentioned without other role indicator, assume backend
        title = "Backend Engineer"
        domain = "Backend"
        must_have = ["Python", "REST APIs", "PostgreSQL"]
        nice_to_have = ["Docker", "AWS", "Kubernetes"]
        top_skills = ["Python", "REST APIs", "PostgreSQL", "AWS"]
    else:
        title = "Software Engineer"
        domain = "Full-stack"
        must_have = ["Python", "JavaScript", "SQL"]
        nice_to_have = ["Docker", "AWS", "Testing"]
        top_skills = ["Python", "JavaScript", "SQL", "Docker"]
    
    # Extract location - check Remote/Bangalore first since they appear together
    location = None
    if "remote" in jd_lower and "bangalore" in jd_lower:
        location = "Remote/Bangalore"
    elif "remote" in jd_lower:
        location = "Remote"
    elif "bangalore" in jd_lower or "bengaluru" in jd_lower:
        location = "Bangalore"
    elif "nyc" in jd_lower or "new york" in jd_lower:
        location = "NYC"
    elif "san francisco" in jd_lower or " sf " in jd_lower or "sf," in jd_lower:
        location = "San Francisco"
    elif "hybrid" in jd_lower:
        location = "Hybrid"
    
    return {
        "title": title,
        "company": "Unspecified",
        "experience_years": experience_years,
        "experience_description": f"{experience_years}+ years of relevant experience",
        "seniority_level": seniority,
        "domain": domain,
        "job_type": "full-time",
        "location": location,
        "must_have_skills": must_have,
        "nice_to_have_skills": nice_to_have,
        "top_skills": top_skills,
        "key_responsibilities": [
            "Design and build scalable systems",
            "Collaborate with cross-functional teams",
            "Mentor junior team members",
            "Contribute to technical architecture"
        ],
        "responsibilities_summary": "Build, maintain, and improve core systems",
        "team_size": "Medium (5-15)",
        "requirements_clarity": "clear",
        "salary_mentioned": False,
        "confidence_score": 0.85
    }


def score_candidates(jd_summary: Dict, candidates: List[Dict]) -> List[Dict]:
    """
    Mock candidate matcher - returns scores in FLAT format expected by orchestrator.
    NOT nested in match_breakdown - orchestrator will build that.
    """
    scores = []
    
    for idx, candidate in enumerate(candidates):
        # Extract experience years from candidate
        exp_str = candidate.get("experience", "0 years")
        try:
            exp_years = int(exp_str.split()[0])
        except:
            exp_years = 0
        
        # Calculate scores based on skill overlap
        candidate_skills = [s.lower() for s in candidate.get("skills", [])]
        jd_must_have = [s.lower() for s in jd_summary.get("must_have_skills", [])]
        jd_nice_to_have = [s.lower() for s in jd_summary.get("nice_to_have_skills", [])]
        
        # Count skill matches
        must_have_matches = sum(1 for skill in jd_must_have if any(skill in cs for cs in candidate_skills))
        nice_have_matches = sum(1 for skill in jd_nice_to_have if any(skill in cs for cs in candidate_skills))
        
        # Calculate individual scores
        skill_match_score = min(100, int((must_have_matches / max(len(jd_must_have), 1)) * 100))
        if nice_have_matches > 0:
            skill_match_score = min(100, skill_match_score + int((nice_have_matches / max(len(jd_nice_to_have), 1)) * 20))
        
        required_exp = jd_summary.get("experience_years", 3)
        experience_alignment = min(100, int((exp_years / max(required_exp, 1)) * 100 + random.randint(5, 20)))
        
        profile_fit = random.randint(70, 95)
        cultural_fit = random.randint(65, 90)
        
        # Calculate overall match score
        match_score = int((skill_match_score * 0.4 + experience_alignment * 0.3 + profile_fit * 0.2 + cultural_fit * 0.1))
        
        # Build reasoning
        reasoning = [
            f"Must-have skills match: {must_have_matches}/{len(jd_must_have)}",
            f"Experience: {exp_years} years vs {required_exp}+ required",
            "Strong technical background",
            "Good team collaboration fit"
        ]
        
        strengths = [
            f"Proficient in {', '.join(candidate.get('skills', [])[:3])}",
            f"{exp_years}+ years of relevant experience",
            "Proven track record in similar roles"
        ]
        
        gaps = []
        if must_have_matches < len(jd_must_have):
            missing = [s for s in jd_must_have if not any(s.lower() in cs for cs in candidate_skills)]
            gaps = [f"Missing expertise in: {', '.join(missing[:2])}"]
        
        # Return in FLAT format (not nested)
        scores.append({
            "id": candidate.get("id", idx + 1),
            "match_score": match_score,
            "skill_match_score": skill_match_score,
            "experience_alignment": experience_alignment,
            "profile_fit": profile_fit,
            "cultural_fit": cultural_fit,
            "reasoning": reasoning,
            "strengths": strengths,
            "gaps": gaps
        })
    
    return sorted(scores, key=lambda x: x["match_score"], reverse=True)


def simulate_outreach(candidate: Dict, jd_title: str, company: str = "") -> Dict:
    """
    Mock outreach simulator - returns conversation and interest data.
    """
    interest_score = random.randint(70, 95)
    likelihood = "high" if interest_score > 80 else "medium" if interest_score > 70 else "low"
    
    return {
        "interest_score": interest_score,
        "likelihood": likelihood,
        "reasoning": [
            "Candidate showed strong interest in role responsibilities",
            "Good alignment with team structure and work style",
            "Available to start within 2 weeks"
        ],
        "positive_signals": [
            "Enthusiastic about the opportunity",
            "Asked detailed technical questions",
            "Interested in growth opportunities",
            "Strong cultural fit indicators"
        ],
        "concerns": [],
        "conversation": [
            {
                "role": "recruiter",
                "text": f"Hi {candidate.get('name')}, we found your profile very interesting for our {jd_title} role. Your experience with {', '.join(candidate.get('skills', [])[:2])} caught our attention. Would you be open to a conversation?",
                "sentiment": "professional"
            },
            {
                "role": "candidate",
                "text": "Thanks for reaching out! I'm very interested in this opportunity. Can you tell me more about the team and key responsibilities?",
                "sentiment": "enthusiastic"
            },
            {
                "role": "recruiter",
                "text": f"Absolutely! We're building scalable systems and looking for someone with your expertise. The team is collaborative and we value continuous learning. What aspects of the role interest you most?",
                "sentiment": "professional"
            },
            {
                "role": "candidate",
                "text": "That sounds great! I'm particularly interested in working on impactful projects with a talented team. I'm available for an interview whenever suits you best.",
                "sentiment": "interested"
            }
        ]
    }
