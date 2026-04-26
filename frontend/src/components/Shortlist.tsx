import React from 'react'
import { CandidateResult, ParsedJD } from '../api/agent'
import { CandidateCard } from './CandidateCard'
import './Shortlist.css'

interface ShortlistProps {
  parsedJD: ParsedJD
  candidates: CandidateResult[]
}

export const Shortlist: React.FC<ShortlistProps> = ({ parsedJD, candidates }) => {
  // Sort candidates by rank (if available) or combined_score (descending)
  const sortedCandidates = [...candidates].sort((a, b) => a.rank - b.rank)

  return (
    <div className="shortlist">
      <div className="jd-summary">
        <h2>📊 Job Description Summary</h2>
        <div className="jd-details">
          <div className="detail">
            <strong>Title:</strong>
            <span>{parsedJD.title}</span>
          </div>
          <div className="detail">
            <strong>Company:</strong>
            <span>{parsedJD.company || 'N/A'}</span>
          </div>
          <div className="detail">
            <strong>Experience Required:</strong>
            <span>{parsedJD.experience_years}+ years</span>
          </div>
          <div className="detail">
            <strong>Seniority Level:</strong>
            <span className="seniority-badge">{parsedJD.seniority_level}</span>
          </div>
          <div className="detail">
            <strong>Domain:</strong>
            <span>{parsedJD.domain}</span>
          </div>
          <div className="detail">
            <strong>Location:</strong>
            <span>{parsedJD.location}</span>
          </div>
          <div className="detail full-width">
            <strong>Must-Have Skills:</strong>
            <div className="skill-tags">
              {parsedJD.must_have_skills.map((skill, idx) => (
                <span key={idx} className="skill-tag required">
                  {skill}
                </span>
              ))}
            </div>
          </div>
          {parsedJD.nice_to_have_skills.length > 0 && (
            <div className="detail full-width">
              <strong>Nice-to-Have Skills:</strong>
              <div className="skill-tags">
                {parsedJD.nice_to_have_skills.map((skill, idx) => (
                  <span key={idx} className="skill-tag optional">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="candidates-section">
        <h2>👥 Top Candidates</h2>
        <div className="candidates-count">
          Found <strong>{candidates.length}</strong> candidate{candidates.length !== 1 ? 's' : ''} matching this role
        </div>
        <div className="candidates-list">
          {sortedCandidates.map((candidate, idx) => (
            <CandidateCard key={idx} candidate={candidate} />
          ))}
        </div>
      </div>
    </div>
  )
}
