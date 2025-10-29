# 🚀 빠른 시작 가이드

## 1️⃣ GitHub에 푸시 (1분)

```bash
# GitHub에서 새 리포지토리 생성 후:
git remote add origin https://github.com/YOUR_USERNAME/AndroidChangePackageName.git
git push -u origin main
```

---

## 2️⃣ 자동 빌드 트리거 (10초)

```bash
# 버전 태그 생성
git tag v1.0.0

# 태그 푸시 → 자동 빌드 시작!
git push origin v1.0.0
```

**이게 끝입니다!** 🎉

---

## 3️⃣ 빌드 확인 (10-15분 대기)

### GitHub Actions에서 실시간 확인
```
1. GitHub 리포지토리 페이지
2. "Actions" 탭 클릭
3. 진행 중인 워크플로우 확인
```

---

## 4️⃣ 다운로드 (즉시 가능)

```
1. "Releases" 탭 클릭
2. "v1.0.0" 릴리스 선택
3. 다운로드:
   - Windows: AndroidProjectRebuilder-Setup-v1.0.0.exe
   - macOS: AndroidProjectRebuilder.dmg
```

**완성!** 🎉
