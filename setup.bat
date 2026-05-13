@echo off

echo ==========================
echo Clip Saver Setup
echo ==========================

cd /d "%~dp0"

echo.
echo [1/4] Checking Python...
py --version

if errorlevel 1 (
    echo.
    echo Python is not installed.
    echo Please install Python from the link below and run this file again.
    echo https://www.python.org/downloads/
    pause
    exit
)

echo.
echo [2/4] Creating virtual environment...
py -m venv venv

echo.
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [4/4] Installing required libraries...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ==========================
echo Setup completed!
echo Run clipSaver.bat to start the program.
echo ==========================

pause