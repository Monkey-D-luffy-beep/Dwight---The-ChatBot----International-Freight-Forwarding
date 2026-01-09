@echo off
echo ========================================
echo    PROJECT DWIGHT - Starting Servers
echo ========================================
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0start_dwight.ps1"
pause
