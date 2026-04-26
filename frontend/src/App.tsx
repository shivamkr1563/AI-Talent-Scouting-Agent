import   { useState } from 'react'
import { runAgent, AgentResult } from './api/agent'
import { JDInput } from './components/JDInput'
import { PhaseLog } from './components/PhaseLog'
import { Shortlist } from './components/Shortlist'
import './App.css'

interface Phase {
  id: string
  name: string
  status: 'pending' | 'in-progress' | 'completed' | 'error'
}

function App() {
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<AgentResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [phases, setPhases] = useState<Phase[]>([
    { id: 'parse', name: 'Parse Job Description', status: 'pending' },
    { id: 'score', name: 'Score Candidates', status: 'pending' },
    { id: 'outreach', name: 'Simulate Outreach', status: 'pending' },
    { id: 'rank', name: 'Rank Results', status: 'pending' },
  ])

  const updatePhase = (phaseId: string, status: Phase['status']) => {
    setPhases((prev) =>
      prev.map((p) => (p.id === phaseId ? { ...p, status } : p))
    )
  }

  const handleSubmit = async (jobDescription: string) => {
    setIsLoading(true)
    setError(null)
    setResult(null)
    setPhases(phases.map((p) => ({ ...p, status: 'pending' as const })))

    try {
      // Simulate phase progression
      updatePhase('parse', 'in-progress')
      await new Promise((resolve) => setTimeout(resolve, 500))
      updatePhase('parse', 'completed')

      updatePhase('score', 'in-progress')
      await new Promise((resolve) => setTimeout(resolve, 500))
      updatePhase('score', 'completed')

      updatePhase('outreach', 'in-progress')
      await new Promise((resolve) => setTimeout(resolve, 500))
      updatePhase('outreach', 'completed')

      updatePhase('rank', 'in-progress')

      // Call the API
      const response = await runAgent(jobDescription)

      updatePhase('rank', 'completed')
      setResult(response)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'An error occurred while processing the job description'
      )
      phases.forEach((p) => {
        if (p.status === 'in-progress') {
          updatePhase(p.id, 'error')
        }
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🤖 AI Talent Scouting Agent</h1>
        <p>Intelligent candidate matching with Gemini AI</p>
      </header>

      <main className="app-main">
        <div className="container">
          <JDInput onSubmit={handleSubmit} isLoading={isLoading} />

          {isLoading && <PhaseLog phases={phases} />}

          {error && <div className="error-message">⚠️ {error}</div>}

          {result && <Shortlist parsedJD={result.parsed_jd} candidates={result.candidates} />}

          {!result && !isLoading && !error && (
            <div className="welcome-message">
              <p>👋 Welcome! Paste a job description above to get started.</p>
              <p>The AI agent will analyze the JD and rank candidates from your database.</p>
            </div>
          )}
        </div>
      </main>

      <footer className="app-footer">
        <p>© 2026 AI Talent Scouting. Powered by Gemini AI & Vite React.</p>
      </footer>
    </div>
  )
}

export default App
