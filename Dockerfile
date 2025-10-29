# Android Project Rebuilder - Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 필요한 시스템 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# 포트 노출
EXPOSE 8090

# 실행 명령
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8090"]
