import React, { useState } from 'react'
import './JDInput.css'

interface JDInputProps {
  onSubmit: (jobDescription: string) => void
  isLoading: boolean
}

export const JDInput: React.FC<JDInputProps> = ({ onSubmit, isLoading }) => {
  const [jd, setJd] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (jd.trim()) {
      onSubmit(jd)
    }
  }

  return (
    <div className="jd-input-container">
      <form onSubmit={handleSubmit} className="jd-form">
        <h2>📝 Job Description</h2>
        <textarea
          value={jd}
          onChange={(e) => setJd(e.target.value)}
          placeholder="Paste your job description here..."
          className="jd-textarea"
          disabled={isLoading}
        />
        <button type="submit" disabled={!jd.trim() || isLoading} className="submit-btn">
          {isLoading ? '⏳ Processing...' : '🚀 Run Agent'}
        </button>
      </form>
    </div>
  )
}
