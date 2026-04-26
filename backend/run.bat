@echo off
REM Run the production backend
REM This script properly sets up the environment and runs the backend

echo.
echo 🚀 Starting AI Talent Scouting Backend (v2.0 Production)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Set working directory
cd /d "%~dp0"

echo Working Directory: %CD%
echo Starting uvicorn server on http://127.0.0.1:8000
echo API Docs available at http://127.0.0.1:8000/docs
echo Press Ctrl+C to stop the server
echo.

REM Run the production backend
python -m uvicorn main_v2:app --reload --port 8000 --host 127.0.0.1
