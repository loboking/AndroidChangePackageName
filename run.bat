@echo off
REM ============================================
REM Android Project Rebuilder - Windows Launcher
REM ============================================

echo.
echo ======================================
echo Android Project Rebuilder
echo ======================================
echo.

REM Python 버전 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python이 설치되어 있지 않습니다.
    echo.
    echo Python 3.11 이상을 설치하세요:
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python version:
python --version
echo.

REM 기존 서버 프로세스 종료
echo [INFO] 기존 서버 프로세스 확인 중...
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq uvicorn*" >nul 2>&1
if not errorlevel 1 (
    echo [INFO] 기존 서버 종료 중...
    taskkill /F /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq uvicorn*" >nul 2>&1
    timeout /t 2 /nobreak >nul
)
echo [OK] 포트 8090 사용 가능
echo.

REM 가상환경 생성
if not exist "venv" (
    echo [INFO] 가상환경 생성 중...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] 가상환경 생성 실패
        pause
        exit /b 1
    )
    echo [OK] 가상환경 생성 완료
) else (
    echo [OK] 가상환경 이미 존재
)
echo.

REM 가상환경 활성화
echo [INFO] 가상환경 활성화 중...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] 가상환경 활성화 실패
    pause
    exit /b 1
)
echo.

REM 필요한 패키지 설치
echo [INFO] 필요한 패키지 설치 중...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] 패키지 설치 실패
    pause
    exit /b 1
)
echo [OK] 패키지 설치 완료
echo.

REM 서버 시작
echo ======================================
echo [INFO] 서버 시작 중...
echo ======================================
echo.
echo [OK] 서버 주소: http://localhost:8090
echo.
echo [사용 방법]
echo    1. 브라우저에서 위 주소로 접속하세요
echo    2. Android 프로젝트 ZIP 파일을 업로드하세요
echo    3. 새 패키지명과 앱 이름을 입력하세요
echo    4. '프로젝트 리빌드 시작' 버튼을 클릭하세요
echo.
echo [주의] 서버를 중지하려면 Ctrl+C를 누르세요
echo.
echo ======================================
echo.

REM uvicorn 서버 실행
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8090 --reload

REM 서버 종료 시
echo.
echo [INFO] 서버가 종료되었습니다.
pause
