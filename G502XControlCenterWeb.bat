@echo off
setlocal
title G502 X Control Center Web
cd /d "%~dp0"
if not exist "Python39\python.exe" (
    echo Bundled Python39 is missing. Restore the complete project folder.
    pause
    exit /b 1
)
"Python39\python.exe" "Module\Backend\Src\Server.py" --open-browser
if errorlevel 1 (
    echo Unable to start. Check the message above. Port 8765 may already be in use.
    pause
    exit /b 1
)
