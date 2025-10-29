# PRD: Android Project Rebuilder - Windows Standalone Application

## 1. 개요

### 1.1 목적
기존 macOS 독립 실행형 앱의 Windows 버전을 개발하여 Windows 사용자들도 서버 설치 없이 Android 프로젝트를 리빌드할 수 있도록 함

### 1.2 목표
- macOS 버전과 동일한 기능 제공
- Windows 네이티브 UI/UX 경험
- .exe 실행 파일 생성
- 설치 프로그램 (installer) 제공

### 1.3 범위
- **포함**: Windows 10/11 지원, PyWebView 기반 GUI, PyInstaller 빌드
- **제외**: Windows 7/8 지원, UWP/Microsoft Store 배포

---

## 2. 기술 스택 비교

### 2.1 macOS vs Windows 차이점

| 항목 | macOS | Windows |
|------|-------|---------|
| **WebView** | WebKit (Safari) | EdgeHTML/Chromium (Edge) |
| **PyWebView Backend** | Cocoa | mshtml/edgechromium |
| **실행 파일** | .app 번들 | .exe |
| **아이콘** | .icns | .ico |
| **빌드 도구** | PyInstaller | PyInstaller |
| **설치 프로그램** | .dmg | NSIS/Inno Setup |

### 2.2 선택한 기술 스택
- **GUI Framework**: PyWebView 4.4.1
- **WebView Engine**: EdgeChromium (Windows 10/11 기본 탑재)
- **빌드 도구**: PyInstaller 6.16.0
- **설치 프로그램**: Inno Setup (무료, 오픈소스)
- **아이콘**: .ico 파일

---

## 3. 기능 요구사항

### 3.1 핵심 기능 (macOS 버전과 동일)
1. ✅ 프로젝트 ZIP 파일 선택
2. ✅ 패키지명 변경
3. ✅ 앱 이름 변경
4. ✅ 버전 초기화 (1.0.0)
5. ✅ Firebase google-services.json 교체
6. ✅ 앱 아이콘 교체 (다중 해상도)
7. ✅ 스플래시 이미지 교체
8. ✅ BASE_URL 변경
9. ✅ 빌드 아티팩트 정리
10. ✅ 로그 파일 옵션

### 3.2 Windows 특화 기능
1. **Windows 스타일 파일 다이얼로그**
   - 네이티브 Windows 파일 선택창
   - "다른 이름으로 저장" 다이얼로그

2. **Windows Defender 호환성**
   - 코드 서명 (선택사항)
   - SmartScreen 경고 최소화

3. **설치 프로그램**
   - 시작 메뉴 바로가기 생성
   - 프로그램 추가/제거 등록
   - 자동 업데이트 경로 제공

---

## 4. 아키텍처

### 4.1 프로젝트 구조
```
AndroidChangePackageName/
├── standalone_app.py          # 공통 (macOS/Windows)
├── standalone_windows.spec    # Windows 전용 PyInstaller 설정
├── requirements-standalone.txt # 공통
├── frontend/
│   ├── index_standalone.html  # 공통
│   └── standalone.js          # 공통
├── backend/                   # 공통 (100% 재사용)
├── resources/
│   ├── icon.ico              # Windows 아이콘 (신규)
│   └── icon.icns             # macOS 아이콘 (기존)
├── installer/
│   └── windows_installer.iss  # Inno Setup 스크립트 (신규)
└── dist/
    ├── AndroidProjectRebuilder.exe      # Windows 실행 파일
    └── AndroidProjectRebuilder-Setup.exe # 설치 프로그램
```

### 4.2 기술적 차이점

#### macOS (기존)
```python
# PyWebView backend
import webview
window = webview.create_window(...)
webview.start()  # Uses Cocoa/WebKit
```

#### Windows (신규)
```python
# PyWebView backend (자동 선택)
import webview
window = webview.create_window(...)
webview.start()  # Uses EdgeChromium automatically on Windows 10/11
```

**핵심**: 코드 변경 없이 PyWebView가 자동으로 Windows 백엔드 선택!

---

## 5. 구현 계획

### 5.1 Phase 1: 환경 설정 (Windows 머신 필요)
- [ ] Windows 10/11 개발 환경 준비
- [ ] Python 3.13 설치 (Windows용)
- [ ] PyWebView, PyInstaller 설치
- [ ] Edge WebView2 Runtime 확인 (Windows 10/11 기본 포함)

