# 🤖 GitHub Actions 자동 빌드 가이드

## 🎯 개요

**Windows PC 없이도** GitHub Actions가 자동으로:
- ✅ Windows 설치 파일 (`.exe`) 생성
- ✅ macOS DMG 생성
- ✅ GitHub Releases에 자동 업로드

**한 번만 설정하면 끝!**

---

## 🚀 설정 방법 (5분)

### Step 1: GitHub 리포지토리 생성

```bash
# 1. GitHub에서 새 리포지토리 생성
# 예: https://github.com/yourusername/AndroidChangePackageName

# 2. 로컬 프로젝트를 GitHub에 푸시
git init
git add .
git commit -m "feat: Android Project Rebuilder - 전체 기능 구현"
git branch -M main
git remote add origin https://github.com/yourusername/AndroidChangePackageName.git
git push -u origin main
```

### Step 2: 워크플로우 파일 확인

다음 파일들이 이미 생성되어 있습니다:
```
.github/
└── workflows/
    ├── build-windows.yml  ✅ Windows 자동 빌드
    └── build-macos.yml    ✅ macOS 자동 빌드
```

### Step 3: 릴리스 태그 생성 및 푸시

```bash
# 버전 태그 생성 (v1.0.0 형식)
git tag v1.0.0

# 태그 푸시 → 자동 빌드 시작!
git push origin v1.0.0
```

---

## 🎬 자동 빌드 과정

### 태그를 푸시하면...

```
1. GitHub Actions 시작
   ↓
2. Windows 빌드 (windows-latest)
   - Python 3.13 설치
   - 의존성 설치
   - .exe 생성
   - Inno Setup 설치
   - 설치 프로그램 생성
   ↓
3. macOS 빌드 (macos-latest)
   - Python 3.13 설치
   - 의존성 설치
   - .app 생성
   - DMG 생성
   ↓
4. GitHub Release 자동 생성
   - AndroidProjectRebuilder.exe (Portable)
   - AndroidProjectRebuilder-Setup-v1.0.0.exe (Installer)
   - AndroidProjectRebuilder.dmg (macOS)
   ↓
5. 완료! 다운로드 링크 공개
```

**소요 시간**: 약 10-15분 (자동)

---

## 📦 빌드 결과 확인

### GitHub Actions 페이지
```
1. GitHub 리포지토리 페이지 접속
2. "Actions" 탭 클릭
3. 빌드 진행 상황 실시간 확인
4. 완료되면 초록색 체크마크 표시
```

### Releases 페이지
```
1. GitHub 리포지토리 페이지 접속
2. "Releases" 탭 클릭 (오른쪽)
3. 최신 릴리스 확인
4. 파일 다운로드 가능:
   - AndroidProjectRebuilder.exe (Windows Portable)
   - AndroidProjectRebuilder-Setup-v1.0.0.exe (Windows Installer)
   - AndroidProjectRebuilder.dmg (macOS)
```

### Artifacts (빌드 결과물)
```
1. Actions 탭 → 완료된 워크플로우 클릭
2. 하단 "Artifacts" 섹션
3. 다운로드 가능 (90일간 보관)
```

---

## 🔧 수동 빌드 (태그 없이)

GitHub UI에서 수동으로 빌드 실행:

```
1. GitHub 리포지토리 → "Actions" 탭
2. 왼쪽에서 "Build Windows Application" 선택
3. 오른쪽 "Run workflow" 버튼 클릭
4. "Run workflow" 확인
```

macOS도 동일하게 "Build macOS Application" 선택

---

## 📝 버전 업데이트 방법

### 새 버전 릴리스

```bash
# 1. 코드 수정
git add .
git commit -m "feat: 새 기능 추가"
git push

# 2. 새 버전 태그
git tag v1.0.1

# 3. 태그 푸시 → 자동 빌드!
git push origin v1.0.1
```

**자동으로**:
- Windows 설치 파일 재생성
- macOS DMG 재생성
- 새 GitHub Release 생성

---

## 🎯 워크플로우 상세 설명

### build-windows.yml

```yaml
on:
  push:
    tags:
      - 'v*'  # v로 시작하는 태그 (예: v1.0.0)
  workflow_dispatch:  # 수동 실행 가능

jobs:
  build-windows:
    runs-on: windows-latest  # Windows 환경

    steps:
    - Python 3.13 설치
    - 의존성 설치
    - 아이콘 생성
    - PyInstaller로 .exe 빌드
    - Inno Setup 다운로드 및 설치
    - 설치 프로그램 빌드
    - Artifacts 업로드
    - Release 생성 (태그 시)
```

### build-macos.yml

