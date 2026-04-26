# Sample Inputs & Outputs

This document provides real examples of job descriptions, parsed requirements, and scored results from the AI Talent Scouting Agent.

---

## Example 1: Senior Backend Engineer (Python/FastAPI)

### Input: Job Description

```
Senior Backend Engineer - TechCorp

We're building the next generation of financial technology and we need a 
backend engineer who loves solving complex problems.

Requirements:
- 4+ years of backend development experience
- Strong proficiency in Python
- Experience with FastAPI or Django
- PostgreSQL or MongoDB expertise
- AWS/GCP cloud platform experience
- Docker and Kubernetes familiarity
- Microservices architecture knowledge

Nice to have:
- Event-driven systems (Apache Kafka, RabbitMQ)
- DynamoDB or Redis caching
- GraphQL

Location: Remote or Bangalore
Compensation: Competitive
```

### Processing

**Step 1: JD Parsing**

```json
{
  "title": "Senior Backend Engineer",
  "domain": "Backend",
  "seniority_level": "senior",
  "experience_years": 4,
  "location": "Remote/Bangalore",
  "must_have_skills": ["Python", "FastAPI", "PostgreSQL", "AWS"],
  "nice_to_have_skills": ["Docker", "Kubernetes", "Kafka", "Redis"],
  "top_skills": ["Python", "FastAPI", "PostgreSQL", "AWS"]
}
```

**Step 2: Load Candidates** (3 candidates from database)

```json
[
  {
    "id": 1,
    "name": "Arjun Mehta",
    "title": "Backend Engineer at DataStartup",
    "skills": ["Python", "FastAPI", "PostgreSQL", "AWS", "Redis"],
    "experience_years": 6,
    "location": "Bangalore"
  },
  {
    "id": 2,
    "name": "Priya Sharma",
    "title": "Data Engineer at CloudCorp",
    "skills": ["Python", "Spark", "AWS", "PostgreSQL", "REST APIs"],
    "experience_years": 5,
    "location": "NYC"
  },
  {
    "id": 3,
    "name": "Rahul Patel",
    "title": "Software Engineer at WebCo",
    "skills": ["Python", "Django", "MySQL", "Docker"],
    "experience_years": 3,
    "location": "San Francisco"
  }
]
```

### Output: API Response

