# Windows 빌드 가이드

## 📋 사전 준비사항

### 1. Windows 환경
- Windows 10 (버전 1809 이상) 또는 Windows 11
- Python 3.13 설치
- Git 설치 (선택사항)

### 2. Python 설치 확인
```cmd
python --version
```
출력: `Python 3.13.x`

---

## 🚀 빌드 단계

### Step 1: 프로젝트 복사
이 프로젝트 폴더를 Windows PC로 복사하거나 클론:
```cmd
git clone <repository-url>
cd AndroidChangePackageName
```

### Step 2: 가상환경 생성
```cmd
python -m venv venv
venv\Scripts\activate
```

프롬프트가 `(venv)`로 바뀌면 성공!

### Step 3: 의존성 설치
```cmd
pip install -r requirements-standalone.txt
```

### Step 4: Windows 아이콘 생성
```cmd
python create_windows_icon.py
```

출력:
```
✓ Created resources/icon.ico
  Sizes: 16x16, 32x32, 48x48, 64x64, 128x128, 256x256
  File size: XX KB
✅ Windows icon ready!
```

### Step 5: .exe 파일 빌드
```cmd
pyinstaller standalone_windows.spec --clean --noconfirm
```

빌드 시간: 약 2-3분

### Step 6: 실행 테스트
```cmd
dist\AndroidProjectRebuilder.exe
```

앱 창이 열리면 성공! 🎉

---

## 📦 설치 프로그램 생성 (선택사항)

### Step 1: Inno Setup 다운로드 및 설치
https://jrsoftware.org/isdl.php
(무료, 약 2MB)

### Step 2: 설치 프로그램 빌드
```cmd
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\windows_installer.iss
```

### Step 3: 설치 프로그램 확인
```
dist\AndroidProjectRebuilder-Setup-v1.0.0.exe
```

이 파일을 배포하면 사용자가 간편하게 설치 가능!

---

## 🧪 테스트

### 기본 테스트
1. ✅ 앱 실행 (더블클릭)
2. ✅ 창이 정상적으로 열림
3. ✅ UI가 제대로 표시됨

### 기능 테스트
1. ✅ "ZIP 파일 선택" 버튼 클릭 → 파일 선택 다이얼로그 표시
2. ✅ Android 프로젝트 ZIP 선택
3. ✅ 패키지명, 앱 이름 입력
4. ✅ "프로젝트 리빌드 시작" 클릭
5. ✅ 처리 로그 표시
6. ✅ 저장 다이얼로그 표시
7. ✅ 결과 ZIP 파일 저장

---

## ⚠️ 문제 해결

### 문제 1: "Windows에서 PC를 보호했습니다" 경고
**원인**: 코드 서명되지 않은 .exe

**해결**:
1. "추가 정보" 클릭
2. "실행" 버튼 클릭

### 문제 2: PyInstaller 빌드 실패
**원인**: 의존성 미설치

**해결**:
```cmd
pip install --upgrade pip
pip install -r requirements-standalone.txt
```

### 문제 3: 앱 실행 시 아무것도 안 보임
**원인**: console=False 설정으로 에러 메시지가 숨겨짐

**디버그**:
1. `standalone_windows.spec` 파일 열기
2. `console=False` → `console=True` 변경
3. 재빌드
4. 콘솔 창에서 에러 메시지 확인

### 문제 4: WebView2 에러
**원인**: Edge WebView2 Runtime 미설치 (드물음)

**해결**:
https://developer.microsoft.com/microsoft-edge/webview2/
에서 "Evergreen Standalone Installer" 다운로드 및 설치

---

## 📊 빌드 결과물

### 단일 실행 파일
- **경로**: `dist\AndroidProjectRebuilder.exe`
- **크기**: 약 40-50MB
- **포함**: Python 런타임, 모든 라이브러리, HTML/JS

### 설치 프로그램 (선택)
- **경로**: `dist\AndroidProjectRebuilder-Setup-v1.0.0.exe`
- **크기**: 약 45-55MB
- **기능**:
  - 시작 메뉴 바로가기 생성
  - 바탕화면 아이콘 (선택)
  - 프로그램 추가/제거 등록
  - 자동 제거 지원

---

## 🔄 업데이트 방법

### 코드 수정 후
```cmd
# 1. 가상환경 활성화
venv\Scripts\activate

# 2. (필요시) HTML 재생성
python create_standalone_html.py

# 3. 재빌드
pyinstaller standalone_windows.spec --clean --noconfirm

# 4. 테스트
dist\AndroidProjectRebuilder.exe
```

---

## 📤 배포

### 개발/테스트용
- `dist\AndroidProjectRebuilder.exe` 파일만 공유
- 압축 권장 (ZIP)

### 일반 사용자용
- `dist\AndroidProjectRebuilder-Setup-v1.0.0.exe` 공유
- 사용자는 설치 후 시작 메뉴에서 실행

### GitHub Release
```cmd
# 1. 버전 태그
git tag v1.0.0
git push origin v1.0.0

# 2. GitHub Releases에 업로드
- AndroidProjectRebuilder.exe (Portable)
- AndroidProjectRebuilder-Setup-v1.0.0.exe (Installer)
```

---

## 🤖 자동 빌드 (GitHub Actions)

`.github/workflows/build-windows.yml` 파일 생성:

```yaml
name: Build Windows App

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.13'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-standalone.txt

    - name: Create Windows icon
      run: python create_windows_icon.py

    - name: Build executable
      run: pyinstaller standalone_windows.spec --clean --noconfirm

    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: AndroidProjectRebuilder-Windows
        path: dist/AndroidProjectRebuilder.exe

    - name: Create Release
      uses: softprops/action-gh-release@v1
      if: startsWith(github.ref, 'refs/tags/')
      with:
        files: dist/AndroidProjectRebuilder.exe
```

이렇게 하면 `git push --tags` 시 자동으로 Windows 빌드!

---

## 📝 체크리스트

### 빌드 전
- [ ] Python 3.13 설치 확인
- [ ] 가상환경 생성 및 활성화
- [ ] requirements-standalone.txt 설치
- [ ] resources/icon.ico 생성

### 빌드
- [ ] `pyinstaller standalone_windows.spec --clean --noconfirm` 실행
- [ ] `dist\AndroidProjectRebuilder.exe` 생성 확인

### 테스트
- [ ] .exe 실행
- [ ] 파일 선택 다이얼로그 테스트
- [ ] 실제 Android 프로젝트 처리 테스트
- [ ] 저장 기능 테스트

### 배포 (선택)
- [ ] 설치 프로그램 생성
- [ ] 코드 서명 (선택)
- [ ] GitHub Release 업로드

---

## 💡 팁

### 크기 최적화
```cmd
# UPX 압축 활성화 (spec 파일에서 이미 설정됨)
upx=True
```

### 디버그 모드
```python
# standalone_windows.spec에서
console=True  # 콘솔 창 표시
debug=True    # 디버그 정보 출력
```

### 빠른 재빌드
```cmd
# --clean 없이 빌드 (캐시 사용)
pyinstaller standalone_windows.spec --noconfirm
```

---

## 🆘 지원

문제가 발생하면:
1. 이슈 생성: GitHub Issues
2. 로그 확인: `build\standalone\warn-standalone.txt`
3. 디버그 모드로 재빌드

---

**빌드 성공하셨나요?** 🎉

다음 단계:
1. 실제 Android 프로젝트로 테스트
2. 사용자 피드백 수집
3. 코드 서명 고려 (배포 시)
