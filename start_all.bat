@echo off
REM Start backend
start cmd /k "cd /d %~dp0 && .venv\Scripts\python.exe backend\app.py"
REM Start frontend
start cmd /k "cd /d %~dp0 && npm start --prefix ai-demo-frontend"
