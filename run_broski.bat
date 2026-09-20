@echo off
cd /d "%~dp0"

echo Starting Broski server...
start /B python app.py

timeout /t 3 /nobreak >nul

echo Opening Broski...
start "" "http://127.0.0.1:5000"

echo.
echo Broski is running.
echo Keep this window open while using Broski.
pause