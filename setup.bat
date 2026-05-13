@echo off
chcp 65001 > nul

echo ==========================
echo Clip Saver Setup
echo ==========================

cd /d "%~dp0"

echo.
echo [1/4] Python 확인 중...
py --version

if errorlevel 1 (
    echo.
    echo Python이 설치되어 있지 않습니다.
    echo 아래 주소에서 Python 설치 후 다시 실행하세요.
    echo https://www.python.org/downloads/
    pause
    exit
)

echo.
echo [2/4] 가상환경 생성 중...
py -m venv venv

echo.
echo [3/4] 가상환경 활성화 중...
call venv\Scripts\activate.bat

echo.
echo [4/4] 라이브러리 설치 중...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ==========================
echo 설치 완료!
echo clipSaver.bat 실행해서 사용하세요.
echo ==========================

pause