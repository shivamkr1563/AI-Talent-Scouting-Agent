import React from 'react'
import './PhaseLog.css'

interface Phase {
  id: string
  name: string
  status: 'pending' | 'in-progress' | 'completed' | 'error'
}

interface PhaseLogProps {
  phases: Phase[]
}

export const PhaseLog: React.FC<PhaseLogProps> = ({ phases }) => {
  return (
    <div className="phase-log">
      <h3>📋 Processing Phases</h3>
      <div className="phases-list">
        {phases.map((phase) => (
          <div key={phase.id} className={`phase-item status-${phase.status}`}>
            <span className="phase-icon">
              {phase.status === 'completed' && '✅'}
              {phase.status === 'in-progress' && '⏳'}
              {phase.status === 'pending' && '⏸️'}
              {phase.status === 'error' && '❌'}
            </span>
            <span className="phase-name">{phase.name}</span>
            <span className="phase-status">{phase.status}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
