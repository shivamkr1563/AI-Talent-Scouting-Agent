# Local Setup Instructions - AI Talent Scouting Agent

## ⚡ Quick Start (5 minutes)

### 1. Prerequisites
- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)

### 2. Clone & Navigate

```bash
git clone <YOUR_REPO_URL>
cd talent-scout
```

### 3. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Setup Frontend

```bash
cd ../frontend

# Install npm dependencies
npm install
```

### 5. Start the Application

**Terminal 1 - Backend (from `backend/` directory):**
```bash
python -m uvicorn main_v2:app --reload --port 8001
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete
```

**Terminal 2 - Frontend (from `frontend/` directory):**
```bash
npm run dev
```

You should see:
```
  ➜  Local:   http://127.0.0.1:5174/
```

### 6. Access the Application

Open your browser to: **http://127.0.0.1:5174/**

---

## 🎯 Test the System

### Option A: Web UI (Easiest)

1. Open http://127.0.0.1:5174/
2. Paste a job description:
   ```
   Senior Backend Engineer - We're looking for someone with 5+ years Python experience, 
   strong FastAPI knowledge, and PostgreSQL expertise. Remote or Bangalore.
   ```
3. Click "Find Talent"
4. View ranked candidates with scoring breakdown

### Option B: Direct API (Command Line)

**Windows PowerShell:**
```powershell
$body = @{
    job_description = "Senior Backend Engineer with 5+ years Python, FastAPI, PostgreSQL"
    max_candidates = 3
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/v2/run" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body `
    -UseBasicParsing | Select-Object -ExpandProperty Content
```

**macOS/Linux (curl):**
```bash
curl -X POST http://127.0.0.1:8001/api/v2/run \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Senior Backend Engineer with 5+ years Python",
    "max_candidates": 3
  }'
```

---

## 🐳 Docker Setup (Optional)

If you prefer Docker:

```bash
# Build images
docker-compose build

# Run services
docker-compose up

# Access at http://localhost:5174
```

---

## 🔌 Configuration

### Environment Variables (Optional)

Create `backend/.env`:
```env
# Port configuration
PORT=8001

# Optional: OpenRouter API (for real AI responses vs mock)
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# CORS settings
ALLOWED_ORIGINS=http://127.0.0.1:5174,http://localhost:5174
```

**Note:** The system works perfectly without an API key using mock data for testing.

---

## ✅ Verify Installation

### Health Check

```bash
curl http://127.0.0.1:8001/health
```

Should return:
```json
{
  "status": "healthy",
  "version": "2.0-production",
  "timestamp": "2026-04-26T10:00:00Z"
}
```

### Frontend Check

Backend logs should show:
```
CORS enabled for: http://127.0.0.1:5174
```

And frontend should show no connection errors in browser console.

---

## 📁 Project Structure

```
talent-scout/
├── backend/
│   ├── main_v2.py              # FastAPI entry point
│   ├── requirements.txt         # Python dependencies
│   ├── .env                    # Configuration (optional)
│   ├── models/
│   │   └── schemas_v2.py       # Pydantic models
│   ├── routers/
│   │   └── agent_v2.py         # Main workflow orchestrator
│   ├── services/
│   │   ├── candidate_matcher.py
│   │   ├── jd_parser.py
│   │   └── mock_services.py    # Fallback implementation
│   └── data/
│       └── mock_candidates.json # Test data
│
├── frontend/
│   ├── package.json            # npm configuration
│   ├── vite.config.ts          # Vite setup
│   ├── index.html              # Entry point
│   └── src/
│       ├── App.tsx             # Main component
│       ├── api/
│       │   └── agent.ts        # Backend API client
│       └── components/
│           ├── JDInput.tsx     # Job description input
│           ├── Shortlist.tsx   # Results display
│           └── CandidateCard.tsx # Individual candidate
│
├── README.md                   # Main documentation
├── SETUP_INSTRUCTIONS.md       # This file
├── ARCHITECTURE.md             # System design & scoring
├── DEMO_SCRIPT.md             # Video script
└── docker-compose.yml          # Docker configuration
```

---

## 🚨 Troubleshooting

### Backend won't start

```bash
# Check if port 8001 is in use
# Windows:
netstat -ano | findstr "8001"

# Kill process on port 8001 (Windows):
taskkill /PID <PID> /F

# Try different port:
python -m uvicorn main_v2:app --port 8002
```

### Frontend won't connect to backend

1. Verify backend is running: `http://127.0.0.1:8001/health`
2. Check browser console for CORS errors
3. Ensure correct backend URL in `frontend/src/api/agent.ts`

### "ModuleNotFoundError"

```bash
# Verify venv is activated
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Reinstall packages
pip install -r requirements.txt
```

### npm dependencies error

```bash
# Clear npm cache and reinstall
rm -r node_modules package-lock.json
npm install
```

---

## 📊 Next Steps

1. **Explore the UI** - Submit job descriptions and view results
2. **Read ARCHITECTURE.md** - Understand the scoring logic
3. **Check SAMPLE_INPUTS_OUTPUTS.md** - See example workflows
4. **Review code** - Look at `routers/agent_v2.py` for main logic
5. **Customize** - Modify scoring weights in `services/mock_services.py`

---

## 📞 Support

- Check backend logs: Terminal running FastAPI
- Check frontend logs: Browser console (F12)
- Database logs: `backend/logs/` directory (if exists)

For issues, check existing code comments in:
- `backend/main_v2.py` - Application setup
- `backend/routers/agent_v2.py` - Core workflow
- `frontend/src/App.tsx` - Frontend structure
