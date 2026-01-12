@echo off
REM Fraud Detection System - Startup Script
REM This script starts both the Flask backend and Streamlit frontend

echo.
echo ========================================
echo Fraud Detection System - Startup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo Checking dependencies...
pip show flask streamlit scikit-learn >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo ✅ Dependencies are installed
echo.
echo Starting Fraud Detection System...
echo.
echo 1. Starting Flask Backend (Port 5000)...
echo 2. Starting Streamlit Frontend (Port 8501)...
echo.
echo ========================================
echo.

REM Start Flask backend in a new window
echo Launching Flask backend...
start cmd /k "python app.py"

REM Wait a moment for Flask to start
timeout /t 2 /nobreak

REM Start Streamlit frontend in a new window
echo Launching Streamlit frontend...
start cmd /k "streamlit run streamlit_app.py"

echo.
echo ========================================
echo System Started!
echo ========================================
echo.
echo Backend API:  http://localhost:5000
echo Frontend URL: http://localhost:8501
echo.
echo Tip: Use the provided test_api.py to verify everything is working
echo Command: python test_api.py
echo.
echo Press Ctrl+C in any window to stop that service
echo Close both windows to fully stop the system
echo.
pause
