# Android Project Rebuilder

자동으로 Android 프로젝트의 패키지명, 앱 이름, 버전, Firebase 설정, 아이콘, BASE_URL을 변경하는 웹 기반 도구입니다.

## 주요 기능

- ✅ **패키지명 자동 변경**
  - `applicationId` (build.gradle)
  - 소스 파일 내 `package` 선언
  - 디렉토리 구조 자동 변경
  - AndroidManifest.xml 수정

- ✅ **앱 이름 변경**
  - `res/values*/strings.xml` 내 `app_name` 수정
  - AndroidManifest.xml 정규화

- ✅ **버전 초기화**
  - versionCode = 1
  - versionName = "1.0.0"

- ✅ **Firebase 설정 교체** (선택)
  - google-services.json 자동 교체

- ✅ **앱 아이콘 교체** (선택)
  - mipmap-* 폴더의 모든 아이콘 일괄 교체

- ✅ **BASE_URL 변경** (선택)
  - build.gradle의 buildConfigField
  - Kotlin/Java 상수
  - strings.xml

- ✅ **빌드 아티팩트 자동 삭제**
  - build/, .gradle/, .idea/, outputs/ 폴더 제거

## 프로젝트 구조

```
android-project-rebuilder/
├── backend/
│   ├── main.py              # FastAPI 엔드포인트
│   ├── processor.py         # 전체 파이프라인
│   └── utils/
│       ├── zip_tools.py     # ZIP 압축/해제
│       ├── cleanup.py       # 빌드 아티팩트 정리
│       ├── file_replace.py  # 패키지/앱이름/버전 교체
│       ├── firebase.py      # Firebase 설정 교체
│       ├── icon_replace.py  # 아이콘 교체
│       └── baseurl_replace.py  # BASE_URL 교체
├── frontend/
│   └── index.html           # 웹 UI
├── requirements.txt
├── Dockerfile
├── run.sh
└── README.md
```

## 설치 및 실행

### 로컬 실행 (권장)

#### 사전 요구사항
- Python 3.11 이상
- pip

#### 실행 단계

1. **프로젝트 디렉토리로 이동**
```bash
cd /path/to/AndroidChangePackageName
```

2. **실행 스크립트 실행**
```bash
./run.sh
```

스크립트가 자동으로:
- 가상환경 생성
- 의존성 설치
- FastAPI 서버 시작 (포트 8090)

3. **브라우저에서 접속**
```
http://localhost:8090
```

#### 수동 실행
```bash
# 가상환경 생성
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 서버 시작
uvicorn backend.main:app --host 0.0.0.0 --port 8090 --reload
```

### Docker 실행 (선택사항)

Docker를 사용하고 싶다면:

1. **Docker 이미지 빌드**
```bash
docker build -t android-rebuilder .
```

2. **컨테이너 실행**
```bash
docker run -p 8090:8090 android-rebuilder
```

3. **브라우저에서 접속**
```
http://localhost:8090
```

## 사용 방법

### 🎯 빠른 시작

1. 터미널에서 실행:
   ```bash
   ./run.sh
   ```

2. 브라우저에서 접속:
   ```
   http://localhost:8090
   ```

3. 화면의 안내에 따라 진행!

### 📖 상세 가이드

**개발을 전혀 모르는 분도 쉽게 사용할 수 있도록 작성된 상세 가이드:**

👉 **[USAGE_GUIDE.md](./USAGE_GUIDE.md)** 를 참고하세요!

가이드에 포함된 내용:
- ✅ 단계별 스크린샷과 설명
- ✅ 자주 묻는 질문 (FAQ)
- ✅ 문제 해결 방법
- ✅ 패키지명 형식 예시
- ✅ 오류 대응 방법

## API 엔드포인트

### POST /process
Android 프로젝트 리빌드 처리

**Request (multipart/form-data):**
```
project_zip: File (필수)
new_package: String (필수)
new_app_name: String (필수)
google_services: File (선택)
app_icon: File (선택)
new_base_url: String (선택)
```

**Response:**
```
Content-Type: application/zip
rebuilt_project.zip
```

### GET /health
헬스 체크

**Response:**
```json
{
  "status": "ok",
  "message": "Android Project Rebuilder is running"
}
```

### GET /api/info
API 정보 조회

**Response:**
```json
{
  "name": "Android Project Rebuilder",
  "version": "1.0.0",
  "features": [...]
}
```

## 처리 단계

1. **ZIP 압축 해제**: 업로드된 프로젝트 압축 해제
2. **빌드 아티팩트 정리**: build/, .gradle/ 등 불필요한 폴더 삭제
3. **App 모듈 탐지**: app 모듈 자동 인식
4. **기존 패키지명 탐지**: build.gradle에서 applicationId 추출
5. **패키지명 교체**:
   - build.gradle applicationId
   - 소스 파일 package 선언
   - 디렉토리 구조 변경
   - AndroidManifest.xml
6. **앱 이름 교체**: strings.xml의 app_name 수정
7. **버전 초기화**: versionCode=1, versionName=1.0.0
8. **Firebase 설정 교체**: google-services.json 교체 (선택)
9. **앱 아이콘 교체**: mipmap-* 폴더 아이콘 일괄 교체 (선택)
10. **BASE_URL 교체**: Config 파일 내 URL 변경 (선택)
11. **결과 ZIP 생성**: rebuilt_project.zip + 로그 파일 포함

## 기술 스택

### Backend
- **Python 3.11+**
- **FastAPI**: 고성능 웹 프레임워크
- **uvicorn**: ASGI 서버

### Frontend
- **Vanilla HTML/CSS/JavaScript**: 의존성 없는 단일 페이지

### Utilities
- **zipfile**: ZIP 압축/해제
- **shutil**: 파일 작업
- **re**: 정규식 처리
- **pathlib**: 경로 관리

## 주의 사항

### 지원되는 프로젝트 구조
- 표준 Android Gradle 프로젝트
- app 모듈 또는 단일 모듈 프로젝트
- Groovy 또는 Kotlin DSL (build.gradle / build.gradle.kts)

### 제외되는 파일/폴더
- build/
- .gradle/
- .idea/
- outputs/
- .DS_Store

### 버전 고정 규칙
- versionCode는 항상 1
- versionName은 항상 "1.0.0"

### 인코딩
- 모든 파일은 UTF-8 기준으로 처리
- 인코딩 실패 시 자동으로 `errors="ignore"` 처리

## 예상 오류 및 해결법

### 1. "build.gradle not found"
**원인**: 프로젝트 구조가 비표준
**해결**: app 모듈이 있는지, build.gradle(.kts) 파일이 있는지 확인

### 2. "Could not detect applicationId"
**원인**: build.gradle에 applicationId가 없음
**해결**: 수동으로 패키지명 추가 후 재시도

### 3. "No mipmap directories found"
**원인**: res/mipmap-* 폴더가 없음
**해결**: 아이콘 교체 기능은 건너뛰고 수동으로 아이콘 추가

### 4. "BASE_URL definitions not found"
**원인**: 프로젝트에 BASE_URL 정의가 없음
**해결**: 정상 동작, 필요 시 수동으로 BASE_URL 추가

## 라이선스

MIT License

## 기여

이슈 및 PR 환영합니다.

## 작성자

Senior Python & Frontend Developer
Android Automation Tool Specialist

---

**문의**: 이슈 탭을 통해 버그 리포트 및 기능 제안 가능합니다.