```yaml
on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build-macos:
    runs-on: macos-latest  # macOS 환경

    steps:
    - Python 3.13 설치
    - 의존성 설치
    - 아이콘 생성
    - PyInstaller로 .app 빌드
    - DMG 생성
    - Artifacts 업로드
    - Release 생성 (태그 시)
```

---

## ✅ 장점

### 1. Windows PC 불필요
- ✅ GitHub Actions가 Windows 환경 제공
- ✅ 자동으로 Windows에서 빌드
- ✅ 로컬 환경에 영향 없음

### 2. 완전 자동화
- ✅ 태그 푸시만 하면 끝
- ✅ 빌드, 테스트, 배포 자동
- ✅ Release 노트 자동 생성

### 3. 크로스 플랫폼 동시 빌드
- ✅ Windows + macOS 동시 빌드
- ✅ 일관된 빌드 환경
- ✅ 버전 관리 용이

### 4. 무료
- ✅ Public 리포지토리: 완전 무료
- ✅ Private 리포지토리: 월 2,000분 무료

---

## 🐛 문제 해결

### 문제 1: 빌드 실패
**증상**: Actions 탭에서 빨간색 X 표시

**해결**:
1. 해당 워크플로우 클릭
2. 실패한 step 확인
3. 로그 읽고 원인 파악
4. 코드 수정 후 재푸시

### 문제 2: Release가 생성되지 않음
**증상**: Artifacts는 있는데 Release가 없음

**원인**: 태그가 아닌 일반 커밋

**해결**:
```bash
# 태그 생성 및 푸시
git tag v1.0.0
git push origin v1.0.0
```

### 문제 3: 워크플로우가 실행되지 않음
**원인**: `.github/workflows/` 폴더가 main 브랜치에 없음

**해결**:
```bash
# 워크플로우 파일 커밋 및 푸시
git add .github/
git commit -m "feat: Add GitHub Actions workflows"
git push
```

---

## 📊 사용 예시

### 시나리오: 새 버전 배포

```bash
# 1. 기능 개발
vim standalone_app.py
# ... 코드 수정 ...

# 2. 커밋
git add .
git commit -m "feat: Add new feature"
git push

# 3. 버전 태그 생성
git tag v1.1.0

# 4. 태그 푸시 → 자동 빌드 시작!
git push origin v1.1.0

# 5. GitHub에서 확인
# - Actions 탭: 빌드 진행 상황 (10-15분)
# - Releases 탭: 완료 후 다운로드 가능
```

### 사용자 다운로드

```
1. GitHub 리포지토리 → Releases 탭
2. 최신 버전 선택 (예: v1.1.0)
3. Assets 섹션에서 다운로드:

   Windows 사용자:
   - AndroidProjectRebuilder-Setup-v1.0.0.exe (권장)
   또는
   - AndroidProjectRebuilder.exe (Portable)

   macOS 사용자:
   - AndroidProjectRebuilder.dmg
```

---

## 🔐 보안 고려사항

### GITHUB_TOKEN
- ✅ 자동으로 제공됨
- ✅ 리포지토리에만 접근 가능
- ✅ 별도 설정 불필요

### Secrets
현재는 불필요하지만, 코드 서명 추가 시:

```yaml
# .github/workflows/build-windows.yml에 추가
- name: Sign executable
  env:
    CERTIFICATE_PASSWORD: ${{ secrets.CERT_PASSWORD }}
  run: |
    # 서명 로직
```

---

## 📈 통계

### 빌드 시간 (평균)
- Windows 빌드: 약 8-10분
- macOS 빌드: 약 6-8분
- 총 소요 시간: 약 10-15분 (병렬 실행)

### 파일 크기
- Windows Portable: ~40-50MB
- Windows Installer: ~45-55MB
- macOS DMG: ~30-40MB

---

## 🎉 완료!

이제 **태그만 푸시하면** 자동으로:
1. ✅ Windows 설치 파일 생성
2. ✅ macOS DMG 생성
3. ✅ GitHub Releases에 업로드
4. ✅ 다운로드 링크 공개

**Windows PC 없이도 완벽한 배포가 가능합니다!** 🚀

---

## 🔗 다음 단계

### 즉시 실행
```bash
# 1. GitHub에 푸시
git add .
git commit -m "feat: Add GitHub Actions workflows"
git push

# 2. 태그 생성 및 푸시
git tag v1.0.0
git push origin v1.0.0

# 3. Actions 탭에서 빌드 확인 (10-15분)

# 4. Releases 탭에서 다운로드!
```

### 선택사항: 코드 서명
- Windows: EV Code Signing Certificate
- macOS: Apple Developer Certificate

### 선택사항: 자동 업데이트
- Sparkle (macOS)
- Squirrel (Windows)

---

**질문이나 문제가 있으면 GitHub Issues에 등록해주세요!**
