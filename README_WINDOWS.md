# Android Project Rebuilder - Windows Edition

## 🎯 개요

Android 프로젝트의 패키지명, 앱 이름, Firebase 설정 등을 자동으로 변경하는 Windows 독립 실행형 애플리케이션입니다.

**서버 설치 불필요** - 단일 `.exe` 파일만으로 실행 가능!

---

## 💻 시스템 요구사항

- **운영체제**: Windows 10 (1809 이상) 또는 Windows 11
- **아키텍처**: x64 (64비트)
- **RAM**: 최소 2GB
- **디스크 공간**: 100MB

---

## 📦 다운로드

### Option 1: Portable (설치 불필요)
- **파일**: `AndroidProjectRebuilder.exe`
- **크기**: 약 40-50MB
- **사용**: 더블클릭만 하면 바로 실행

### Option 2: Installer (권장)
- **파일**: `AndroidProjectRebuilder-Setup-v1.0.0.exe`
- **크기**: 약 45-55MB
- **장점**:
  - 시작 메뉴에 자동 추가
  - 바탕화면 바로가기 생성
  - 프로그램 추가/제거에서 관리 가능

---

## 🚀 빠른 시작

### 방법 1: Portable 실행
```
1. AndroidProjectRebuilder.exe 다운로드
2. 더블클릭 실행
3. (첫 실행 시) "추가 정보" → "실행" 클릭
```

### 방법 2: Installer 설치
```
1. AndroidProjectRebuilder-Setup-v1.0.0.exe 실행
2. 설치 마법사 따라하기
3. 시작 메뉴에서 "Android Project Rebuilder" 실행
```

---

## 📖 사용 방법

### 1단계: 필수 정보 입력

#### 프로젝트 ZIP 파일 선택
- 📁 **"ZIP 파일 선택"** 버튼 클릭
- Android Studio 프로젝트를 압축한 `.zip` 파일 선택

#### 새 패키지명 입력
```
예: com.mycompany.newapp
형식: com.회사명.앱이름 (소문자, 점으로 구분)
```

#### 새 앱 이름 입력
```
예: 새로운앱
한글, 영문, 숫자 모두 가능
```

---

### 2단계: 선택 사항 (Optional)

#### Firebase 설정 교체
- 📄 **"JSON 파일 선택"** 버튼 클릭
- Firebase Console에서 다운로드한 `google-services.json` 선택
- 패키지명이 자동으로 변경되어 적용됨

#### 앱 아이콘 교체
- 🖼️ **"아이콘 선택"** 버튼 클릭
- PNG 또는 JPG 이미지 선택 (정사각형 권장, 512x512 이상)
- 자동으로 다양한 해상도로 생성됨:
  - mdpi (48x48)
  - hdpi (72x72)
  - xhdpi (96x96)
  - xxhdpi (144x144)
  - xxxhdpi (192x192)

#### 스플래시 이미지 교체
- 🖼️ **"스플래시 선택"** 버튼 클릭
- PNG 또는 JPG 이미지 선택 (세로로 긴 이미지 권장, 1080x1920)
- 모든 해상도의 drawable 폴더에 자동 배치

#### BASE_URL 변경
```
예: https://api.myserver.com/
주의: 마지막에 반드시 슬래시(/) 포함!
```

#### 로그 파일 포함
- ✅ 체크: 처리 로그를 `ANDROID_REBUILDER_LOG.txt` 파일로 ZIP에 포함
- ❌ 체크 해제: 로그 파일 미포함

---

### 3단계: 리빌드 실행

1. **🚀 "프로젝트 리빌드 시작"** 버튼 클릭
2. 처리 진행 상황 실시간 확인:
   - 진행바 표시
   - 각 단계별 로그 출력
3. 저장 위치 선택 다이얼로그 표시
4. 저장 위치 선택 후 완료!

---

## 🔧 주요 기능

### 자동 처리 항목

#### ✅ 패키지명 변경
- `build.gradle` / `build.gradle.kts` 파일의 `applicationId` 변경
- `AndroidManifest.xml`의 `package` 속성 변경
- 모든 `.kt` / `.java` 파일의 `package` 선언 변경
- 프로젝트 전체 텍스트 파일에서 패키지명 일괄 치환
- 디렉토리 구조 자동 변경 (`com/old/pkg` → `com/new/pkg`)

#### ✅ 앱 이름 변경
- `strings.xml`의 `app_name` 변경
- AndroidManifest의 `android:label` 변경

#### ✅ 버전 초기화
- `versionCode` → 1
- `versionName` → 1.0.0

#### ✅ Firebase 설정 교체
- 기존 `google-services.json` 파일 탐지
- 동일 위치에 새 파일로 교체
- JSON 내 모든 패키지 참조를 새 패키지명으로 변경

#### ✅ 앱 아이콘 교체
- 5가지 해상도 자동 생성
- 모든 런처 아이콘 파일 교체:
  - `ic_launcher.png`
  - `ic_launcher_round.png`
  - `ic_launcher_background.png`
  - `ic_launcher_foreground.png`
  - `ic_launcher_monochrome.png`

#### ✅ 스플래시 이미지 교체
- 모든 해상도의 drawable 폴더에 배치
- layout XML의 ImageView 자동 업데이트

#### ✅ BASE_URL 변경
- Kotlin 파일에서 `BASE_URL` 상수 일괄 변경
- 환경 변수 파일 자동 업데이트

