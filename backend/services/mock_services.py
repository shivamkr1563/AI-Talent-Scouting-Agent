"""
Mock implementations of AI services for testing/demo purposes.
Simulates the API responses without calling external AI providers.
Returns data in exact format expected by orchestrator.
"""

import json
import random
import re
from typing import Dict, List


# Comprehensive skill database with different categories
KNOWN_SKILLS = {
    # Languages
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust", "Ruby", "PHP",
    "Kotlin", "Swift", "Objective-C", "Scala", "Haskell", "Elixir", "Clojure",
    
    # Frontend
    "React", "Vue", "Angular", "Next.js", "Svelte", "Ember", "Vite", "Webpack",
    "TypeScript", "HTML5", "CSS3", "SASS", "Tailwind", "Tailwind CSS", "Bootstrap",
    "Material UI", "React Testing Library", "Jest", "Cypress",
    
    # Backend
    "FastAPI", "Django", "Flask", "Spring", "Express", "Nest.js", "Laravel", "Rails",
    "Node.js", "ASP.NET", "Fastify", "Gin", "Echo",
    
    # Databases
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "DynamoDB", "Cassandra", "Elasticsearch",
    "Oracle", "SQL Server", "SQLite", "Firebase", "CosmosDB", "Neo4j",
    
    # Cloud & DevOps
    "AWS", "GCP", "Azure", "Kubernetes", "Docker", "CI/CD", "Terraform", "CloudFormation",
    "Ansible", "Jenkins", "GitLab CI", "GitHub Actions", "Prometheus", "Grafana",
    "ECS", "Lambda", "EC2", "S3", "RDS",
    
    # Data & ML
    "Machine Learning", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy",
    "Computer Vision", "NLP", "Deep Learning", "LLM", "RAG", "RLHF",
    "Spark", "Hadoop", "Kafka", "RabbitMQ", "Apache Spark",
    
    # Specialized Technologies
    "WebAssembly", "WASM", "Blockchain", "Solidity", "Ethereum",
    "GraphQL", "REST APIs", "gRPC", "SOAP", "Microservices",
    
    # Tools & Other
    "Git", "Docker", "Linux", "AWS", "Agile", "Scrum", "System Design",
    "API Design", "Database Design", "Testing", "Monitoring", "DevOps",
    "Data Engineering", "Data Science", "Architecture", "Design Patterns"
}

# Rare/specialized skills that indicate non-standard roles
SPECIALIZED_SKILLS = {
    "Rust", "WebAssembly", "WASM", "Blockchain", "Solidity", "Ethereum",
    "COBOL", "Fortran", "LISP", "Erlang", "Haskell"
}


