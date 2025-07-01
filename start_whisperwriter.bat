@echo off
echo Starting WhisperWriter...
echo.

REM Check if we're already in a virtual environment
if defined VIRTUAL_ENV (
    echo Virtual environment already active: %VIRTUAL_ENV%
    echo.
) else (
    echo Activating virtual environment...
    if exist "venv\Scripts\activate.bat" (
        call venv\Scripts\activate.bat
        echo Virtual environment activated.
        echo.
    ) else (
        echo ERROR: Virtual environment not found at venv\Scripts\activate.bat
        echo Please make sure the virtual environment exists.
        pause
        exit /b 1
    )
)

REM Run WhisperWriter
echo Running WhisperWriter...
python run.py

REM Keep the window open if there's an error
if errorlevel 1 (
    echo.
    echo WhisperWriter exited with an error.
    pause
) 