### 5.2 Phase 2: Windows 아이콘 생성
- [ ] .ico 파일 생성 (16x16, 32x32, 48x48, 256x256)
- [ ] 기존 icon.png를 .ico로 변환

### 5.3 Phase 3: PyInstaller 설정 (Windows용)
- [ ] standalone_windows.spec 파일 작성
- [ ] Windows 특화 설정 추가:
  - console=False (콘솔 창 숨김)
  - icon='resources/icon.ico'
  - onefile=True (단일 .exe 생성)

### 5.4 Phase 4: 빌드 및 테스트
- [ ] .exe 파일 빌드
- [ ] Windows 10에서 테스트
- [ ] Windows 11에서 테스트
- [ ] 파일 다이얼로그 동작 확인

### 5.5 Phase 5: 설치 프로그램 생성
- [ ] Inno Setup 설치
- [ ] 설치 스크립트 작성 (windows_installer.iss)
- [ ] 설치 프로그램 빌드 (.exe)
- [ ] 설치/제거 테스트

### 5.6 Phase 6: 배포 준비 (선택사항)
- [ ] 코드 서명 (EV Certificate)
- [ ] VirusTotal 검증
- [ ] README_WINDOWS.md 작성

---

## 6. 상세 작업 (TASK)

### TASK 1: Windows 개발 환경 설정
**목표**: Windows에서 개발 가능한 환경 구축
- Python 3.13 설치 확인
- pip로 pywebview, pyinstaller 설치
- Edge WebView2 Runtime 확인

**검증**:
```cmd
python --version
python -c "import webview; print(webview.__version__)"
pyinstaller --version
```

---

### TASK 2: Windows 아이콘 생성
**목표**: .ico 파일 생성

**스크립트**:
```python
# create_windows_icon.py
from PIL import Image

img = Image.open('resources/icon.png')
icon_sizes = [(16,16), (32,32), (48,48), (256,256)]
img.save('resources/icon.ico', sizes=icon_sizes)
```

**검증**: `resources/icon.ico` 파일 생성 확인

---

### TASK 3: Windows PyInstaller Spec 작성
**목표**: standalone_windows.spec 파일 작성

**주요 차이점**:
```python
# Windows 전용 설정
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AndroidProjectRebuilder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 콘솔 창 숨김 (중요!)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icon.ico'  # Windows 아이콘
)
```

**검증**: spec 파일 문법 오류 없음

---

### TASK 4: .exe 빌드
**목표**: 단일 실행 파일 생성

**명령어**:
```cmd
pyinstaller standalone_windows.spec --clean --noconfirm
```

**예상 결과**:
- `dist/AndroidProjectRebuilder.exe` 생성
- 크기: 약 40-50MB
- 자체 포함형 (Python 런타임 포함)

**검증**:
```cmd
dist\AndroidProjectRebuilder.exe
```

---

### TASK 5: Windows 테스트
**목표**: 모든 기능 동작 확인

**테스트 케이스**:
1. [ ] 앱 실행 (더블클릭)
2. [ ] 파일 선택 다이얼로그 (ZIP, JSON, 이미지)
3. [ ] 프로젝트 처리 (실제 Android ZIP)
4. [ ] 저장 다이얼로그
5. [ ] 로그 표시
6. [ ] 에러 처리

**검증**: 모든 기능 정상 동작

---

### TASK 6: Inno Setup 설치 프로그램 생성
**목표**: 사용자 친화적인 설치 프로그램

**Inno Setup 스크립트** (windows_installer.iss):
```ini
[Setup]
AppName=Android Project Rebuilder
AppVersion=1.0.0
DefaultDirName={pf}\AndroidProjectRebuilder
DefaultGroupName=Android Project Rebuilder
OutputDir=dist
OutputBaseFilename=AndroidProjectRebuilder-Setup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\AndroidProjectRebuilder.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\Android Project Rebuilder"; Filename: "{app}\AndroidProjectRebuilder.exe"
Name: "{commondesktop}\Android Project Rebuilder"; Filename: "{app}\AndroidProjectRebuilder.exe"

[Run]
Filename: "{app}\AndroidProjectRebuilder.exe"; Description: "Launch Android Project Rebuilder"; Flags: postinstall nowait skipifsilent
```

