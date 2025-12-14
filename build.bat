@echo off
echo AoE4 Villager Reminder - Build Script
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH!
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create sound file if it doesn't exist
if not exist "assets\sounds\villager.wav" (
    echo Creating sound file...
    python create_sound.py
)

REM Build executable
echo Building executable...
pyinstaller build.spec --clean

echo.
echo Build complete! Check the 'dist' folder.
pause


