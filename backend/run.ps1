# Run the production backend
# This script properly sets up the environment and runs the backend

Write-Host "🚀 Starting AI Talent Scouting Backend (v2.0 Production)" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green

# Set working directory
$backendPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $backendPath

Write-Host "Working Directory: $(Get-Location)" -ForegroundColor Cyan
Write-Host "Starting uvicorn server on http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "API Docs available at http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run the production backend
python -m uvicorn main_v2:app --reload --port 8000 --host 127.0.0.1