def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract ONLY skills that are explicitly mentioned in the text.
    Do NOT use defaults.
    """
    text_lower = text.lower()
    found_skills = []
    
    # Check each known skill case-insensitively
    for skill in KNOWN_SKILLS:
        skill_lower = skill.lower()
        # Use word boundaries to avoid partial matches
        # E.g., "Rust" shouldn't match "rustic"
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)
    
    return found_skills


def detect_job_role(jd_text: str, found_skills: List[str] = None) -> str:
    """
    Dynamically detect job role from JD text and skills.
    
    Returns: 'frontend', 'backend', 'ml', 'devops', 'data', 'fullstack', or 'unknown'
    
    Rules:
    - If BOTH frontend AND backend keywords/skills → 'fullstack'
    - If only frontend → 'frontend'
    - If only backend → 'backend'
    - If ML/Data/DevOps → respective role
    """
    if found_skills is None:
        found_skills = []
    
    jd_lower = jd_text.lower()
    found_skills_lower = [s.lower() for s in found_skills]
    
    # Define keyword sets
    frontend_keywords = {"frontend", "react", "vue", "angular", "typescript", "tailwind", "next.js", "css", "html"}
    backend_keywords = {"backend", "fastapi", "django", "flask", "spring", "express", "node.js", "python", "java", "rest api", "api"}
    ml_keywords = {"machine learning", "ai", "nlp", "ml engineer", "tensorflow", "pytorch"}
    devops_keywords = {"devops", "infrastructure", "sre", "kubernetes", "docker", "ci/cd"}
    data_keywords = {"data engineer", "data pipeline", "spark", "hadoop", "kafka"}
    
    # Define skill sets
    frontend_skills = {"react", "vue", "angular", "next.js", "html5", "css3", "typescript", "jest", "cypress", "tailwind"}
    backend_skills = {"fastapi", "django", "flask", "spring", "express", "node.js", "postgresql", "mysql", "java", "python"}
    ml_skills = {"machine learning", "tensorflow", "pytorch", "scikit-learn", "pandas", "nlp", "deep learning"}
    devops_skills = {"kubernetes", "docker", "ci/cd", "terraform", "ansible", "github actions"}
    data_skills = {"spark", "hadoop", "kafka", "data engineering", "apache spark"}
    
    # Count matches for each domain
    frontend_keywords_match = sum(1 for kw in frontend_keywords if kw in jd_lower)
    backend_keywords_match = sum(1 for kw in backend_keywords if kw in jd_lower)
    ml_keywords_match = sum(1 for kw in ml_keywords if kw in jd_lower)
    devops_keywords_match = sum(1 for kw in devops_keywords if kw in jd_lower)
    data_keywords_match = sum(1 for kw in data_keywords if kw in jd_lower)
    
    skill_set_lower = set(found_skills_lower)
    frontend_skills_match = len(skill_set_lower & frontend_skills)
    backend_skills_match = len(skill_set_lower & backend_skills)
    
    # Check for FULL-STACK (BOTH frontend AND backend present)
    has_frontend = frontend_keywords_match > 0 or frontend_skills_match > 0
    has_backend = backend_keywords_match > 0 or backend_skills_match > 0
    
    if has_frontend and has_backend:
        return "fullstack"
    elif has_frontend:
        return "frontend"
    elif has_backend:
        return "backend"
    elif ml_keywords_match > 0 or len(skill_set_lower & ml_skills) > 0:
        return "ml"
    elif devops_keywords_match > 0 or len(skill_set_lower & devops_skills) > 0:
        return "devops"
    elif data_keywords_match > 0 or len(skill_set_lower & data_skills) > 0:
        return "data"
    else:
        return "unknown"


def detect_candidate_domain(candidate_skills: List[str]) -> str:
    """
    Detect candidate's primary domain/role from their skills.
    Returns: 'frontend', 'backend', 'ml', 'devops', 'data', 'fullstack', or 'unknown'
    """
    skills_lower = [s.lower() for s in candidate_skills]
    skill_set = set(skills_lower)
    
    frontend_skills = {"react", "vue", "angular", "next.js", "html5", "css3", "typescript", "jest", "cypress"}
    backend_skills = {"fastapi", "django", "flask", "spring", "express", "node.js", "postgresql", "mysql"}
    ml_skills = {"machine learning", "tensorflow", "pytorch", "scikit-learn", "pandas", "nlp", "deep learning"}
    devops_skills = {"kubernetes", "docker", "ci/cd", "terraform", "ansible", "github actions", "gitlab ci"}
    data_skills = {"spark", "hadoop", "kafka", "data engineering", "apache spark"}
    
    # Count skill matches per domain
    frontend_count = len(skill_set & frontend_skills)
    backend_count = len(skill_set & backend_skills)
    ml_count = len(skill_set & ml_skills)
    devops_count = len(skill_set & devops_skills)
    data_count = len(skill_set & data_skills)
    
    # Return domain with most skill matches
    domain_scores = {
        "frontend": frontend_count,
        "backend": backend_count,
        "ml": ml_count,
        "devops": devops_count,
        "data": data_count,
    }
    
    max_domain = max(domain_scores, key=domain_scores.get)
    if domain_scores[max_domain] > 0:
        return max_domain
    else:
        return "fullstack"


def normalize_skill_name(skill: str) -> str:
    """Normalize skill names for consistent matching."""
    # Keyword mapping for skill aliases
    skill_mapping = {
        "rest api": "rest apis",
        "apis": "rest apis",
        "rest": "rest apis",
        "ml": "machine learning",
        "machine learning": "machine learning",
        "nlp": "nlp",
        "transformers": "nlp",
        "bert": "nlp",
        "ts": "typescript",
        "js": "javascript",
        "py": "python",
        "node": "node.js",
        "react.js": "react",
        "nextjs": "next.js",
        "fastapi": "fastapi",
        "tf": "tensorflow",
        "pytorch": "pytorch",
        "aws": "aws",
        "gcp": "gcp",
        "azure": "azure",
        "k8s": "kubernetes",
        "k8": "kubernetes",
        "db": "database",
        "sql": "sql",
        "nosql": "nosql",
        "devops": "devops",
        "cicd": "ci/cd",
        "ci/cd": "ci/cd",
    }
    
    normalized = skill.lower().strip()
    return skill_mapping.get(normalized, normalized)


def calculate_skill_match_score(job_skills: List[str], candidate_skills: List[str]) -> tuple:
    """
    Calculate skill match score with normalization and keyword mapping.
    
    Returns: (skill_match_score, matched_skills_count, missing_skills)
    """
    # Normalize all skills
    job_skills_normalized = set(normalize_skill_name(s) for s in job_skills)
    candidate_skills_normalized = set(normalize_skill_name(s) for s in candidate_skills)
    
    # Calculate matches
    matched_skills = job_skills_normalized & candidate_skills_normalized
    missing_skills = job_skills_normalized - candidate_skills_normalized
    
    # Score calculation
    if not job_skills_normalized:
        return 100, 0, []
    
    match_percentage = (len(matched_skills) / len(job_skills_normalized)) * 100
    score = min(100, int(match_percentage))
    
    return score, len(matched_skills), list(missing_skills)


def generate_ranking_explanation(candidate: dict, job_role: str, 
                                role_fit_score: int, role_fit_explanation: str,
                                skill_match_score: int, missing_skills: List[str],
                                combined_score: float) -> str:
    """
    Generate detailed explanation for why candidate is ranked.
    """
    name = candidate.get("name", "Candidate")
    candidate_domain = detect_candidate_domain(candidate.get("skills", []))
    
    explanation = f"{name} ({candidate_domain.title()}) - Final Score: {combined_score:.1f}/100\n"
    explanation += f"  Role Alignment: {role_fit_explanation} ({role_fit_score}/100)\n"
    explanation += f"  Skill Match: {skill_match_score}/100"
    
    if missing_skills:
        explanation += f"\n  Missing Skills: {', '.join(missing_skills[:3])}"
        if len(missing_skills) > 3:
            explanation += f" (+{len(missing_skills) - 3} more)"
    
    return explanation


def calculate_role_fit_score(job_role: str, candidate_domain: str, 
                             candidate_skills: List[str] = None,
                             job_skills: List[str] = None) -> tuple:
    """
    Calculate role fit score (0-100) based on job role and candidate domain/skills.
    
    Returns: (role_fit_score, explanation)
    
    Rules:
    
    FULL-STACK JOB:
    - Candidate has both frontend + backend skills → 85-95
    - Candidate has one side strong, partial other → 60-80
    - Candidate has only one side → 40-60
    - Candidate has neither → <40
    
    BACKEND JOB:
    - Candidate is backend specialist → 90-100
    - Candidate is full-stack → 75-85
    - Candidate has some backend → 50-75
    - Candidate is frontend/other → <40
    
    FRONTEND JOB:
    - Candidate is frontend specialist → 90-100
    - Candidate is full-stack → 75-85
    - Candidate has some frontend → 50-75
    - Candidate is backend/other → <40
    """
    if candidate_skills is None:
        candidate_skills = []
    if job_skills is None:
        job_skills = []
    
    candidate_skills_lower = set(s.lower() for s in candidate_skills)
    job_skills_lower = set(s.lower() for s in job_skills)
    
    # Skill categories
    frontend_skills = {"react", "vue", "angular", "next.js", "html5", "css3", "typescript", "jest", "cypress", "tailwind"}
    backend_skills = {"fastapi", "django", "flask", "spring", "express", "node.js", "postgresql", "mysql", "java", "python"}
    
    candidate_frontend_count = len(candidate_skills_lower & frontend_skills)
    candidate_backend_count = len(candidate_skills_lower & backend_skills)
    job_frontend_count = len(job_skills_lower & frontend_skills)
    job_backend_count = len(job_skills_lower & backend_skills)
    
    # Determine candidate's actual profile
    has_frontend = candidate_frontend_count > 0
    has_backend = candidate_backend_count > 0
    candidate_is_fullstack = has_frontend and has_backend
    
    if job_role == "fullstack":
        # FULL-STACK JOB
        if candidate_is_fullstack:
            # Both skills present
            score = min(95, 85 + (candidate_frontend_count + candidate_backend_count) * 2)
            explanation = f"Full-stack candidate with {candidate_frontend_count} frontend + {candidate_backend_count} backend skills"
        elif has_frontend or has_backend:
            # Only one side
            if candidate_frontend_count > candidate_backend_count:
                score = min(75, 50 + candidate_frontend_count * 5)
                explanation = f"Frontend specialist ({candidate_frontend_count} skills) - needs backend skills"
            else:
                score = min(75, 50 + candidate_backend_count * 5)
                explanation = f"Backend specialist ({candidate_backend_count} skills) - needs frontend skills"
        else:
            score = 20
            explanation = "No relevant frontend or backend skills for full-stack role"
    
    elif job_role == "backend":
        # BACKEND JOB
        if candidate_domain == "backend":
            score = min(100, 90 + candidate_backend_count)
            explanation = f"Backend specialist with {candidate_backend_count} backend skills - perfect match"
        elif candidate_is_fullstack:
            score = min(85, 75 + candidate_backend_count * 2)
            explanation = f"Full-stack developer with {candidate_backend_count} backend skills - good fit"
        elif has_backend:
            score = min(75, 50 + candidate_backend_count * 5)
            explanation = f"Partial backend experience ({candidate_backend_count} skills) - may need ramp-up"
        else:
            score = 20
            explanation = "No backend skills - significant mismatch"
    
    elif job_role == "frontend":
        # FRONTEND JOB
        if candidate_domain == "frontend":
            score = min(100, 90 + candidate_frontend_count)
            explanation = f"Frontend specialist with {candidate_frontend_count} frontend skills - perfect match"
        elif candidate_is_fullstack:
            score = min(85, 75 + candidate_frontend_count * 2)
            explanation = f"Full-stack developer with {candidate_frontend_count} frontend skills - good fit"
        elif has_frontend:
            score = min(75, 50 + candidate_frontend_count * 5)
            explanation = f"Partial frontend experience ({candidate_frontend_count} skills) - may need ramp-up"
        else:
            score = 20
            explanation = "No frontend skills - significant mismatch"
    
    elif job_role == candidate_domain:
        # Perfect domain match
        score = 95
        explanation = f"Domain match: {job_role} specialist"
    
    else:
        # Different roles
        related_roles = {
            "backend": {"fullstack", "data"},
            "frontend": {"fullstack"},
            "ml": {"data", "backend"},
            "devops": {"backend", "data"},
            "data": {"ml", "devops"},
        }
        
        if candidate_domain in related_roles.get(job_role, set()):
            score = 65
            explanation = f"Related role: {candidate_domain} → {job_role}"
        else:
            score = 30
            explanation = f"Different domain: {candidate_domain} vs {job_role}"
    
    return int(score), explanation


def detect_domain_and_title(jd_text: str, found_skills: List[str]) -> tuple:
    """
    Detect role domain and title based on actual content, not defaults.
    Returns (title, domain, is_specialized)
    """
    jd_lower = jd_text.lower()
    found_skills_lower = [s.lower() for s in found_skills]
    
    # Check for specialized roles FIRST
    if "rust" in found_skills_lower and "webassembly" in found_skills_lower:
        return ("Rust Backend Engineer", "Specialized Backend", True)
    elif "rust" in found_skills_lower:
        return ("Rust Engineer", "Systems Programming", True)
    elif "blockchain" in found_skills_lower or "solidity" in found_skills_lower:
        return ("Blockchain Developer", "Blockchain", True)
    
    # Standard role detection
    if "backend" in jd_lower or "fastapi" in found_skills_lower or "django" in found_skills_lower:
        return ("Backend Engineer", "Backend", False)
    elif "react" in found_skills_lower or "frontend" in jd_lower or "vue" in found_skills_lower:
        return ("Frontend Developer", "Frontend", False)
    elif "devops" in jd_lower or "kubernetes" in found_skills_lower or "docker" in found_skills_lower:
        return ("DevOps Engineer", "DevOps", False)
    elif "machine learning" in jd_lower or "pytorch" in found_skills_lower or "tensorflow" in found_skills_lower:
        return ("ML Engineer", "ML", False)
    elif "data engineer" in jd_lower or "spark" in found_skills_lower or "kafka" in found_skills_lower:
        return ("Data Engineer", "Data Engineering", False)
    else:
        return ("Software Engineer", "Full-Stack", False)


def parse_jd(jd_text: str) -> Dict:
    """
    Fixed JD parser - extracts ONLY skills mentioned in text.
    Does NOT use default fallback skills.
    Marks specialized roles appropriately.
    """
    jd_lower = jd_text.lower()
    
    # Extract all skills mentioned in the JD
    extracted_skills = extract_skills_from_text(jd_text)
    
    # Separate must-have and nice-to-have
    # "must have" or "required" → must_have_skills
    # "nice to have" or "preferred" → nice_to_have_skills
    must_have = []
    nice_to_have = []
    
    # Simple heuristic: skills before "nice to have" are must-have
    if "nice to have" in jd_lower or "nice-to-have" in jd_lower or "preferred" in jd_lower:
        nice_to_have_idx = max(
            jd_lower.find("nice to have"),
            jd_lower.find("nice-to-have"),
            jd_lower.find("preferred")
        )
        jd_upper_half = jd_text[:nice_to_have_idx]
        jd_lower_half = jd_text[nice_to_have_idx:]
        
        must_have = extract_skills_from_text(jd_upper_half)
        nice_to_have = extract_skills_from_text(jd_lower_half)
    else:
        # If no "nice to have" section, all extracted skills are must-have
        must_have = extracted_skills
        nice_to_have = []
    
    # If NO skills were extracted, return minimal parsing
    if not must_have and not extracted_skills:
        title, domain, is_specialized = detect_domain_and_title(jd_text, [])
        return {
            "title": title,
            "company": "Unspecified",
            "experience_years": 3,
            "experience_description": "3+ years of relevant experience",
            "seniority_level": "mid",
            "domain": domain,
            "job_type": "full-time",
            "location": None,
            "must_have_skills": [],
            "nice_to_have_skills": [],
            "top_skills": [],
            "key_responsibilities": ["Build scalable systems", "Collaborate with teams"],
            "responsibilities_summary": "Unknown specialized role",
            "team_size": "Unknown",
            "requirements_clarity": "unclear",
            "salary_mentioned": False,
            "is_specialized_role": is_specialized,
            "confidence_score": 0.5
        }
    
    # Detect title and domain based on actual extracted skills
    title, domain, is_specialized = detect_domain_and_title(jd_text, must_have or nice_to_have)
    # Determine seniority and experience from keywords
    if "senior" in jd_lower or "lead" in jd_lower or "principal" in jd_lower:
        seniority = "senior"
        experience_years = 5
        if "4+" in jd_lower:
            experience_years = 4
        elif "5+" in jd_lower:
            experience_years = 5
        elif "6+" in jd_lower:
            experience_years = 6
    elif "junior" in jd_lower or "entry" in jd_lower:
        seniority = "junior"
        experience_years = 1
    else:
        seniority = "mid"
        experience_years = 3
        if "2+" in jd_lower or "2 years" in jd_lower:
            experience_years = 2
        elif "3+" in jd_lower or "3 years" in jd_lower:
            experience_years = 3
        elif "5+" in jd_lower or "5 years" in jd_lower:
            experience_years = 5
    
    # Extract location
    location = None
    if "remote" in jd_lower and "bangalore" in jd_lower:
        location = "Remote/Bangalore"
    elif "remote" in jd_lower:
        location = "Remote"
    elif "bangalore" in jd_lower or "bengaluru" in jd_lower:
        location = "Bangalore"
    elif "nyc" in jd_lower or "new york" in jd_lower:
        location = "NYC"
    elif "san francisco" in jd_lower or " sf " in jd_lower:
        location = "San Francisco"
    elif "hybrid" in jd_lower:
        location = "Hybrid"
    
    # Build top_skills (combination of must and nice-to-have)
    top_skills = must_have + nice_to_have
    
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
        "requirements_clarity": "clear" if extracted_skills else "unclear",
        "salary_mentioned": False,
        "is_specialized_role": is_specialized,
        "confidence_score": 0.85 if extracted_skills else 0.5
    }


def score_candidates(jd_summary: Dict, candidates: List[Dict]) -> List[Dict]:
    """
    Mock candidate matcher - returns scores in FLAT format expected by orchestrator.
    Handles specialized roles with significant score reductions for mismatches.
    
    Key logic for specialized roles:
    1. If skill_match < 30%, cap final score below 50
    2. If ALL candidates have skill_match < 30%, mark as "No suitable candidates"
    3. Heavy penalty for missing critical/specialized skills
    """
    scores = []
    is_specialized = jd_summary.get("is_specialized_role", False)
    jd_must_have = [s.lower() for s in jd_summary.get("must_have_skills", [])]
    jd_nice_to_have = [s.lower() for s in jd_summary.get("nice_to_have_skills", [])]
    specialized_skills_in_jd = [s for s in jd_must_have if any(tech.lower() in s for tech in SPECIALIZED_SKILLS)]
    
    # First pass: calculate all scores
    for idx, candidate in enumerate(candidates):
        # Extract experience years from candidate
        exp_str = candidate.get("experience", "0 years")
        try:
            exp_years = int(exp_str.split()[0])
        except:
            exp_years = 0
        
        # Get candidate skills in lowercase
        candidate_skills = [s.lower() for s in candidate.get("skills", [])]
        
        # Count skill matches
        must_have_matches = sum(1 for skill in jd_must_have if any(skill in cs for cs in candidate_skills))
        nice_have_matches = sum(1 for skill in jd_nice_to_have if any(skill in cs for cs in candidate_skills))
        
        # Calculate core skill match percentage
        if jd_must_have:
            core_skill_match_percent = (must_have_matches / len(jd_must_have)) * 100
        else:
            core_skill_match_percent = 50
        
        # Calculate individual scores
        skill_match_score = min(100, int(core_skill_match_percent))
        if nice_have_matches > 0 and jd_nice_to_have:
            skill_match_score = min(100, skill_match_score + int((nice_have_matches / max(len(jd_nice_to_have), 1)) * 20))
        
        # FOR SPECIALIZED ROLES: Severe penalty if candidate lacks specialized skills
        has_specialized_skills = False
        if is_specialized and specialized_skills_in_jd:
            has_specialized_skills = any(any(tech.lower() in cs for tech in SPECIALIZED_SKILLS) for cs in candidate_skills)
            if not has_specialized_skills:
                # Massive penalty for lacking specialized skills: reduce to 30% of calculated score
                skill_match_score = max(5, int(skill_match_score * 0.3))
        
        required_exp = jd_summary.get("experience_years", 3)
        experience_alignment = min(100, int((exp_years / max(required_exp, 1)) * 100 + random.randint(5, 20)))
        
        profile_fit = random.randint(70, 95)
        cultural_fit = random.randint(65, 90)
        
        # Calculate overall match score
        match_score = int((skill_match_score * 0.4 + experience_alignment * 0.3 + profile_fit * 0.2 + cultural_fit * 0.1))
        
        # RULE 1: If core skill match < 30%, cap final score below 50
        if skill_match_score < 30:
            match_score = min(49, match_score)
        
        # Build reasoning
        reasoning = [
            f"Must-have skills match: {must_have_matches}/{len(jd_must_have)}" if jd_must_have else "No standard skills specified",
            f"Experience: {exp_years} years vs {required_exp}+ required",
        ]
        
        # Add specialized role feedback
        if is_specialized and specialized_skills_in_jd:
            if not has_specialized_skills:
                reasoning.append(f"Lacks specialized technology: {', '.join(specialized_skills_in_jd)}")
                reasoning.append("This is a highly specialized role requiring niche expertise")
            else:
                reasoning.append("Has required specialized technology expertise")
        
        strengths = [
            f"Proficient in {', '.join(candidate.get('skills', [])[:3])}" if candidate.get('skills') else "Skills profile available",
            f"{exp_years}+ years of relevant experience",
            "Proven track record in similar roles"
        ]
        
        gaps = []
        if jd_must_have and must_have_matches < len(jd_must_have):
            missing = [s for s in jd_must_have if not any(s in cs for cs in candidate_skills)]
            gaps = [f"Missing expertise in: {', '.join(missing[:2])}"]
        
        if is_specialized and specialized_skills_in_jd:
            if not has_specialized_skills:
                gaps.append(f"No experience with specialized tech: {', '.join(specialized_skills_in_jd)}")
        
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
            "gaps": gaps,
            "core_skill_match_percent": core_skill_match_percent
        })
    
    # Sort by match score
    scores = sorted(scores, key=lambda x: x["match_score"], reverse=True)
    
    # RULE 2: If ALL candidates have skill_match < 30%, add system-level warning
    all_low_skill_match = all(score['skill_match_score'] < 30 for score in scores)
    if all_low_skill_match and is_specialized:
        # Add a flag to the first candidate's reasoning (will be handled by orchestrator)
        if scores:
            scores[0]['system_warning'] = "Role too specialized for current candidate pool"
            scores[0]['all_candidates_unsuitable'] = True
    
    return scores


def simulate_outreach(candidate: Dict, jd_title: str, company: str = "", match_score: int = 75, gaps: List[str] = None) -> Dict:
    """
    Mock outreach simulator - generates realistic conversations based on skill match.
    
    Args:
        candidate: Candidate profile with name, skills, experience
        jd_title: Job title being discussed
        company: Company name
        match_score: Candidate's match score (0-100)
        gaps: List of missing skills/gaps
    
    Returns:
        Conversation and interest data - VARIED based on match quality
    """
    if gaps is None:
        gaps = []
    
    candidate_name = candidate.get('name', 'Candidate')
    candidate_skills = candidate.get('skills', [])[:2]
    candidate_exp = candidate.get('experience', '0 years')
    
    # Determine match quality and response tone
    if match_score >= 80:
        # EXCELLENT MATCH - Enthusiastic, confident, excited
        interest_score = random.randint(85, 95)
        likelihood = "high"
        
        opening_response = f"Thanks for reaching out! I'm really excited about this opportunity. {jd_title} is exactly the kind of role I've been looking for!"
        mid_response = f"Absolutely! I'm particularly interested in working on {['mission-critical projects', 'scalable systems', 'challenging technical problems'][random.randint(0,2)]}. The focus on {['continuous learning', 'technical excellence', 'team collaboration'][random.randint(0,2)]} really appeals to me."
        final_response = f"This sounds like a perfect fit for me. I'm very interested in moving forward. I'm available for an interview at your earliest convenience."
        
        positive_signals = [
            "Highly enthusiastic about the role",
            "Strong technical alignment with requirements",
            "Immediately sees how skills transfer to role",
            "Asks advanced technical questions",
            "References specific project interests",
            "Confident about ability to contribute immediately"
        ]
        concerns = []
        
    elif match_score >= 60:
        # GOOD MATCH - Interested, some clarifying questions
        interest_score = random.randint(72, 85)
        likelihood = "high" if match_score >= 70 else "medium"
        
        opening_response = f"Thanks for reaching out! I'm interested in learning more about this {jd_title} role."
        
        if gaps:
            # Has some gaps but intrigued
            mid_response = f"The role sounds interesting, and I have solid experience with {', '.join(candidate_skills)}. I noticed the role also requires {gaps[0].split('Missing expertise in: ')[1] if 'Missing' in gaps[0] else 'some additional skills'}. Can you tell me more about how critical those are?"
            final_response = "I'd be interested in discussing how my background could work for this role. I learn quickly and have picked up new technologies before."
        else:
            # Good match, very interested
            mid_response = f"Great! I have experience with {', '.join(candidate_skills)} and have worked on similar projects. I'm particularly interested in learning more about your tech stack and team."
            final_response = "This sounds like a really good opportunity. I'd be happy to move forward with an interview."
        
        positive_signals = [
            "Interested in role growth potential",
            "Relevant experience and skills",
            "Shows willingness to learn",
            "Asks clarifying questions about requirements"
        ]
        
        if gaps:
            concerns = [
                f"Needs to develop expertise in: {gaps[0].split('Missing expertise in: ')[1] if 'Missing' in gaps[0] else 'specialized areas'}",
                "May require onboarding time for unfamiliar technologies"
            ]
        else:
            concerns = []
        
    else:
        # POOR MATCH - Hesitant, concerned about fit, asks about training
        interest_score = random.randint(45, 65)
        likelihood = "medium" if interest_score > 55 else "low"
        
        opening_response = f"Thanks for thinking of me. I'm somewhat interested, but I want to be honest about my background."
        
        missing_tech = gaps[0].split('Missing expertise in: ')[1] if gaps and 'Missing' in gaps[0] else 'some key requirements'
        
        mid_response = f"I notice you're looking for {missing_tech}, which I don't have significant experience with. I do have {', '.join(candidate_skills)}, but there would be a learning curve. Would this role allow for training or mentorship on the areas where I'm less experienced?"
        final_response = f"I'm genuinely interested, but I want to set realistic expectations. If you're open to some ramp-up time and willing to support learning, I think I could grow into this role. Otherwise, I understand if you need someone more immediately productive."
        
        positive_signals = [
            "Shows self-awareness about skill gaps",
            "Honest about experience level",
            "Expresses genuine interest despite challenges",
            "Willing to invest in learning"
        ]
        concerns = [
            f"Missing expertise: {missing_tech}",
            "Would require training/mentorship",
            "Longer ramp-up time expected",
            "May not meet immediate project demands"
        ]
    
    # Build recruiter responses that acknowledge candidate tone
    recruiter_opening = f"Hi {candidate_name}, I found your profile very interesting for our {jd_title} role. Your experience with {', '.join(candidate_skills)} caught our attention. Would you be open to a conversation?"
    
    if match_score >= 80:
        recruiter_mid = f"Excellent! We're building {['mission-critical systems', 'next-generation products', 'scalable infrastructure'][random.randint(0,2)]} and looking for someone with exactly your expertise. The team is highly collaborative, and we love technical discussions."
    elif match_score >= 60:
        recruiter_mid = f"Great question. The role involves {['system design and architecture', 'building scalable solutions', 'leading technical initiatives'][random.randint(0,2)]}. We're a supportive team and invest in continuous learning."
    else:
        recruiter_mid = f"I appreciate your honesty. We do have some flexibility with the tech stack learning, especially for someone with strong fundamentals. {['We offer mentorship', 'The team is supportive', 'We can provide training'][random.randint(0,2)]}. What's your appetite for learning new technologies?"
    
    recruiter_closing = "Your background is valuable. Let's schedule a technical discussion to see if this is the right fit."
    
    return {
        "interest_score": interest_score,
        "likelihood": likelihood,
        "reasoning": [
            f"Match quality: {match_score}/100",
            f"Experience alignment: {candidate_exp}",
            "Demonstrated interest in similar roles" if match_score >= 60 else "Potential fit with appropriate support"
        ],
        "positive_signals": positive_signals,
        "concerns": concerns,
        "conversation": [
            {
                "role": "recruiter",
                "text": recruiter_opening,
                "sentiment": "professional"
            },
            {
                "role": "candidate",
                "text": opening_response,
                "sentiment": "enthusiastic" if match_score >= 80 else "interested" if match_score >= 60 else "cautious"
            },
            {
                "role": "recruiter",
                "text": recruiter_mid,
                "sentiment": "professional"
            },
            {
                "role": "candidate",
                "text": mid_response,
                "sentiment": "very_positive" if match_score >= 80 else "positive" if match_score >= 60 else "neutral"
            },
            {
                "role": "recruiter",
                "text": recruiter_closing,
                "sentiment": "professional"
            },
            {
                "role": "candidate",
                "text": final_response,
                "sentiment": "very_positive" if match_score >= 80 else "interested" if match_score >= 60 else "conditional"
            }
        ]
    }
