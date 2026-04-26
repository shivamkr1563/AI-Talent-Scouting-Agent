import axios from 'axios'

// Production v2 API types
interface ParsedJD {
  title: string
  company: string
  experience_years: number
  seniority_level: string
  domain: string
  job_type: string
  location: string
  must_have_skills: string[]
  nice_to_have_skills: string[]
  key_responsibilities: string[]
  confidence_score: number
}

interface ScoringBreakdown {
  skill_match_score: number
  experience_alignment: number
  profile_fit: number
  cultural_fit: number
  reasoning: string[]
  strengths: string[]
  gaps: string[]
}

interface InterestBreakdown {
  initial_engagement: string
  opportunity_appeal: string
  conversation_quality: string
  likelihood: 'high' | 'medium' | 'low'
  positive_signals: string[]
  concerns: string[]
}

interface Conversation {
  role: 'recruiter' | 'candidate'
  text: string
  sentiment: string
}

interface CandidateResult {
  name: string
  title: string
  skills: string[]
  experience_years: number
  location: string
  summary: string
  match_score: number
  match_breakdown: ScoringBreakdown
  interest_score: number
  interest_breakdown: InterestBreakdown
  conversation: Conversation[]
  combined_score: number
  rank: number
  recommendation: string
}

interface ExecutionMetrics {
  jd_parsing_time: number
  candidate_scoring_time: number
  outreach_time: number
  total_time_seconds: number
  errors_encountered: number
}

interface AgentResult {
  parsed_jd: ParsedJD
  candidates: CandidateResult[]
  metrics: ExecutionMetrics
  success: boolean
  message: string
}

interface RunAgentRequest {
  job_description: string
  company_name?: string
  max_candidates?: number
}

const API_URL = import.meta.env.VITE_API_URL || '/api'

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const runAgent = async (jobDescription: string, companyName = 'TechCorp', maxCandidates = 10): Promise<AgentResult> => {
  const payload: RunAgentRequest = {
    job_description: jobDescription,
    company_name: companyName,
    max_candidates: maxCandidates,
  }
  const response = await apiClient.post<AgentResult>('/v2/run', payload)
  return response.data
}

export type { ParsedJD, Conversation, CandidateResult, AgentResult, ScoringBreakdown, InterestBreakdown, ExecutionMetrics }
