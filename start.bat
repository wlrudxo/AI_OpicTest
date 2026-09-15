@echo off
cd /d "%~dp0"
echo Open http://127.0.0.1:8765 in Chrome or Edge after the server starts.
"%~dp0.venv\Scripts\python.exe" "%~dp0app.py"
pause