**빌드**:
```cmd
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\windows_installer.iss
```

**검증**:
- `dist/AndroidProjectRebuilder-Setup.exe` 생성
- 설치 테스트 (시작 메뉴, 바탕화면 바로가기)
- 제거 테스트 (프로그램 추가/제거)

---

## 7. 주의사항 및 제약

### 7.1 Windows Defender SmartScreen
**문제**: 서명되지 않은 .exe 실행 시 경고 표시

**해결 방법**:
1. **개발/테스트**: 우클릭 → "자세한 정보" → "실행"
2. **배포**: EV Code Signing Certificate 구매 (약 $300/년)

### 7.2 EdgeChromium 요구사항
- Windows 10 (1809 이상): WebView2 Runtime 자동 포함
- Windows 10 (이전 버전): 수동 설치 필요
- Windows 11: 기본 포함

### 7.3 백신 오탐
- PyInstaller로 생성된 .exe는 일부 백신에서 오탐 가능
- 해결: VirusTotal 업로드, 코드 서명

---

## 8. 성공 기준

### 8.1 필수 요구사항
- ✅ Windows 10/11에서 실행 가능
- ✅ macOS 버전과 동일한 모든 기능 동작
- ✅ 네이티브 Windows 파일 다이얼로그
- ✅ 단일 .exe 파일 생성
- ✅ 40-60MB 크기

### 8.2 선택적 요구사항
- ⭐ 설치 프로그램 (.exe installer)
- ⭐ 코드 서명
- ⭐ 자동 업데이트 기능

---

## 9. 타임라인

### Option 1: Windows 머신 있는 경우
- **Phase 1-4**: 2-3시간
- **Phase 5**: 1시간
- **Phase 6**: 1-2시간
- **총 예상 시간**: 4-6시간

### Option 2: Windows 머신 없는 경우
- **대안 1**: 가상 머신 (Parallels, VMware)
- **대안 2**: GitHub Actions (Windows runner)
- **대안 3**: 클라우드 Windows 환경 (Azure, AWS)

---

## 10. 위험 요소 및 완화 방안

| 위험 | 영향 | 완화 방안 |
|------|------|-----------|
| Windows Defender 차단 | 높음 | 코드 서명, VirusTotal 검증 |
| WebView2 Runtime 미설치 | 중간 | 설치 프로그램에 포함 또는 자동 다운로드 |
| 백신 오탐 | 중간 | 주요 백신사에 오탐 신고 |
| 파일 경로 문제 (\ vs /) | 낮음 | pathlib 사용 (크로스 플랫폼) |
| 한글 경로 문제 | 낮음 | UTF-8 인코딩 확인 |

---

## 11. 다음 단계

### 즉시 시작 가능 (Windows 머신 있음)
```bash
# 1. 이 프로젝트를 Windows PC로 복사
# 2. 가상환경 생성
python -m venv venv
venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements-standalone.txt

# 4. 아이콘 생성
python create_windows_icon.py

# 5. 빌드
pyinstaller standalone_windows.spec --clean

# 6. 실행
dist\AndroidProjectRebuilder.exe
```

### Windows 머신 없는 경우
**GitHub Actions 워크플로우 작성** (자동 빌드)
```yaml
# .github/workflows/build-windows.yml
name: Build Windows App
on: [push]
jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - run: pip install -r requirements-standalone.txt
      - run: python create_windows_icon.py
      - run: pyinstaller standalone_windows.spec --clean
      - uses: actions/upload-artifact@v3
        with:
          name: AndroidProjectRebuilder-Windows
          path: dist/AndroidProjectRebuilder.exe
```

---

## 12. 결론

Windows 버전 개발은 **macOS 버전의 95% 코드를 재사용**할 수 있어 상대적으로 간단합니다. 주요 차이점은:
1. 아이콘 형식 (.icns → .ico)
2. PyInstaller spec 파일 설정
3. 설치 프로그램 (선택사항)

**예상 작업량**: Windows 머신이 있다면 **4-6시간**, 없다면 GitHub Actions로 자동화 가능.

**다음 액션**: Windows 개발 환경 준비 → TASK 1부터 순차 진행