```json
{
  "parsed_jd": {
    "title": "Senior Backend Engineer",
    "domain": "Backend",
    "seniority_level": "senior",
    "experience_years": 4,
    "location": "Remote/Bangalore",
    "must_have_skills": ["Python", "FastAPI", "PostgreSQL", "AWS"],
    "nice_to_have_skills": ["Docker", "Kubernetes", "Kafka", "Redis"],
    "top_skills": ["Python", "FastAPI", "PostgreSQL", "AWS"]
  },
  "candidates": [
    {
      "id": 1,
      "name": "Arjun Mehta",
      "title": "Backend Engineer at DataStartup",
      "experience_years": 6,
      "location": "Bangalore",
      "rank": 1,
      "match_score": 92,
      "interest_score": 87,
      "combined_score": 90.5,
      "recommendation": "Strong Match",
      "match_breakdown": {
        "skill_match_score": 95,
        "experience_alignment": 92,
        "profile_fit": 88,
        "cultural_fit": 85,
        "reasoning": [
          "Has 6 years Python backend experience, exceeds requirement",
          "Expert in FastAPI - exact tech stack match",
          "Strong PostgreSQL and AWS expertise",
          "Redis caching experience is bonus",
          "Based in Bangalore, matches location"
        ],
        "strengths": [
          "All required skills present",
          "2+ years above requirement",
          "Exact tech match for role",
          "Nice-to-have skills (Redis)"
        ],
        "gaps": [
          "Limited Kubernetes experience",
          "Kafka exposure not evident"
        ]
      },
      "interest_breakdown": {
        "likelihood": "high",
        "positive_signals": [
          "Strong technical alignment with role",
          "Growth opportunity in fintech appeals",
          "Working with larger systems of scale",
          "Team leadership potential"
        ],
        "concerns": [
          "Currently at startup, may want stability",
          "Salary expectations likely high given experience"
        ]
      },
      "conversation": [
        {
          "role": "recruiter",
          "text": "Hi Arjun! I found your profile and was impressed by your FastAPI expertise. We're hiring a Senior Backend Engineer at TechCorp working on financial systems. Would you be open to a conversation?",
          "sentiment": "professional"
        },
        {
          "role": "candidate",
          "text": "Thanks for reaching out! I'm always interested in exploring new opportunities. I've been wanting to work on fintech systems. What's the team structure like?",
          "sentiment": "positive"
        },
        {
          "role": "recruiter",
          "text": "Great! We have a team of 12 backend engineers across multiple products. You'd be leading the payments platform using FastAPI and PostgreSQL. The role involves system design and mentoring juniors.",
          "sentiment": "professional"
        },
        {
          "role": "candidate",
          "text": "That sounds excellent. System design and mentoring are both areas I'm passionate about. I'd love to learn more about the architecture and roadmap. When can we schedule a technical discussion?",
          "sentiment": "very_positive"
        }
      ]
    },
    {
      "id": 2,
      "name": "Priya Sharma",
      "title": "Data Engineer at CloudCorp",
      "experience_years": 5,
      "location": "NYC",
      "rank": 2,
      "match_score": 78,
      "interest_score": 75,
      "combined_score": 77.5,
      "recommendation": "Good Match",
      "match_breakdown": {
        "skill_match_score": 75,
        "experience_alignment": 85,
        "profile_fit": 72,
        "cultural_fit": 70,
        "reasoning": [
          "Python and AWS expertise strong",
          "Data engineering background provides database knowledge",
          "PostgreSQL experience present",
          "Missing FastAPI - biggest gap",
          "Might transition from data to backend successfully"
        ],
        "strengths": [
          "Strong Python skills",
          "AWS expert",
          "5 years experience matches requirement",
          "Database knowledge transferable"
        ],
        "gaps": [
          "No FastAPI experience (framework specific)",
          "Background in data engineering, not backend",
          "Would need ramp-up time on microservices patterns"
        ]
      },
      "interest_breakdown": {
        "likelihood": "medium",
        "positive_signals": [
          "Open to backend transition",
          "Excited about systems scale",
          "Interested in mentoring juniors"
        ],
        "concerns": [
          "Career pivot from data to backend",
          "Would need framework training",
          "Location preference: NYC vs Remote"
        ]
      },
      "conversation": [
        {
          "role": "recruiter",
          "text": "Hi Priya, your data engineering background and AWS expertise caught our attention. We have a backend role that could be a great next step for you. Interested?",
          "sentiment": "professional"
        },
        {
          "role": "candidate",
          "text": "Interesting. I've been thinking about moving closer to core backend work. What framework does TechCorp use? I have some web frameworks experience but not in production systems.",
          "sentiment": "neutral"
        },
        {
          "role": "recruiter",
          "text": "We use FastAPI, which is modern Python. Your data systems knowledge would help with database optimization. Would you be open to learning FastAPI while contributing?",
          "sentiment": "professional"
        },
        {
          "role": "candidate",
          "text": "That makes sense. I've learned frameworks quickly in the past. The fintech focus is compelling. Let's talk more about the learning curve and team support.",
          "sentiment": "positive"
        }
      ]
    },
    {
      "id": 3,
      "name": "Rahul Patel",
      "title": "Software Engineer at WebCo",
      "experience_years": 3,
      "location": "San Francisco",
      "rank": 3,
      "match_score": 62,
      "interest_score": 70,
      "combined_score": 65.0,
      "recommendation": "Potential",
      "match_breakdown": {
        "skill_match_score": 58,
        "experience_alignment": 60,
        "profile_fit": 68,
        "cultural_fit": 75,
        "reasoning": [
          "Python and Docker experience good",
          "Only 3 years experience vs 4+ required",
          "Django instead of FastAPI",
          "MySQL instead of PostgreSQL",
          "Missing AWS and Kubernetes entirely",
          "Would be junior for Senior role"
        ],
        "strengths": [
          "Python foundation solid",
          "Docker containerization knowledge",
          "Eager and trainable profile",
          "Good cultural fit indicators"
        ],
        "gaps": [
          "3 years vs 4+ required - junior for role",
          "No FastAPI (would need to learn)",
          "No AWS/cloud experience",
          "No PostgreSQL (different SQL DB)",
          "Senior role might be stretch"
        ]
      },
      "interest_breakdown": {
        "likelihood": "medium",
        "positive_signals": [
          "Interested in growth opportunity",
          "Willing to learn new technologies",
          "Strong work ethic evident"
        ],
        "concerns": [
          "Significant jump from 3 to senior role",
          "Would need close mentoring",
          "Tech stack different from current",
          "May be overqualified ambitions vs current level"
        ]
      },
      "conversation": [
        {
          "role": "recruiter",
          "text": "Hi Rahul, I noticed you're working with Python and Docker. We have a Senior Backend Engineer role that might be interesting as your next career move. Are you open to growth opportunities?",
          "sentiment": "professional"
        },
        {
          "role": "candidate",
          "text": "Thanks for thinking of me. I'm definitely interested in growing. A senior role would be exciting but I want to be realistic about my experience level. What would the support look like?",
          "sentiment": "positive"
        },
        {
          "role": "recruiter",
          "text": "Great self-awareness. This role does require 4+ years ideally, but your Python skills are solid. We could structure it with close mentoring and focus on FastAPI and PostgreSQL training initially.",
          "sentiment": "professional"
        },
        {
          "role": "candidate",
          "text": "That sounds fair. I'm definitely capable of learning new frameworks. FastAPI is on my learning list anyway. I'd be excited to fast-track with professional guidance. When's the next step?",
          "sentiment": "positive"
        }
      ]
    }
  ],
  "metrics": {
    "total_time_seconds": 1.24,
    "candidates_processed": 3,
    "errors_encountered": 0
  }
}
```

