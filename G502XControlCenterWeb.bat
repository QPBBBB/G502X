@echo off
setlocal
title G502 X Control Center Web
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Python environment is missing. Follow Quick Start in README.md first.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" "module\Backend\Src\Server.py" --open-browser
if errorlevel 1 (
    echo Unable to start. Check the message above. Port 8765 may already be in use.
    pause
    exit /b 1
)
