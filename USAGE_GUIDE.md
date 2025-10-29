# 📖 Android Project Rebuilder 사용 가이드

프로그래밍을 전혀 모르는 분도 쉽게 사용할 수 있는 단계별 가이드입니다.

---

## 🎯 이 프로그램이 하는 일

Android 앱 프로젝트의 다음 항목들을 **자동으로** 변경해줍니다:
- 📦 패키지명 (예: com.example.old → com.example.new)
- 📱 앱 이름 (예: 구앱 → 신앱)
- 🔢 버전 (항상 1.0.0으로 초기화)
- 🔥 Firebase 설정 (선택사항)
- 🖼️ 앱 아이콘 (선택사항)
- 🌐 서버 주소 (BASE_URL, 선택사항)

---

## 📋 시작하기 전 준비물

### 1️⃣ Python 설치 확인

터미널(Mac) 또는 명령 프롬프트(Windows)를 열고 다음 명령어를 입력하세요:

```bash
python3 --version
```

**결과가 "Python 3.11" 이상이면 OK!**

만약 Python이 없다면:
- **Mac**: [python.org](https://www.python.org/downloads/)에서 다운로드
- **Windows**: Microsoft Store에서 "Python 3.11" 검색 후 설치

### 2️⃣ 준비할 파일들

✅ **필수:**
- Android 프로젝트 폴더를 ZIP으로 압축한 파일

📌 **선택 (필요한 경우만):**
- google-services.json (Firebase 사용 시)
- 앱 아이콘 이미지 (PNG 또는 JPG 파일)

---

## 🚀 1단계: 서버 실행하기

### Mac/Linux 사용자

1. **Finder에서 이 프로젝트 폴더 열기**
   - 폴더 이름: `AndroidChangePackageName`

2. **터미널 열기**
   - 방법 1: Finder에서 폴더 우클릭 → "폴더에서 새로운 터미널"
   - 방법 2: 터미널 앱 실행 후 `cd` 명령어로 이동

3. **실행 명령어 입력**
   ```bash
   ./run.sh
   ```

4. **서버가 시작되면 이런 메시지가 보입니다:**
   ```
   ✅ 서버 주소: http://localhost:8090
   ```

### Windows 사용자

1. **이 프로젝트 폴더 열기**
   - 폴더 이름: `AndroidChangePackageName`

2. **명령 프롬프트(cmd) 또는 PowerShell 열기**
   - 폴더 주소창에 `cmd` 입력 후 Enter

3. **Python으로 직접 실행**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8090
   ```

4. **서버 시작 완료!**

---

## 🌐 2단계: 웹 페이지 열기

서버가 실행되면:

1. **웹 브라우저 열기** (Chrome, Safari, Edge 등 아무거나)

2. **주소창에 입력:**
   ```
   http://localhost:8090
   ```

3. **다음과 같은 화면이 나타납니다:**

   ```
   ╔════════════════════════════════════════╗
   ║   Android Project Rebuilder            ║
   ║   자동 패키지명 변경, 앱 이름 수정,    ║
   ║   버전 초기화 도구                      ║
   ╚════════════════════════════════════════╝
   ```

---

## 📝 3단계: 프로젝트 정보 입력하기

### 필수 입력 항목 (반드시 입력)

#### 1️⃣ Android 프로젝트 ZIP
- **"파일 선택"** 버튼 클릭
- Android 프로젝트를 압축한 ZIP 파일 선택
- 예: `MyAndroidApp.zip`

#### 2️⃣ 새 패키지명
- 입력 예시: `com.mycompany.newapp`
- **형식:** 영어 소문자 + 점(.) 으로 구분
- ❌ 틀린 예: `MyApp`, `com.MyApp`, `myapp`
- ✅ 올바른 예: `com.example.myapp`

#### 3️⃣ 새 앱 이름
- 입력 예시: `우리회사앱`
- 한글, 영어, 숫자 모두 가능
- 공백 가능 (예: `My New App`)

---

### 선택 입력 항목 (필요한 경우만)

#### 🔥 google-services.json (Firebase 사용 시)
- Firebase 콘솔에서 다운로드 받은 파일 업로드
- 없으면 비워두세요

#### 🖼️ 앱 아이콘 이미지
- PNG 또는 JPG 파일
- 정사각형 이미지 권장 (512x512 이상)
- 업로드하면 모든 해상도에 자동 적용됩니다

#### 🌐 새 BASE_URL (API 서버 주소)
- 입력 예시: `https://api.mycompany.com`
- 프로젝트에서 서버 주소를 사용하는 경우만 입력
- 모르면 비워두세요

---

## 🎬 4단계: 리빌드 시작

1. **모든 정보를 입력했으면**

2. **"🚀 프로젝트 리빌드 시작" 버튼 클릭**

3. **처리 중 화면:**
   - 진행바가 나타납니다
   - 로그 창에 처리 내역이 실시간으로 표시됩니다

   ```
   프로젝트 업로드 중...
   서버 처리 중...
   ✅ 리빌드 완료!
   ```

4. **완료되면 자동으로 파일이 다운로드됩니다:**
   - 파일명: `rebuilt_project.zip`

---

## 📦 5단계: 결과 확인

### 다운로드된 파일 확인

1. **`rebuilt_project.zip` 파일 압축 해제**

2. **폴더 내부에서 확인할 항목:**

   ✅ **ANDROID_REBUILDER_LOG.txt**
   - 처리 과정 상세 로그
   - 뭐가 바뀌었는지 확인 가능

   ✅ **변경된 프로젝트 파일들**
   - 패키지명, 앱 이름 등이 모두 변경됨

3. **Android Studio에서 열어서 빌드 테스트**

---

## 🛑 서버 중지하기

### 서버를 멈추고 싶을 때

터미널/명령 프롬프트 창에서:

1. **Ctrl + C** 키를 누르세요
2. 서버가 종료됩니다

### 다시 시작하려면

```bash
./run.sh
```

명령어를 다시 실행하면 됩니다.

---

## ❓ 자주 묻는 질문 (FAQ)

### Q1. "포트 8090이 이미 사용 중" 오류가 나요

**A:** 걱정 마세요! `run.sh` 스크립트가 **자동으로** 기존 서버를 종료하고 다시 시작합니다.

그래도 안 되면:
```bash
# Mac/Linux
lsof -ti:8090 | xargs kill -9

# Windows
netstat -ano | findstr :8090
taskkill /PID [PID번호] /F
```

### Q2. 브라우저에서 페이지가 안 열려요

**원인:**
- 서버가 제대로 실행되지 않았을 수 있습니다

**해결:**
1. 터미널에서 서버 실행 메시지 확인
2. `http://localhost:8090` 주소가 정확한지 확인
3. 서버를 종료하고 다시 시작

### Q3. ZIP 업로드 후 오류가 나요

**원인:**
- ZIP 파일이 손상되었거나
- Android 프로젝트 구조가 표준이 아닐 수 있습니다

**해결:**
1. 프로젝트 폴더에 `app/` 폴더가 있는지 확인
2. `build.gradle` 파일이 있는지 확인
3. 압축 시 프로젝트 루트부터 압축했는지 확인

### Q4. 패키지명 형식을 모르겠어요

**올바른 형식:**
- 영어 소문자만 사용
- 단어는 점(.)으로 구분
- 최소 2단계 이상 (예: `com.example`)

**예시:**
- ✅ `com.mycompany.myapp`
- ✅ `kr.co.company.project`
- ❌ `MyApp` (점 없음)
- ❌ `com.MyApp` (대문자 사용)

### Q5. 처리 시간이 얼마나 걸리나요?

**일반적으로:**
- 작은 프로젝트: 10~30초
- 중간 프로젝트: 30초~1분
- 큰 프로젝트: 1~3분

프로젝트 크기와 컴퓨터 성능에 따라 다릅니다.

### Q6. 원본 프로젝트는 어떻게 되나요?

**안심하세요!**
- 원본 파일은 **절대 수정되지 않습니다**
- 업로드한 ZIP은 임시로 처리되고 자동 삭제됩니다
- 결과물은 새로운 ZIP 파일로 다운로드됩니다

---

## 🔧 문제 해결

### Python이 없다고 나와요

**Mac:**
```bash
# Homebrew로 설치
brew install python3
```

**Windows:**
- Microsoft Store에서 "Python 3.11" 검색 후 설치

### pip 설치 오류

```bash
# pip 업그레이드
python3 -m pip install --upgrade pip

# 의존성 재설치
pip install -r requirements.txt
```

### 권한 오류 (Permission Denied)

**Mac/Linux:**
```bash
# run.sh 실행 권한 부여
chmod +x run.sh
```

---

## 📞 도움이 더 필요하신가요?

1. **로그 파일 확인:**
   - 다운로드된 ZIP 안의 `ANDROID_REBUILDER_LOG.txt` 파일 열기
   - 어떤 단계에서 문제가 발생했는지 확인 가능

2. **터미널 출력 확인:**
   - 서버 실행 시 터미널에 나타나는 메시지 읽기
   - 오류 메시지를 복사해서 검색

3. **프로젝트 구조 확인:**
   - Android Studio에서 정상적으로 열리는 프로젝트인지 확인

---

## 🎉 성공적으로 완료되었다면

축하합니다! 🎊

다운로드된 `rebuilt_project.zip` 파일을:
1. 압축 해제
2. Android Studio에서 열기
3. 빌드 및 실행 테스트

모든 패키지명, 앱 이름이 변경되어 있을 것입니다!

---

## 📌 팁 & 주의사항

### ✅ 하면 좋은 것
- 원본 프로젝트를 별도로 백업해두세요
- 결과물을 Android Studio에서 테스트 후 사용하세요
- 로그 파일을 확인하여 모든 변경사항을 파악하세요

### ❌ 하지 말아야 할 것
- 처리 중에 브라우저 창을 닫지 마세요
- 여러 프로젝트를 동시에 업로드하지 마세요
- 패키지명에 특수문자나 공백을 넣지 마세요

---

**즐거운 앱 개발 되세요!** 🚀