#### ✅ 빌드 정리
- `build/` 폴더 삭제
- `.gradle/` 폴더 삭제
- `local.properties` 삭제
- 캐시 파일 정리

#### ✅ ZIP 폴더명 변경
- 압축 해제된 프로젝트 폴더명을 새 앱 이름으로 자동 변경
- 결과 ZIP 파일명: `package_changed_{앱이름}.zip`

---

## 📊 처리 예시

### 입력
```
- 프로젝트: MyOldProject.zip
- 패키지명: com.example.oldapp → com.newcompany.mynewapp
- 앱 이름: 구앱 → 신규앱
- Firebase: google-services.json (새 프로젝트)
- 아이콘: new_icon.png (1024x1024)
```

### 출력
```
package_changed_신규앱.zip
├── 신규앱/  ← 폴더명 변경됨
│   ├── app/
│   │   ├── src/
│   │   │   ├── main/
│   │   │   │   ├── java/com/newcompany/mynewapp/  ← 패키지 구조 변경
│   │   │   │   ├── res/
│   │   │   │   │   ├── mipmap-mdpi/ic_launcher.png  ← 새 아이콘
│   │   │   │   │   ├── values/strings.xml  ← 앱 이름 변경
│   │   │   │   ├── AndroidManifest.xml  ← 패키지명 변경
│   │   │   │   └── google-services.json  ← 새 Firebase 설정
│   │   └── build.gradle  ← applicationId 변경
│   └── ANDROID_REBUILDER_LOG.txt  ← 처리 로그 (선택사항)
```

---

## ⚠️ 주의사항

### Windows Defender 경고
**첫 실행 시 "Windows에서 PC를 보호했습니다" 메시지 표시**

이유: 코드 서명되지 않은 실행 파일이기 때문

**해결 방법**:
1. "추가 정보" 클릭
2. "실행" 버튼 클릭
3. 앱이 정상 실행됨

> 💡 **안전성**: 이 앱은 오픈소스이며 악성 코드가 없습니다. Windows Defender 경고는 서명되지 않은 모든 .exe 파일에 표시되는 일반적인 경고입니다.

### 백신 프로그램
일부 백신 프로그램에서 오탐이 발생할 수 있습니다.

**해결**:
- 예외 목록에 추가
- 또는 소스 코드에서 직접 빌드 (BUILD_WINDOWS.md 참조)

---

## 🐛 문제 해결

### 문제 1: 앱이 실행되지 않음
**증상**: 더블클릭 시 아무 반응 없음

**원인**: Edge WebView2 Runtime 미설치 (드물음)

**해결**:
1. https://developer.microsoft.com/microsoft-edge/webview2/ 방문
2. "Evergreen Standalone Installer" 다운로드
3. 설치 후 재시도

---

### 문제 2: 파일 선택 다이얼로그가 열리지 않음
**증상**: 버튼 클릭 시 반응 없음

**해결**:
1. 앱 완전 종료
2. 작업 관리자에서 프로세스 확인 및 종료
3. 재실행

---

### 문제 3: 처리 중 오류 발생
**증상**: 로그에 `[ERROR]` 메시지 표시

**확인 사항**:
- ✅ Android 프로젝트 ZIP 파일이 올바른지 확인
- ✅ 패키지명 형식이 올바른지 확인 (com.company.app)
- ✅ 이미지 파일이 손상되지 않았는지 확인
- ✅ 충분한 디스크 공간이 있는지 확인 (최소 500MB)

---

### 문제 4: 저장 실패
**증상**: "Failed to save file" 메시지

**해결**:
- 다른 폴더에 저장 시도
- 폴더 권한 확인
- 바탕화면 또는 다운로드 폴더 사용

---

## 💡 팁 & 트릭

### 빠른 실행
바탕화면 바로가기 생성:
1. `AndroidProjectRebuilder.exe` 우클릭
2. "바로가기 만들기" 선택
3. 바탕화면으로 이동

### 배치 처리
PowerShell 스크립트로 여러 프로젝트 자동 처리 가능 (고급 사용자용)

### 로그 파일 활용
문제 발생 시 `ANDROID_REBUILDER_LOG.txt` 파일을 확인하면 정확한 오류 원인 파악 가능

---

## 📝 릴리스 노트

### v1.0.0 (2025-10-29)
- ✨ 최초 Windows 버전 릴리스
- ✅ macOS 버전의 모든 기능 포함
- ✅ Windows 네이티브 파일 다이얼로그
- ✅ EdgeChromium WebView 지원
- ✅ 단일 .exe 실행 파일
- ✅ Inno Setup 설치 프로그램

---

## 🤝 지원

### 문의
- 이슈: GitHub Issues
- 이메일: support@example.com

### 기여
이 프로젝트는 오픈소스입니다. Pull Request 환영!

---

## 📄 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

---

## 🔗 관련 링크

- GitHub Repository: https://github.com/yourproject
- macOS 버전: [다운로드 링크]
- 사용 가이드: [문서 링크]
- Firebase Console: https://console.firebase.google.com
- AppFactory Admin: [링크]

---

## ✨ 추가 기능 요청

원하는 기능이 있으신가요?
- GitHub Issues에 제안해주세요
- 또는 직접 기여해주세요 (Pull Request)

---

**즐거운 개발 되세요!** 🚀