---

## Example 2: React Developer (Frontend)

### Input: Job Description

```
React Developer - MobileFirst Inc

Looking for a React Developer with modern web experience.

Skills needed:
- 3+ years React experience
- TypeScript proficiency
- Tailwind CSS or similar
- REST API integration
- Testing: Jest/React Testing Library

Preferred:
- Next.js experience
- GraphQL knowledge
- Design system work

Location: NYC, hybrid
```

### Output: Parsed JD

```json
{
  "title": "React Developer",
  "domain": "Frontend",
  "seniority_level": "mid",
  "experience_years": 3,
  "location": "NYC",
  "must_have_skills": ["React", "TypeScript", "Tailwind CSS", "REST APIs"],
  "nice_to_have_skills": ["Next.js", "GraphQL", "Jest"],
  "top_skills": ["React", "TypeScript", "REST APIs"]
}
```

### Output: Ranked Candidates

```json
{
  "candidates": [
    {
      "name": "Priya Sharma",
      "rank": 1,
      "match_score": 88,
      "interest_score": 82,
      "combined_score": 86,
      "recommendation": "Strong Match",
      "strengths": [
        "4 years React experience",
        "TypeScript expert",
        "Built with Tailwind in 3+ projects",
        "Strong REST API integration skills"
      ]
    },
    {
      "name": "Arjun Mehta",
      "rank": 2,
      "match_score": 72,
      "interest_score": 78,
      "combined_score": 74,
      "recommendation": "Good Match",
      "gaps": [
        "Limited TypeScript (mainly JavaScript)",
        "No Tailwind CSS experience",
        "But GraphQL knowledge is strong bonus"
      ]
    }
  ]
}
```

---

## Example 3: DevOps Engineer

### Input: Job Description

```
DevOps Engineer / Site Reliability Engineer

5+ years DevOps/SRE experience
Linux administration
Kubernetes and Docker
AWS infrastructure (EC2, S3, RDS, Lambda)
CI/CD pipelines (Jenkins, GitLab CI, GitHub Actions)
Monitoring: Prometheus, Grafana
Infrastructure as Code (Terraform, CloudFormation)

Location: Remote (worldwide)
```

### Output: Ranking

