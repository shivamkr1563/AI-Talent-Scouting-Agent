from pydantic import BaseModel

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
