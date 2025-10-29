# 🐛 버그 수정 보고서

## 문제 상황

### 증상
- macOS 앱에서 "📁 ZIP 파일 선택" 버튼 클릭 시
- 팝업 에러: `Error: null is not an object`
- 파일 선택 다이얼로그가 열리지 않음

### 에러 메시지
```
Error: null is not an object (evaluating 
'document.getElementById('zipFileInfo').textContent = ...')
```

---

## 원인 분석

### JavaScript 코드 (standalone.js)
```javascript
// 라인 15
document.getElementById('zipFileInfo').textContent = `✓ Selected: ...`;
```

### HTML 파일 (index_standalone.html) - 문제
```html
<!-- ID가 없음! -->
<div class="file-info">압축된 Android 프로젝트 파일을 선택하세요</div>
```

### 원인
1. `create_standalone_html.py`에서 텍스트 매칭 실패
2. 원본 HTML의 텍스트가 변경되었는데 스크립트는 구버전 텍스트로 검색
3. 매칭 실패 → ID 추가 안됨 → `getElementById` 반환값 `null`
4. `null.textContent` 시도 → 에러 발생

---

## 해결 방법

### 1. create_standalone_html.py 수정

#### 변경 전
```python
replacements = [
    (
        '<div class="file-info">업로드할 Android 프로젝트 ZIP 파일을 선택하세요</div>',
        '<div class="file-info" id="zipFileInfo">업로드할 Android 프로젝트 ZIP 파일을 선택하세요</div>'
    ),
]
```

#### 변경 후
```python
replacements = [
    (
        '<div class="file-info">압축된 Android 프로젝트 파일을 선택하세요</div>',
        '<div class="file-info" id="zipFileInfo">압축된 Android 프로젝트 파일을 선택하세요</div>'
    ),
]
```

### 2. 모든 file-info 요소 수정
- ✅ zipFileInfo (ZIP 파일)
- ✅ googleServicesInfo (Firebase JSON)
- ✅ appIconInfo (앱 아이콘)
- ✅ splashInfo (스플래시 이미지)

### 3. HTML 재생성
```bash
python create_standalone_html.py
```

### 4. 앱 재빌드
```bash
pyinstaller standalone.spec --clean --noconfirm
```

---

## 수정 결과

### HTML (수정 후)
```html
<!-- ID 추가됨! -->
<div class="file-info" id="zipFileInfo">압축된 Android 프로젝트 파일을 선택하세요</div>
<div class="file-info" id="googleServicesInfo">Firebase 설정 파일 (선택)</div>
<div class="file-info" id="appIconInfo">PNG 또는 JPG 형식 (모든 해상도에 적용)</div>
<div class="file-info" id="splashInfo">PNG 또는 JPG 형식 - 스플래시 화면에 사용되는 이미지</div>
```

### 동작 확인
```
✅ "📁 ZIP 파일 선택" 버튼 클릭
✅ 파일 선택 다이얼로그 정상 표시
✅ 파일 선택 후 경로 표시
✅ 에러 없음
```

---

## GitHub Actions 워크플로우 업데이트

### build-windows.yml & build-macos.yml
```yaml
- name: Create standalone HTML (with fixed IDs)
  run: python create_standalone_html.py
```

이제 자동 빌드 시에도 항상 최신 HTML이 생성됩니다!

---

## 영향 범위

### macOS
- ✅ 로컬 빌드 수정 완료
- ✅ dist/AndroidProjectRebuilder.app 재생성
- ✅ 테스트 완료

### Windows
- ✅ create_standalone_html.py 수정 (공통 파일)
- ✅ GitHub Actions 워크플로우 업데이트
- ✅ 다음 자동 빌드 시 자동 적용

---

## 재발 방지

### 1. 빌드 프로세스 강화
```bash
# 항상 HTML을 재생성
python create_standalone_html.py

# 그 다음 빌드
pyinstaller standalone.spec --clean
```

### 2. 테스트 자동화 (향후)
```python
# test_html_ids.py
def test_html_has_required_ids():
    with open('frontend/index_standalone.html') as f:
        html = f.read()
    
    assert 'id="zipFileInfo"' in html
    assert 'id="googleServicesInfo"' in html
    assert 'id="appIconInfo"' in html
    assert 'id="splashInfo"' in html
```

### 3. 문서화
- ✅ BUILD_WINDOWS.md에 HTML 생성 스텝 명시
- ✅ STANDALONE_BUILD_REPORT.md 업데이트

---

## 커밋 히스토리

```
5361e9e fix: 파일 선택 다이얼로그 오류 수정 - HTML ID 매칭 문제 해결
f7489e4 fix: Update Windows spec to use fixed standalone HTML
```

---

## 결론

✅ **문제 완전 해결**
- macOS 앱: 즉시 수정 완료
- Windows 앱: 다음 자동 빌드 시 자동 적용
- GitHub Actions: 워크플로우 업데이트 완료

**테스트 방법**:
1. macOS: `open dist/AndroidProjectRebuilder.app`
2. "📁 ZIP 파일 선택" 버튼 클릭
3. 파일 선택 다이얼로그 정상 동작 확인

**Windows 테스트** (자동 빌드 후):
1. GitHub Releases에서 다운로드
2. AndroidProjectRebuilder-Setup.exe 실행
3. 동일하게 테스트

---

**수정 완료 시간**: 2025-10-29 12:49
**영향받은 파일**: 3개 (create_standalone_html.py, 2개 워크플로우)
**테스트 상태**: ✅ macOS 완료, ⏳ Windows 대기 (자동 빌드)
