#!/bin/bash
# Android Project Rebuilder - 실행 스크립트

PORT=8090

echo "======================================"
echo "Android Project Rebuilder"
echo "======================================"
echo ""

# Python 버전 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3가 설치되어 있지 않습니다."
    echo "   Python 3.11 이상을 설치해주세요."
    exit 1
fi

echo "✅ Python version: $(python3 --version)"
echo ""

# 기존 서버 프로세스 확인 및 종료
echo "🔍 기존 서버 프로세스 확인 중..."
EXISTING_PID=$(lsof -ti:$PORT)

if [ ! -z "$EXISTING_PID" ]; then
    echo "⚠️  포트 $PORT에서 실행 중인 프로세스 발견: PID $EXISTING_PID"
    echo "   기존 서버를 종료합니다..."
    kill -9 $EXISTING_PID 2>/dev/null
    sleep 2
    echo "✅ 기존 서버 종료 완료"
    echo ""
else
    echo "✅ 포트 $PORT 사용 가능"
    echo ""
fi

# 가상환경 확인 및 생성
if [ ! -d "venv" ]; then
    echo "📦 가상환경 생성 중..."
    python3 -m venv venv
    echo "✅ 가상환경 생성 완료"
    echo ""
fi

# 가상환경 활성화
echo "🔧 가상환경 활성화 중..."
source venv/bin/activate

# 의존성 설치
echo "📥 필요한 패키지 설치 중..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ 패키지 설치 완료"

echo ""
echo "======================================"
echo "🚀 서버 시작 중..."
echo "======================================"
echo ""
echo "✅ 서버 주소: http://localhost:$PORT"
echo ""
echo "📖 사용 방법:"
echo "   1. 브라우저에서 위 주소로 접속하세요"
echo "   2. Android 프로젝트 ZIP 파일을 업로드하세요"
echo "   3. 새 패키지명과 앱 이름을 입력하세요"
echo "   4. '🚀 프로젝트 리빌드 시작' 버튼을 클릭하세요"
echo ""
echo "⚠️  서버를 중지하려면 Ctrl+C를 누르세요"
echo ""
echo "======================================"
echo ""

# FastAPI 실행
uvicorn backend.main:app --host 0.0.0.0 --port $PORT --reload
