@echo off
"%~dp0.venv\Scripts\python.exe" "%~dp0stt.py" %*
exit /b %errorlevel%
