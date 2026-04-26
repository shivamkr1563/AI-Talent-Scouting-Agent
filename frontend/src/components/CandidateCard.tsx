import React, { useState } from 'react'
import { CandidateResult } from '../api/agent'
import './CandidateCard.css'

interface CandidateCardProps {
  candidate: CandidateResult
}

export const CandidateCard: React.FC<CandidateCardProps> = ({ candidate }) => {
  const [expanded, setExpanded] = useState(false)

  const getRecommendationColor = (rec: string) => {
    if (rec.includes('Strong')) return '#4CAF50'
    if (rec.includes('Good')) return '#2196F3'
    if (rec.includes('Potential')) return '#FF9800'
    return '#9C27B0'
  }

  const getInterestColor = (likelihood: string) => {
    if (likelihood === 'high') return '#4CAF50'
    if (likelihood === 'medium') return '#FF9800'
    return '#F44336'
  }

  return (
    <div className="candidate-card">
      <div className="card-header">
        <div className="candidate-info">
          <h3>
            #{candidate.rank} - {candidate.name}
          </h3>
          <p className="position">{candidate.title}</p>
          <p className="location">📍 {candidate.location}</p>
        </div>
        <div className="score-section">
          <div className="score-badge">
            <span className="score">{Math.round(candidate.combined_score)}</span>
            <span className="score-label">/100</span>
          </div>
          <p
            className="recommendation"
            style={{ color: getRecommendationColor(candidate.recommendation) }}
          >
            {candidate.recommendation}
          </p>
        </div>
      </div>

      <div className="scores">
        <div className="score-item">
          <span className="label">
            Match Score <strong>{candidate.match_score}/100</strong>
          </span>
          <div className="score-bar">
            <div className="score-fill match" style={{ width: `${candidate.match_score}%` }} />
          </div>
        </div>
        <div className="score-item">
          <span className="label">
            Interest Score <strong>{candidate.interest_score}/100</strong>
          </span>
          <div className="score-bar">
            <div className="score-fill interest" style={{ width: `${candidate.interest_score}%` }} />
          </div>
        </div>
      </div>

      <div className="candidate-details">
        <div className="detail">
          <strong>Experience:</strong>
          <span>{candidate.experience_years} years</span>
        </div>
        <div className="detail">
          <strong>Skills:</strong>
          <div className="skill-tags">
            {candidate.skills.slice(0, 8).map((skill, idx) => (
              <span key={idx} className="skill-tag">
                {skill}
              </span>
            ))}
            {candidate.skills.length > 8 && (
              <span className="skill-tag">+{candidate.skills.length - 8} more</span>
            )}
          </div>
        </div>
      </div>

      <div className="breakdown-section">
        <div className="breakdown">
          <h4>Match Analysis</h4>
          <div className="score-factors">
            <div className="factor">
              <span>Skill Match:</span>
              <span className="value">{candidate.match_breakdown.skill_match_score}/100</span>
            </div>
            <div className="factor">
              <span>Experience:</span>
              <span className="value">{candidate.match_breakdown.experience_alignment}/100</span>
            </div>
            <div className="factor">
              <span>Profile Fit:</span>
              <span className="value">{candidate.match_breakdown.profile_fit}/100</span>
            </div>
            <div className="factor">
              <span>Cultural Fit:</span>
              <span className="value">{candidate.match_breakdown.cultural_fit}/100</span>
            </div>
          </div>
          {candidate.match_breakdown.strengths.length > 0 && (
            <div className="strengths">
              <strong>Strengths:</strong>
              <ul>
                {candidate.match_breakdown.strengths.map((strength, idx) => (
                  <li key={idx}>✓ {strength}</li>
                ))}
              </ul>
            </div>
          )}
          {candidate.match_breakdown.gaps.length > 0 && (
            <div className="gaps">
              <strong>Gaps:</strong>
              <ul>
                {candidate.match_breakdown.gaps.map((gap, idx) => (
                  <li key={idx}>⚠ {gap}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        <div className="breakdown">
          <h4>Interest Assessment</h4>
          <div className="interest-info">
            <div className="interest-item">
              <span>Likelihood:</span>
              <span
                className="likelihood-badge"
                style={{ color: getInterestColor(candidate.interest_breakdown.likelihood) }}
              >
                {candidate.interest_breakdown.likelihood.toUpperCase()}
              </span>
            </div>
          </div>
          {candidate.interest_breakdown.positive_signals.length > 0 && (
            <div className="signals">
              <strong>Positive Signals:</strong>
              <ul>
                {candidate.interest_breakdown.positive_signals.map((signal, idx) => (
                  <li key={idx}>✅ {signal}</li>
                ))}
              </ul>
            </div>
          )}
          {candidate.interest_breakdown.concerns.length > 0 && (
            <div className="concerns">
              <strong>Concerns:</strong>
              <ul>
                {candidate.interest_breakdown.concerns.map((concern, idx) => (
                  <li key={idx}>⚠️ {concern}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      <button className="expand-btn" onClick={() => setExpanded(!expanded)}>
        {expanded ? '▼ Hide Conversation' : '▶ Show Conversation'}
      </button>

      {expanded && (
        <div className="conversation">
          <h4>Simulated Recruiter Outreach:</h4>
          {candidate.conversation.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <span className="role">{msg.role === 'recruiter' ? '👨‍💼 Recruiter' : '👤 Candidate'}:</span>
              <span className="text">{msg.text}</span>
              {msg.sentiment && <span className="sentiment">({msg.sentiment})</span>}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
