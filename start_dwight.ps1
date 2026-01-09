# ============================================
# Project Dwight - Server Startup Script
# ============================================
# Double-click START_DWIGHT.bat or run: .\start_dwight.ps1
# ============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   PROJECT DWIGHT - Starting Servers   " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kill any existing Python processes on our ports
Write-Host "[1/4] Cleaning up old processes..." -ForegroundColor Yellow
Get-Job | Stop-Job -ErrorAction SilentlyContinue
Get-Job | Remove-Job -ErrorAction SilentlyContinue
Get-Process -Name "python" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Set working directory
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

# Start Backend Server as background job
Write-Host "[2/4] Starting Backend (FastAPI + Groq)..." -ForegroundColor Yellow
Start-Job -Name "DwightBackend" -ScriptBlock {
    Set-Location $using:projectRoot\backend
    & "$using:projectRoot\backend\venv\Scripts\python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8000
} | Out-Null

Start-Sleep -Seconds 6

# Start Frontend Server
Write-Host "[3/4] Starting Frontend (HTTP Server)..." -ForegroundColor Yellow
Start-Process -FilePath "$projectRoot\backend\venv\Scripts\python.exe" `
    -ArgumentList "-m", "http.server", "3000", "--directory", "$projectRoot\frontend" `
    -WindowStyle Hidden

Start-Sleep -Seconds 2

# Test backend health
Write-Host "[4/4] Verifying servers..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -TimeoutSec 5
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "   SERVERS STARTED SUCCESSFULLY!       " -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Backend API:  http://127.0.0.1:8000" -ForegroundColor White
    Write-Host "  Frontend UI:  http://127.0.0.1:3000" -ForegroundColor White
    Write-Host "  Health Check: $($health.status)" -ForegroundColor White
    Write-Host ""
    Write-Host "  LLM Provider: Groq (llama-3.1-8b-instant)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Press any key to open the chat interface..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    Start-Process "http://127.0.0.1:3000"
} catch {
    Write-Host ""
    Write-Host "WARNING: Backend may still be starting..." -ForegroundColor Yellow
    Write-Host "Try opening http://127.0.0.1:3000 in a few seconds" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Servers running in background. Close this window when done." -ForegroundColor Gray
Write-Host "To stop servers: Get-Process python | Stop-Process" -ForegroundColor Gray
Write-Host ""
