from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ==================== REQUESTS ====================

class RunAgentRequest(BaseModel):
    job_description: str = Field(..., min_length=100, max_length=5000)
    company_name: Optional[str] = None
    max_candidates: int = Field(default=10, ge=1, le=100)


# ==================== JD ANALYSIS ====================

class SkillMatch(BaseModel):
    skill: str
    required: bool
    candidate_has: Optional[bool] = None
    proficiency: Optional[str] = None  # beginner, intermediate, expert


class ParsedJD(BaseModel):
    title: str
    company: str
    top_skills: list[str]
    nice_to_have_skills: list[str] = []
    experience_years: int
    experience_description: str
    domain: str
    seniority_level: str  # junior, mid, senior, lead
    location: Optional[str] = None
    job_type: str = "full-time"  # full-time, contract, part-time
    key_responsibilities: list[str] = []
    must_have_skills: list[str] = []


class JDAnalysis(BaseModel):
    parsed_jd: ParsedJD
    analysis_timestamp: datetime = Field(default_factory=datetime.utcnow)
    analysis_confidence: float = Field(ge=0, le=1)  # 0-1 confidence score


# ==================== CANDIDATE ====================

class Conversation(BaseModel):
    role: str  # "recruiter" | "candidate"
    text: str
    sentiment: Optional[str] = None  # positive, neutral, negative
    timestamp: Optional[datetime] = None


class ScoringBreakdown(BaseModel):
    skill_match_score: int = Field(ge=0, le=100)
    experience_alignment: int = Field(ge=0, le=100)
    profile_fit: int = Field(ge=0, le=100)
    cultural_fit: int = Field(ge=0, le=100)
    overall_match_score: int = Field(ge=0, le=100)
    reasoning: list[str]  # Detailed explanation of score
    strengths: list[str]
    gaps: list[str]


class InterestBreakdown(BaseModel):
    initial_engagement: int = Field(ge=0, le=100)
    opportunity_appeal: int = Field(ge=0, le=100)
    conversation_quality: int = Field(ge=0, le=100)
    overall_interest_score: int = Field(ge=0, le=100)
    likelihood: str  # high, medium, low
    reasoning: list[str]
    positive_signals: list[str]
    concerns: list[str]


class CandidateResult(BaseModel):
    id: int
    name: str
    title: str
    skills: list[str]
    experience_years: int
    location: Optional[str] = None
    summary: Optional[str] = None
    
    # Scoring with explainability
    match_score: int = Field(ge=0, le=100)
    match_breakdown: ScoringBreakdown
    
    interest_score: int = Field(ge=0, le=100)
    interest_breakdown: InterestBreakdown
    
    # Conversation
    conversation: list[Conversation]
    
    # Combined ranking
    combined_score: float = Field(ge=0, le=100)
    rank: int
    recommendation: str  # Strong Match, Good Fit, Potential, Review


# ==================== AGENT RESPONSE ====================

class ExecutionMetrics(BaseModel):
    total_time_seconds: float
    jd_parsing_time: float
    candidate_scoring_time: float
    outreach_time: float
    candidates_processed: int
    errors_encountered: int


class AgentResult(BaseModel):
    parsed_jd: ParsedJD
    candidates: list[CandidateResult]
    metrics: ExecutionMetrics
    generation_timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "2.0-production"


# ==================== ERROR HANDLING ====================

class ErrorResponse(BaseModel):
    error: str
    error_code: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    details: Optional[dict] = None


class ProcessingPhase(BaseModel):
    phase: str
    status: str  # pending, in-progress, completed, failed
    progress: int = Field(ge=0, le=100)
    message: str
    error: Optional[str] = None
