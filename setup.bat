@echo off
echo Setting up WhisperWriter...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or newer from https://python.org
    pause
    exit /b 1
)

echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo This might be due to Python version compatibility issues.
    echo WhisperWriter works best with Python 3.11
    pause
    exit /b 1
)

echo.
echo ✅ Setup complete!
echo.
echo To run WhisperWriter:
echo   1. Double-click start_whisperwriter.bat
echo   OR
echo   2. Run: .\venv\Scripts\activate then python run.py
echo.
pause 