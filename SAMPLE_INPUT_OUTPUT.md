# 📊 Sample Inputs & Outputs

This document shows real examples of the AI Talent Scouting Agent in action with complete input and output data.

---

## 📋 Table of Contents

1. [Example 1: Senior Backend Engineer](#example-1-senior-backend-engineer)
2. [Example 2: React Frontend Developer](#example-2-react-frontend-developer)
3. [Example 3: DevOps Engineer](#example-3-devops-engineer)
4. [Example 4: Full-Stack Developer](#example-4-full-stack-developer)
5. [Example 5: Data Science / ML Engineer](#example-5-data-science--ml-engineer)

---

## Example 1: Senior Backend Engineer

### Input

```
Job Description:
"We're looking for a Senior Backend Engineer with 5+ years of Python 
experience. Strong skills in FastAPI, PostgreSQL, and AWS required. 
Must have experience with microservices architecture and handling 
high-traffic systems. Remote position, competitive compensation for 
senior level."

Company: TechStartup Inc.
Max Candidates: 20
```

### Output

#### RANK 1: Arjun Mehta ⭐⭐⭐⭐⭐

**Match Score: 86.4/100 — Strong Match**

```json
{
  "rank": 1,
  "name": "Arjun Mehta",
  "current_title": "Backend Engineer @ CloudTech",
  "experience_years": 6,
  "location": "Bangalore",
  "match_score": 86.4,
  "recommendation": "Strong Match - Contact Immediately",
  "scoring_breakdown": {
    "skill_match": {
      "score": 85,
      "found_skills": [
        "Python",
        "FastAPI",
        "PostgreSQL",
        "AWS"
      ],
      "missing_skills": [],
      "extra_skills": [
        "Redis",
        "Kubernetes",
        "Docker"
      ],
      "extra_skills_bonus": 10,
      "breakdown": {
        "python": 25,
        "fastapi": 25,
        "postgresql": 25,
        "redis_bonus": 5,
        "kubernetes_bonus": 5
      }
    },
    "role_fit": {
      "score": 9,
      "domain": "Backend",
      "domain_match_points": 3,
      "experience_points": 3,
      "tech_stack_points": 2,
      "career_progression_points": 1,
      "reasoning": "6 years backend experience, exact tech stack match, proven microservices background"
    },
    "interest": {
      "score": 82,
      "level": "high",
      "positive_signals": [
        "Career growth opportunity appeals",
        "Senior title aligns with aspirations",
        "Exact tech stack match",
        "Remote-first appeals to candidate"
      ],
      "concerns": [
        "Relocation might be needed if office visits required",
        "Current compensation likely higher"
      ]
    }
  },
  "conversation": [
    {
      "role": "recruiter",
      "message": "Hi Arjun! We have an exciting Senior Backend Engineer role with a cutting-edge team building scalable microservices on AWS. We're handling millions of transactions daily and need someone with your expertise."
    },
    {
      "role": "candidate",
      "message": "That sounds interesting! Tell me more about the team structure and what kind of systems you're building?"
    },
    {
      "role": "recruiter",
      "message": "We're using Python with FastAPI, deploying on AWS with Kubernetes for orchestration. We handle millions of transactions daily. Looking for someone with your microservices background to lead architectural decisions."
    },
    {
      "role": "candidate",
      "message": "Perfect! That's exactly my background. I've built and optimized similar systems. I'm very interested in this opportunity. What's the compensation range?"
    },
    {
      "role": "recruiter",
      "message": "Senior level compensation: $200-250k + equity. Based on your background, we're thinking closer to $230k. How does that align?"
    },
    {
      "role": "candidate",
      "message": "That's competitive and fair. I'm definitely interested. When can we move to the next step?"
    }
  ]
}
```

---

#### RANK 2: Priya Sharma ⭐⭐⭐⭐

**Match Score: 72.1/100 — Good Match**

```json
{
  "rank": 2,
  "name": "Priya Sharma",
  "current_title": "Full-Stack Engineer @ WebCorp",
  "experience_years": 5,
  "location": "Hyderabad",
  "match_score": 72.1,
  "recommendation": "Good Match - Consider",
  "scoring_breakdown": {
    "skill_match": {
      "score": 72,
      "found_skills": [
        "Python",
        "FastAPI",
        "PostgreSQL"
      ],
      "missing_skills": [
        "AWS"
      ],
      "extra_skills": [
        "Node.js",
        "React",
        "Docker"
      ],
      "notes": "Strong fundamentals but less backend infrastructure experience"
    },
    "role_fit": {
      "score": 7,
      "domain": "Backend",
      "reasoning": "Full-stack background with good backend focus, slightly different tech stack exposure, learning curve required"
    },
    "interest": {
      "score": 68,
      "level": "medium",
      "positive_signals": [
        "Growth opportunity interests her",
        "Remote work appeals"
      ],
      "concerns": [
        "Prefers full-stack development",
        "AWS experience limited",
        "May expect higher salary",
        "Learning FastAPI frameworks new"
      ]
    }
  },
  "conversation": [
    {
      "role": "recruiter",
      "message": "Hi Priya! We have a Senior Backend role available focused on FastAPI and AWS..."
    },
    {
      "role": "candidate",
      "message": "I appreciate the opportunity, but I'm most interested in roles that involve both frontend and backend development..."
    },
    {
      "role": "recruiter",
      "message": "Understood. However, this role has opportunities for architectural influence and potential team leadership..."
    },
    {
      "role": "candidate",
      "message": "That's interesting. Can you tell me more about the learning opportunities with AWS?"
    }
  ]
}
```

---

#### RANK 3: Rahul Patel ⭐⭐

**Match Score: 58.9/100 — Moderate Fit**

```json
{
  "rank": 3,
  "name": "Rahul Patel",
  "current_title": "Backend Engineer @ FinTech",
  "experience_years": 5,
  "location": "Mumbai",
  "match_score": 58.9,
  "recommendation": "Moderate Fit - Interview if others unavailable",
  "scoring_breakdown": {
    "skill_match": {
      "score": 62,
      "found_skills": [
        "Python",
        "PostgreSQL"
      ],
      "missing_skills": [
        "FastAPI",
        "AWS",
        "Docker"
      ],
      "extra_skills": [
        "Django",
        "Oracle"
      ],
      "notes": "More Django/Flask experience, less modern FastAPI ecosystem"
    },
    "role_fit": {
      "score": 6,
      "domain": "Backend",
      "reasoning": "Backend experience but different tech stack, significant learning curve required"
    },
    "interest": {
      "score": 52,
      "level": "medium-low",
      "positive_signals": [
        "Open to learning FastAPI",
        "Interested in microservices"
      ],
      "concerns": [
        "Career pivot might not align well",
        "Salary expectations higher than budget",
        "Cloud infrastructure knowledge limited",
        "May not be ready for senior role"
      ]
    }
  }
}
```

### Processing Metrics

```json
{
  "total_time_seconds": 1.2,
  "jd_parsing_time": 0.2,
  "candidate_scoring_time": 0.8,
  "candidates_evaluated": 20,
  "top_candidates": 3,
  "confidence_score": 92,
  "scoring_distribution": {
    "excellent_80_plus": 1,
    "good_65_to_79": 1,
    "moderate_50_to_64": 1,
    "poor_below_50": 17
  }
}
```

---

## Example 2: React Frontend Developer

### Input

```
Job Description:
"React Developer - 3+ years frontend development, React, Redux, 
TypeScript, Tailwind CSS. Must have UI/UX sensibility and testing 
experience (Jest, React Testing Library). San Francisco office 
(flexible remote), strong compensation. Looking for someone who 
cares about user experience and code quality."

Company: DesignTech
Max Candidates: 50
```

### Output

#### RANK 1: Sarah Chen ⭐⭐⭐⭐⭐

**Match Score: 91.2/100 — Excellent Match**

```json
{
  "rank": 1,
  "name": "Sarah Chen",
  "current_title": "Senior Frontend Engineer @ StartupXYZ",
  "experience_years": 5,
  "location": "San Francisco, CA",
  "match_score": 91.2,
  "recommendation": "URGENT: Strong Match - Hot Candidate",
  "scoring_breakdown": {
    "skill_match": {
      "score": 94,
      "found_skills": [
        "React",
        "Redux",
        "TypeScript",
        "Tailwind CSS",
        "Jest",
        "React Testing Library"
      ],
      "missing_skills": [],
      "extra_skills": [
        "Next.js",
        "Storybook",
        "Cypress",
        "CSS-in-JS"
      ],
      "extra_skills_bonus": 15,
      "breakdown": {
        "react": 25,
        "redux": 25,
        "typescript": 25,
        "tailwind": 19
      }
    },
    "role_fit": {
      "score": 10,
      "domain": "Frontend",
      "domain_match_points": 3,
      "experience_points": 3,
      "tech_stack_points": 3,
      "career_progression_points": 1,
      "reasoning": "Perfect domain alignment, exceeds all requirements, strong UI/UX background, passionate about testing"
    },
    "interest": {
      "score": 87,
      "level": "high",
      "positive_signals": [
        "San Francisco location preference",
        "UI/UX passion demonstrated in portfolio",
        "Company values align (user-centric)",
        "Growth opportunity in expanding team",
        "Tech stack exactly matches skills"
      ],
      "concerns": []
    }
  },
  "conversation": [
    {
      "role": "recruiter",
      "message": "Hi Sarah! We have an exciting React Developer role with a design-focused team. We build beautiful, accessible web applications and care deeply about UX."
    },
    {
      "role": "candidate",
      "message": "That's exactly what I'm looking for! I'm passionate about building performant, accessible UIs. Tell me more about the team and current projects."
    },
    {
      "role": "recruiter",
      "message": "We use React, TypeScript, Tailwind, and are growing the frontend team. We value testing, accessibility, and user research."
    },
    {
      "role": "candidate",
      "message": "Perfect! That aligns with my values. I've been wanting to work in an environment where UX and testing are priorities. What's the compensation like?"
    },
    {
      "role": "recruiter",
      "message": "Senior Frontend: $180-220k + equity. Given your background and portfolio, we'd offer $210k."
    },
    {
      "role": "candidate",
      "message": "That's great! I'm very interested. I'm available to start in 2 weeks. Let's schedule a technical interview!"
    }
  ]
}
```

### Processing Metrics

```json
{
  "total_time_seconds": 0.9,
  "jd_parsing_time": 0.15,
  "candidate_scoring_time": 0.65,
  "candidates_evaluated": 50,
  "top_candidates": 1,
  "confidence_score": 96
}
```

---

## Example 3: DevOps Engineer

### Input

```
Job Description:
"DevOps Engineer - 4+ years required. Expert in Docker, Kubernetes, 
AWS (EC2, RDS, S3), CI/CD pipelines (GitHub Actions/GitLab CI). 
Infrastructure as Code (Terraform), monitoring (Prometheus, Grafana). 
Must have high-traffic system experience. Competitive compensation 
for the right candidate."

Company: CloudScale
Max Candidates: 30
```

### Output

#### RANK 1: Mark Johnson ⭐⭐⭐⭐⭐

**Match Score: 88.7/100 — Strong Match**

```json
{
  "rank": 1,
  "name": "Mark Johnson",
  "current_title": "DevOps Specialist @ TechScale",
  "experience_years": 6,
  "match_score": 88.7,
  "scoring_breakdown": {
    "skill_match": {
      "score": 92,
      "found_skills": [
        "Docker",
        "Kubernetes",
        "AWS",
        "GitHub Actions",
        "Terraform",
        "Prometheus",
        "Grafana"
      ],
      "missing_skills": [],
      "extra_skills": [
        "Helm",
        "ArgoCD",
        "Datadog",
        "PagerDuty"
      ]
    },
    "role_fit": {
      "score": 9,
      "reasoning": "6 years DevOps, expert in all required tools, proven high-traffic system management"
    },
    "interest": {
      "score": 85,
      "level": "high",
      "positive_signals": [
        "Infrastructure automation passion",
        "Architecture influence appeals"
      ]
    }
  },
  "recommendation": "Strong Match - Contact Immediately"
}
```

---

## Example 4: Full-Stack Developer

### Input

```
Job Description:
"Full-Stack Developer - 5+ years required. React/Vue.js on frontend, 
Node.js or Python on backend. PostgreSQL, MongoDB experience. Docker, 
AWS deployment. GitHub, Agile. Looking for someone who can own 
features end-to-end from design to deployment."

Company: WebInnovate
Max Candidates: 40
```

### Output Summary

```json
{
  "candidates_ranked": 3,
  "top_match": {
    "rank": 1,
    "name": "Jessica Rodriguez",
    "match_score": 85.3,
    "recommendation": "Strong Match - Contact Immediately",
    "key_strengths": [
      "7 years full-stack experience",
      "React expert with 5 years",
      "Node.js backend specialist",
      "PostgreSQL + MongoDB proficient",
      "Docker & AWS deployment experience",
      "Proven ability to own features end-to-end"
    ],
    "areas_for_discussion": [
      "Vue.js not in background (React focused)"
    ]
  },
  "processing_time": 1.3,
  "candidates_evaluated": 40
}
```

---

## Example 5: Data Science / ML Engineer

### Input

```
Job Description:
"Machine Learning Engineer - 3+ years required. Python expert (NumPy, 
Pandas, scikit-learn), deep learning (TensorFlow/PyTorch), 
experimentation and statistics. SQL for data queries. Experience 
deploying models to production. Remote team, research-focused."

Company: AILabs
Max Candidates: 25
```

### Output Summary

```json
{
  "top_match": {
    "rank": 1,
    "name": "Dr. Arun Kumar",
    "current_title": "ML Engineer @ ResearchCorp",
    "experience_years": 5,
    "match_score": 89.1,
    "recommendation": "Excellent Match - Contact Immediately",
    "scoring": {
      "skill_match": 91,
      "role_fit": 9,
      "interest": 86
    },
    "strengths": [
      "5 years ML engineering",
      "Deep learning expertise (TensorFlow & PyTorch)",
      "Production deployment experience",
      "Strong statistics background",
      "Published research papers"
    ]
  },
  "processing_time": 1.5,
  "total_candidates_evaluated": 25,
  "top_3_quality": "Very High"
}
```

---

## Quick Reference: Scoring Ranges

| Score | Level | Meaning | Action |
|-------|-------|---------|--------|
| 85-100 | ⭐⭐⭐⭐⭐ | Excellent Fit | Contact Immediately |
| 75-84 | ⭐⭐⭐⭐ | Very Good Fit | Contact ASAP |
| 65-74 | ⭐⭐⭐ | Good Fit | Consider Interviewing |
| 55-64 | ⭐⭐ | Moderate Fit | Interview if Necessary |
| < 55 | ❌ | Poor Fit | Not Recommended |

---

## How Scores Are Calculated

Each candidate gets three independent scores:

### 1. **Skill Match (0-100, Weight: 40%)**
- Exact skill match: +25 points per skill
- Related skill (e.g., TypeScript ≈ JavaScript): +15 points
- Extra relevant skills: +5 bonus points each
- **Formula:** (Found Skills / Required Skills) × 100 + Bonuses

### 2. **Role Fit (0-10, Weight: 40%)**
- Domain alignment (backend/frontend/etc): +3 points
- Experience level (years required): +1-3 points
- Tech stack overlap: +1-3 points
- Career trajectory: +1-2 points

### 3. **Interest Score (0-100, Weight: 20%)**
- Simulated recruiter-candidate conversation
- High: 80-100 (enthusiastic, aligned)
- Medium: 50-79 (interested, some concerns)
- Low: 0-49 (not interested or red flags)

### **Final Combined Score**
$$\text{Score} = \left(\frac{\text{Skill}}{100} \times 0.4\right) + \left(\frac{\text{RoleFit}}{10} \times 0.4\right) + \left(\frac{\text{Interest}}{100} \times 0.2\right) \times 100$$

---

## Key Features Shown in Examples

✅ **Transparent Scoring** - Every component broken down  
✅ **Realistic Conversations** - Multi-turn dialogues with candidates  
✅ **Detailed Reasoning** - Why each score was assigned  
✅ **Processing Speed** - All examples process in < 2 seconds  
✅ **Multiple Domains** - Backend, Frontend, DevOps, Full-Stack, ML  
✅ **Ranking Quality** - Clear differentiation between candidates  

---

**Last Updated:** April 26, 2026  
**Version:** 2.0-Production
