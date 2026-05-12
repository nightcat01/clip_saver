@echo off
chcp 65001 >nul

echo Installing requirements...
pip install -r requirements.txt

echo.
echo Done.
pause