```
1. [Candidate with 7 years K8s + AWS] ✓ 89/100
2. [Candidate with 5 years Docker + some K8s] ✓ 76/100
3. [Candidate with 4 years ops but no IaC] ⚠ 65/100
```

---

## Example 4: Machine Learning Engineer

### Input: Job Description

```
ML Engineer - AIStartup

3+ years ML/AI experience
Python expert
Deep learning frameworks (PyTorch or TensorFlow)
Computer vision OR NLP specialization
Model deployment experience
AWS SageMaker or similar

Nice: LLMs, RAG systems, RLHF
```

### Output: Top Candidate

```json
{
  "name": "Arjun Mehta",
  "rank": 1,
  "match_score": 91,
  "interest_score": 88,
  "combined_score": 90,
  "recommendation": "Perfect Match",
  "reasoning": [
    "6+ years ML experience",
    "PyTorch expert",
    "Computer vision specialization",
    "Recent LLM fine-tuning experience",
    "AWS SageMaker deployment experience"
  ]
}
```

---

## Example 5: Full-Stack Developer

### Input: Job Description

```
Full-Stack Developer - WebStartup

Needed:
- 4+ years full-stack development
- Frontend: React, Vue, or Angular
- Backend: Node.js, Python, or Java
- Databases: SQL and NoSQL
- Cloud: AWS/GCP/Azure
- Agile/Scrum experience

Location: Remote
```

### Output: Processing Multiple Candidates

```json
{
  "candidates": [
    {
      "name": "Priya Sharma",
      "rank": 1,
      "match_score": 85,
      "reasoning": [
        "5 years full-stack",
        "React + Node.js expert",
        "PostgreSQL + MongoDB experience",
        "AWS deployment experienced"
      ]
    },
    {
      "name": "Rahul Patel",
      "rank": 2,
      "match_score": 76,
      "reasoning": [
        "4 years full-stack",
        "Python + Vue background",
        "Some cloud experience",
        "Needs Node.js ramp-up"
      ]
    }
  ]
}
```

---

## Example 6: Edge Case - Very Specific Requirements

### Input: Job Description

```
Specialist: Rust Backend Engineer + WebAssembly

Rare combination needed:
- 3+ years Rust production experience
- WebAssembly compilation
- High-performance systems
- No other languages required
- Competitive salary

Location: Remote (startup)
```

### Output: Realistic Scenario

```json
{
  "candidates": [
    {
      "name": "Arjun Mehta",
      "match_score": 45,
      "gaps": [
        "No Rust experience (Python/FastAPI focused)",
        "Not a specialist match",
        "Would need 6+ months ramp-up"
      ],
      "recommendation": "Not Recommended"
    }
  ],
  "note": "Extremely specialized role. System correctly identifies that none of the current candidate pool are suitable. Recruiter should expand search to Rust-specific communities."
}
```

---

## Key Observations from Examples

### Pattern 1: Strong Technical Match
- When candidate has **exact same tech stack** → Score 85-95
- When candidate has **transferable skills** → Score 70-80

### Pattern 2: Experience Levels
- **Exceeds requirement (6+ for 4+ needed)** → Bonus +10 points
- **Meets requirement exactly** → Base score
- **Below requirement (3 for 4+ needed)** → Penalty -15 points

### Pattern 3: Interest Scores
- **Perfect tech alignment** → Higher interest (80-90)
- **Some learning required** → Medium interest (70-80)
- **Major career pivot** → Lower interest (60-70)

### Pattern 4: Conversations Reflect Reality
- Enthusiastic candidates = realistic positive responses
- Career changers = thoughtful questions about support
- Misaligned = honest concerns about fit

---

## API Usage Example (curl)

```bash
# Test the system with Example 1 request

curl -X POST http://127.0.0.1:8001/api/v2/run \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Senior Backend Engineer - 4+ years Python, FastAPI, PostgreSQL, AWS. Remote.",
    "max_candidates": 3
  }'
```

**Expected response time:** 1-2 seconds

---

## Using Sample Data for Testing

All sample job descriptions above can be directly pasted into the web UI or used in API calls. Each will produce realistic, consistent results demonstrating the system's scoring and ranking logic.

For batch testing, save these as `.txt` files and process them programmatically.
