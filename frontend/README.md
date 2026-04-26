# 🎨 Frontend - AI Talent Scouting

A modern React + TypeScript + Vite frontend for the AI Talent Scouting application.

## 🚀 Quick Start

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The frontend will start on `http://localhost:5173` and automatically proxy API requests to the backend on `http://localhost:8000`.

### Build

```bash
npm run build
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── api/                    # API client
│   │   ├── agent.ts           # Gemini agent API calls
│   │   └── index.ts           # Exports
│   ├── components/            # React components
│   │   ├── JDInput.tsx        # Job description input form
│   │   ├── JDInput.css
│   │   ├── CandidateCard.tsx  # Individual candidate display
│   │   ├── CandidateCard.css
│   │   ├── PhaseLog.tsx       # Processing phases tracker
│   │   ├── PhaseLog.css
│   │   ├── Shortlist.tsx      # Results display
│   │   ├── Shortlist.css
│   │   └── index.ts           # Exports
│   ├── App.tsx                # Main app component
│   ├── App.css                # App styles
│   ├── main.tsx               # Entry point
│   ├── index.css              # Global styles
├── index.html                 # HTML template
├── vite.config.ts             # Vite configuration
├── tsconfig.json              # TypeScript config
├── package.json               # Dependencies
└── README.md                  # This file
```

## 🎯 Components

### JDInput
- Text area for job description input
- Submit button to trigger agent processing
- Loading state management

### PhaseLog
- Shows processing progress
- 4 phases: Parse JD → Score Candidates → Simulate Outreach → Rank Results
- Visual status indicators (pending, in-progress, completed, error)

### CandidateCard
- Displays individual candidate details
- Match score and interest score with progress bars
- Skills and match/interest reasons
- Expandable conversation simulator results

### Shortlist
- Shows parsed job description summary
- Lists all matched candidates ranked by combined score
- Overall score = (match_score * 0.5) + (interest_score * 0.5)

## 🔌 API Integration

The frontend communicates with the backend via axios:

```typescript
POST /api/run
{
  "job_description": "Senior Backend Engineer..."
}

Response:
{
  "parsed_jd": {...},
  "candidates": [...]
}
```

The Vite dev server automatically proxies `/api/*` requests to `http://localhost:8000`.

## 🎨 Styling

- Responsive CSS with Flexbox and Grid
- Mobile-friendly design
- Color scheme:
  - Purple gradient headers (#667eea, #764ba2)
  - Green for match scores (#4CAF50)
  - Blue for interest scores (#2196F3)
  - Light backgrounds for accessibility

## 🔧 Technologies

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Fast build tool & dev server
- **Axios** - HTTP client
- **CSS3** - Styling

## 📦 Dependencies

```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "axios": "^1.6.0"
}
```

## 🚀 Deployment

Build for production:

```bash
npm run build
```

This generates a `dist/` folder ready for deployment.

## 📝 Features

- ✅ Job description input with real-time validation
- ✅ Multi-phase processing visualization
- ✅ Candidate ranking by combined scores
- ✅ Expandable conversation simulator results
- ✅ Responsive design for mobile/tablet/desktop
- ✅ Error handling and user feedback
- ✅ Proxy API requests to backend
- ✅ TypeScript for type safety

## 🤝 Contributing

To add new components:

1. Create `src/components/MyComponent.tsx`
2. Create `src/components/MyComponent.css`
3. Export from `src/components/index.ts`
4. Import and use in `App.tsx`

## 📄 License

Part of AI Talent Scouting project © 2026
