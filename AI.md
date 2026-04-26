# AI Talent Scouting Agent — Implementation Plan

> Stack: FastAPI (Python) + Vite + React (TypeScript)

-----

## Project Structure


talent-scout/
├── backend/
│   ├── main.py
│   ├── routers/
│   │   └── agent.py
│   ├── services/
│   │   ├── jd_parser.py
│   │   ├── candidate_matcher.py
│   │   └── outreach_simulator.py
│   ├── models/
│   │   └── schemas.py
│   ├── data/
│   │   └── mock_candidates.json
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── vite.config.ts
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── api/
│   │   │   └── agent.ts
│   │   └── components/
│   │       ├── JDInput.tsx
│   │       ├── CandidateCard.tsx
│   │       ├── PhaseLog.tsx
│   │       └── Shortlist.tsx
│   └── package.json
└── README.md


-----

## Phase 1 — Backend Setup

### 1.1 Init & Install

bash
cd backend
python -m venv venv && source venv/bin/activate
pip install fastapi uvicorn anthropic pydantic python-dotenv


### 1.2 requirements.txt


fastapi
uvicorn[standard]
anthropic
pydantic
python-dotenv


### 1.3 .env


ANTHROPIC_API_KEY=your_key_here


-----

## Phase 2 — Backend Code

### 2.1 models/schemas.py

Define Pydantic models:

python
# Request
class RunAgentRequest(BaseModel):
    job_description: str

# Response building blocks
class ParsedJD(BaseModel):
    title: str
    company: str
    top_skills: list[str]
    experience: str
    domain: str

class Conversation(BaseModel):
    role: str   # "recruiter" | "candidate"
    text: str

class CandidateResult(BaseModel):
    id: int
    name: str
    title: str
    skills: list[str]
    match_score: int
    match_reason: str
    interest_score: int
    interest_reason: str
    conversation: list[Conversation]

class AgentResult(BaseModel):
    parsed_jd: ParsedJD
    candidates: list[CandidateResult]


### 2.2 services/jd_parser.py

python
import anthropic, json, os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def parse_jd(jd_text: str) -> dict:
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system="Extract structured info from job descriptions. Return ONLY valid JSON. No markdown.",
        messages=[{
            "role": "user",
            "content": f"Schema: {{title, company, top_skills[], experience, domain}}\n\nJD:\n{jd_text}"
        }]
    )
    return json.loads(msg.content[0].text)


### 2.3 services/candidate_matcher.py

python
def score_candidates(jd_summary: dict, candidates: list[dict]) -> list[dict]:
    # Build prompt with all candidates, ask Claude to return match scores + reasons
    # Return list of {id, match_score, match_reason}
    ...


### 2.4 services/outreach_simulator.py

python
def simulate_outreach(candidate: dict, jd_title: str) -> dict:
    # Prompt Claude to simulate 3-turn recruiter<>candidate conversation
    # Return {conversation: [], interest_score, interest_reason}
    ...


### 2.5 routers/agent.py

python
from fastapi import APIRouter
from models.schemas import RunAgentRequest, AgentResult
from services import jd_parser, candidate_matcher, outreach_simulator
import json

router = APIRouter(prefix="/api")

@router.post("/run", response_model=AgentResult)
async def run_agent(req: RunAgentRequest):
    # 1. Parse JD
    parsed = jd_parser.parse_jd(req.job_description)

    # 2. Load mock candidates
    with open("data/mock_candidates.json") as f:
        candidates = json.load(f)

    # 3. Score candidates
    scores = candidate_matcher.score_candidates(parsed, candidates)

    # 4. Simulate outreach for each
    results = []
    for cand in candidates:
        score = next(s for s in scores if s["id"] == cand["id"])
        outreach = outreach_simulator.simulate_outreach(cand, parsed["title"])
        results.append({**cand, **score, **outreach})

    # 5. Sort by combined score
    results.sort(key=lambda x: x["match_score"] * 0.5 + x["interest_score"] * 0.5, reverse=True)

    return {"parsed_jd": parsed, "candidates": results}


### 2.6 main.py

python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.agent import router
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


*Run backend:*

bash
uvicorn main:app --reload --port 8000


-----

## Phase 3 — Frontend Setup

### 3.1 Init Vite + React + TS

bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm install axios


### 3.2 vite.config.ts — Proxy API

ts
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})


### 3.3 src/api/agent.ts

ts
import axios from 'axios'

export const runAgent = (jobDescription: string) =>
  axios.post('/api/run', { job_description: jobDescription })
    .then(res => res.data)


### 3.4 Components

|Component          |Responsibility                         |
|-------------------|---------------------------------------|
|JDInput.tsx      |Textarea + Run button                  |
|PhaseLog.tsx     |Step-by-step progress display          |
|CandidateCard.tsx|Scores, skills, expandable conversation|
|Shortlist.tsx    |Final ranked table                     |

### 3.5 App.tsx flow

ts
const handleRun = async () => {
  setLoading(true)
  const result = await runAgent(jd)
  setJdAnalysis(result.parsed_jd)
  setCandidates(result.candidates)
  setLoading(false)
}


*Run frontend:*

bash
npm run dev  # → http://localhost:5173


-----

## Phase 4 — Data

### data/mock_candidates.json

json
[
  {
    "id": 1,
    "name": "Arjun Mehta",
    "title": "ML Engineer @ Swiggy",
    "skills": ["PyTorch", "Recommender Systems", "Kafka", "Python"],
    "experience": "5 years",
    "summary": "Built food personalization engine for 80M+ users."
  },
  ...
]


> *To extend:* swap mock JSON with a real database (PostgreSQL + SQLAlchemy) or LinkedIn API.

-----

## Phase 5 — Claude Code Prompts

Run these in Claude Code in order:


1. "Create the FastAPI project structure as per PLAN.md"

2. "Implement jd_parser.py using the Anthropic Python SDK"

3. "Implement candidate_matcher.py — batch score all candidates in one API call"

4. "Implement outreach_simulator.py — use asyncio.gather to run all outreach calls concurrently"

5. "Wire up the router and main.py with CORS"

6. "Scaffold the Vite+React frontend with the component structure from PLAN.md"

7. "Connect frontend to backend via axios, replicate the UI from the React artifact"

8. "Add loading states and error handling on both frontend and backend"


-----

## API Reference

|Method|Endpoint  |Body                         |Returns      |
|------|----------|-----------------------------|-------------|
|POST  |/api/run|{ job_description: string }|AgentResult|

-----

## Key Design Decisions

- *Single POST endpoint* — keeps the frontend simple; agent orchestration lives entirely in backend
- *Concurrent outreach* — use asyncio.gather for parallel Claude calls per candidate (faster)
- *Vite proxy* — avoids CORS issues in dev; in prod, deploy behind nginx or use env var for API base URL
- *Pydantic schemas* — type-safe contract between frontend and backend

-----

## Future Extensions

- Stream results back via *SSE* (Server-Sent Events) for live phase updates
- Replace mock candidates with *PostgreSQL + pgvector* for semantic search
- Add *email outreach draft* generation per candidate
- Auth layer with *FastAPI + JWT*