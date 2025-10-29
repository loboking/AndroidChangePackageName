"""
패키지명, 앱 이름, 버전 교체 로직
"""
import re
import os
import shutil
from pathlib import Path
from typing import List, Tuple


def detect_old_package_name(app_module: str) -> Tuple[str, List[str]]:
    """
    build.gradle(.kts)에서 기존 패키지명 탐지

    Args:
        app_module: app 모듈 경로

    Returns:
        (old_package_name, logs)
    """
    logs = []
    app_path = Path(app_module)

    # build.gradle 또는 build.gradle.kts 찾기
    gradle_files = list(app_path.glob('build.gradle*'))
    if not gradle_files:
        logs.append("[PACKAGE] ERROR: build.gradle not found in " + str(app_path))
        return None, logs

    gradle_file = gradle_files[0]
    logs.append(f"[PACKAGE] Reading gradle file: {gradle_file}")

    try:
        content = gradle_file.read_text(encoding='utf-8', errors='ignore')

        # 패턴 1: applicationId "com.example.app" (Groovy)
        match = re.search(r'applicationId\s+["\']([^"\']+)["\']', content)
        if match:
            old_package = match.group(1)
            logs.append(f"[PACKAGE] ✅ Detected old package from applicationId: {old_package}")
            return old_package, logs

        # 패턴 2: applicationId = "com.example.app" (Kotlin DSL)
        match = re.search(r'applicationId\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            old_package = match.group(1)
            logs.append(f"[PACKAGE] ✅ Detected old package from applicationId: {old_package}")
            return old_package, logs

        # 패턴 3: namespace = "com.example.app" (AGP 7.0+)
        match = re.search(r'namespace\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            old_package = match.group(1)
            logs.append(f"[PACKAGE] ✅ Detected old package from namespace: {old_package}")
            return old_package, logs

        logs.append("[PACKAGE] ⚠️ WARNING: Could not detect applicationId or namespace in gradle file")
        logs.append("[PACKAGE] Gradle file content (first 500 chars):")
        logs.append(content[:500])
        return None, logs
    except Exception as e:
        import traceback
        logs.append(f"[PACKAGE] ❌ ERROR reading {gradle_file}: {str(e)}")
        logs.append(f"[PACKAGE] Traceback: {traceback.format_exc()}")
        return None, logs


def replace_package_name(project_root: str, old_package: str, new_package: str) -> Tuple[List[str], int]:
    """
    프로젝트 전체에서 패키지명 교체
    - build.gradle(.kts)의 applicationId
    - 소스 파일(.kt/.java)의 package 선언
    - AndroidManifest.xml의 package 속성
    - 디렉토리 구조 변경

    Args:
        project_root: 프로젝트 루트
        old_package: 기존 패키지명
        new_package: 새 패키지명

    Returns:
        (로그 메시지 리스트, 변경된 파일 수)
    """
    logs = []
    change_count = 0

    if not old_package:
        logs.append("[PACKAGE] ⚠️ Skipping package replacement (old package not detected)")
        return logs, 0

    logs.append(f"[PACKAGE] 🔄 Starting package replacement:")
    logs.append(f"[PACKAGE]    Old: {old_package}")
    logs.append(f"[PACKAGE]    New: {new_package}")

    project_path = Path(project_root)

    # 1. build.gradle(.kts) 파일 수정
    for gradle_file in project_path.rglob('build.gradle*'):
        try:
            content = gradle_file.read_text(encoding='utf-8', errors='ignore')
            original_content = content

            # applicationId "..." (Groovy)
            content = re.sub(
                r'(applicationId\s+["\'])' + re.escape(old_package) + r'(["\'])',
                r'\1' + new_package + r'\2',
                content
            )

            # applicationId = "..." (Kotlin DSL)
            content = re.sub(
                r'(applicationId\s*=\s*["\'])' + re.escape(old_package) + r'(["\'])',
                r'\1' + new_package + r'\2',
                content
            )

            # namespace = "..." (AGP 7.0+)
            content = re.sub(
                r'(namespace\s*=\s*["\'])' + re.escape(old_package) + r'(["\'])',
                r'\1' + new_package + r'\2',
                content
            )

            if content != original_content:
                gradle_file.write_text(content, encoding='utf-8')
                logs.append(f"[PACKAGE] ✅ Updated package in {gradle_file.relative_to(project_path)}")
                change_count += 1
        except Exception as e:
            import traceback
            logs.append(f"[PACKAGE] ❌ ERROR updating {gradle_file}: {str(e)}")
            logs.append(f"[PACKAGE] Traceback: {traceback.format_exc()}")

    # 2. AndroidManifest.xml 파일 수정
    for manifest in project_path.rglob('AndroidManifest.xml'):
        try:
            content = manifest.read_text(encoding='utf-8', errors='ignore')
            new_content = re.sub(
                r'(package\s*=\s*["\'])' + re.escape(old_package) + r'(["\'])',
                r'\1' + new_package + r'\2',
                content
            )
            if new_content != content:
                manifest.write_text(new_content, encoding='utf-8')
                logs.append(f"[PACKAGE] ✅ Updated package in {manifest.relative_to(project_path)}")
                change_count += 1
        except Exception as e:
            import traceback
            logs.append(f"[PACKAGE] ❌ ERROR updating {manifest}: {str(e)}")
            logs.append(f"[PACKAGE] Traceback: {traceback.format_exc()}")

    # 3. 소스 파일(.kt/.java) package 선언 수정
    source_files = list(project_path.rglob('*.kt')) + list(project_path.rglob('*.java'))
    for source_file in source_files:
        # build 폴더 제외
        if 'build' in source_file.parts:
            continue
        try:
            content = source_file.read_text(encoding='utf-8', errors='ignore')
            original_content = content

            # 패턴: package 선언 (서브패키지 포함, 세미콜론 선택적)
            new_content = re.sub(
                r'^package\s+' + re.escape(old_package) + r'(\.[a-zA-Z_][a-zA-Z0-9_.]*)?\s*;?\s*$',
                f'package {new_package}\\1',
                content,
                flags=re.MULTILINE
            )

            if new_content != original_content:
                source_file.write_text(new_content, encoding='utf-8')
                logs.append(f"[PACKAGE] ✅ Updated package in {source_file.relative_to(project_path)}")
                change_count += 1
        except Exception as e:
            import traceback
            logs.append(f"[PACKAGE] ❌ ERROR updating {source_file}: {str(e)}")
            logs.append(f"[PACKAGE] Traceback: {traceback.format_exc()}")

    # 4. 모든 텍스트 파일에서 패키지명 일괄 변경
    bulk_logs, bulk_changes = _replace_package_in_all_files(project_root, old_package, new_package)
    logs.extend(bulk_logs)
    change_count += bulk_changes

    # 5. 디렉토리 구조 변경
    dir_logs, dir_changes = _rename_package_directories(project_root, old_package, new_package)
    logs.extend(dir_logs)
    change_count += dir_changes

    logs.append(f"[PACKAGE] 📊 Total changes: {change_count} files/directories")
    return logs, change_count


def _replace_package_in_all_files(project_root: str, old_package: str, new_package: str) -> Tuple[List[str], int]:
    """
    프로젝트 내 모든 텍스트 파일에서 이전 패키지명을 새 패키지명으로 일괄 변경

    Args:
        project_root: 프로젝트 루트
        old_package: 이전 패키지명
        new_package: 새 패키지명

    Returns:
        (로그 메시지 리스트, 변경된 파일 수)
    """
    logs = []
    change_count = 0
    project_path = Path(project_root)

    # 텍스트 파일 확장자 (변경 대상)
    TEXT_EXTENSIONS = {
        '.xml', '.kt', '.java', '.gradle', '.kts', '.properties',
        '.json', '.txt', '.md', '.pro', '.cfg', '.config'
    }

    # 제외할 폴더
    EXCLUDE_DIRS = {'build', '.gradle', '.idea', 'outputs', '__pycache__', '.git'}

    logs.append(f"[PACKAGE] 🔍 Scanning all text files for package name replacement...")

    for file_path in project_path.rglob('*'):
        # 제외 조건 확인
        if any(excluded in file_path.parts for excluded in EXCLUDE_DIRS):
            continue

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        try:
            # 파일 읽기
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            original_content = content

            # 패키지명 일괄 치환
            content = content.replace(old_package, new_package)

            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                logs.append(f"[PACKAGE] ✅ Bulk replaced in {file_path.relative_to(project_path)}")
                change_count += 1

        except Exception as e:
            # 오류는 조용히 스킵 (바이너리 파일 등)
            continue

    if change_count > 0:
        logs.append(f"[PACKAGE] 📊 Bulk replacement: {change_count} files updated")
    else:
        logs.append(f"[PACKAGE] ℹ️ No additional files needed bulk replacement")

    return logs, change_count


def _rename_package_directories(project_root: str, old_package: str, new_package: str) -> Tuple[List[str], int]:
    """
    패키지 디렉토리 구조 변경
    src/main/java/com/example/old -> src/main/java/com/example/new
    """
    logs = []
    change_count = 0
    project_path = Path(project_root)

    old_parts = old_package.split('.')
    new_parts = new_package.split('.')

    # src/main/* 하위의 모든 소스 디렉토리 탐색
    for src_main_dir in project_path.rglob('src/main'):
        if not src_main_dir.is_dir():
            continue

        # src/main 하위의 모든 디렉토리 탐색 (java, kotlin, etc.)
        for src_dir in src_main_dir.iterdir():
            if not src_dir.is_dir():
                continue

            old_package_path = src_dir / Path(*old_parts)
            if old_package_path.exists() and old_package_path.is_dir():
                new_package_path = src_dir / Path(*new_parts)
                try:
                    # 새 패키지 부모 디렉토리 생성
                    new_package_path.parent.mkdir(parents=True, exist_ok=True)

                    # 🔥 중요: 대상 경로가 이미 존재하면 제거!
                    if new_package_path.exists():
                        shutil.rmtree(new_package_path)
                        logs.append(f"[PACKAGE] 🗑️ Removed existing: {new_package_path.relative_to(project_path)}")

                    # 이동
                    shutil.move(str(old_package_path), str(new_package_path))
                    logs.append(f"[PACKAGE] ✅ Moved directory: {old_package_path.relative_to(project_path)} -> {new_package_path.relative_to(project_path)}")
                    change_count += 1

                    # 빈 부모 디렉토리 정리
                    _cleanup_empty_dirs(src_dir)
                except Exception as e:
                    import traceback
                    logs.append(f"[PACKAGE] ❌ ERROR moving directory {old_package_path}: {str(e)}")
                    logs.append(f"[PACKAGE] Traceback: {traceback.format_exc()}")

    return logs, change_count


def _cleanup_empty_dirs(start_dir: Path):
    """빈 디렉토리 재귀 삭제 - Python 3.11 호환"""
    for dirpath, dirnames, filenames in os.walk(str(start_dir), topdown=False):
        dirpath = Path(dirpath)
        # 디렉토리가 비어있고 start_dir가 아니면 삭제
        if not list(dirpath.iterdir()) and dirpath != start_dir:
            try:
                dirpath.rmdir()
                # logs에 추가하지 않음 (너무 많은 로그 방지)
            except Exception:
                pass


def replace_app_name(project_root: str, new_app_name: str) -> Tuple[List[str], int]:
    """
    앱 이름 교체
    - res/values*/strings.xml의 <string name="app_name">
    - AndroidManifest.xml의 android:label을 @string/app_name으로 정규화
    - settings.gradle(.kts)의 rootProject.name

    Args:
        project_root: 프로젝트 루트
        new_app_name: 새 앱 이름

    Returns:
        (로그 메시지 리스트, 변경된 파일 수)
    """
    logs = []
    change_count = 0
    project_path = Path(project_root)

    logs.append(f"[APP_NAME] 🔄 Changing app name to: {new_app_name}")

    # 1. strings.xml 수정
    for strings_xml in project_path.rglob('strings.xml'):
        # More flexible check for values directory
        if not any(part.startswith('values') for part in strings_xml.parts):
            continue
        try:
            content = strings_xml.read_text(encoding='utf-8', errors='ignore')
            new_content = re.sub(
                r'(<string\s+name="app_name">)[^<]+(</string>)',
                r'\1' + new_app_name + r'\2',
                content
            )
            if new_content != content:
                strings_xml.write_text(new_content, encoding='utf-8')
                logs.append(f"[APP_NAME] ✅ Updated app_name in {strings_xml.relative_to(project_path)}")
                change_count += 1
        except Exception as e:
            import traceback
            logs.append(f"[APP_NAME] ❌ ERROR updating {strings_xml}: {str(e)}")
            logs.append(f"[APP_NAME] Traceback: {traceback.format_exc()}")

    # 2. AndroidManifest.xml 정규화
    for manifest in project_path.rglob('AndroidManifest.xml'):
        try:
            content = manifest.read_text(encoding='utf-8', errors='ignore')
            # android:label을 @string/app_name으로 교체
            new_content = re.sub(
                r'android:label="[^"]*"',
                r'android:label="@string/app_name"',
                content
            )
            if new_content != content:
                manifest.write_text(new_content, encoding='utf-8')
                logs.append(f"[APP_NAME] ✅ Normalized android:label in {manifest.relative_to(project_path)}")
                change_count += 1
        except Exception as e:
            import traceback
            logs.append(f"[APP_NAME] ❌ ERROR updating {manifest}: {str(e)}")
            logs.append(f"[APP_NAME] Traceback: {traceback.format_exc()}")

    # 3. settings.gradle(.kts) rootProject.name 수정
    for settings_file in project_path.glob('settings.gradle*'):
        try:
            content = settings_file.read_text(encoding='utf-8', errors='ignore')
            original_content = content

            # rootProject.name = "..." 형태 (Groovy/Kotlin DSL 모두 지원)
            new_content = re.sub(
                r'(rootProject\.name\s*=\s*["\'])[^"\']+(["\'])',
                r'\1' + new_app_name + r'\2',
                content
            )

            if new_content != original_content:
                settings_file.write_text(new_content, encoding='utf-8')
                logs.append(f"[APP_NAME] ✅ Updated rootProject.name in {settings_file.relative_to(project_path)}")
                change_count += 1
        except Exception as e:
            import traceback
            logs.append(f"[APP_NAME] ❌ ERROR updating {settings_file}: {str(e)}")
            logs.append(f"[APP_NAME] Traceback: {traceback.format_exc()}")

    logs.append(f"[APP_NAME] 📊 Total changes: {change_count} files")
    return logs, change_count


def reset_version(project_root: str) -> Tuple[List[str], int]:
    """
    버전 정보 초기화
    - versionCode = 1
    - versionName = "1.0.0"
    - productFlavors/buildTypes 내 중복 제거

    Args:
        project_root: 프로젝트 루트

    Returns:
        (로그 메시지 리스트, 변경된 파일 수)
    """
    logs = []
    change_count = 0
    project_path = Path(project_root)

    logs.append("[VERSION] 🔄 Resetting version to 1.0.0")

    for gradle_file in project_path.rglob('build.gradle*'):
        try:
            content = gradle_file.read_text(encoding='utf-8', errors='ignore')
            original_content = content

            # versionCode (Groovy)
            content = re.sub(
                r'versionCode\s+\d+',
                r'versionCode 1',
                content
            )

            # versionCode = ... (Kotlin DSL)
            content = re.sub(
                r'versionCode\s*=\s*\d+',
                r'versionCode = 1',
                content
            )

            # versionName (Groovy)
            content = re.sub(
                r'versionName\s+["\'][^"\']*["\']',
                r'versionName "1.0.0"',
                content
            )

            # versionName = "..." (Kotlin DSL)
            content = re.sub(
                r'versionName\s*=\s*["\'][^"\']*["\']',
                r'versionName = "1.0.0"',
                content
            )

            if content != original_content:
                gradle_file.write_text(content, encoding='utf-8')
                logs.append(f"[VERSION] ✅ Reset to versionCode=1, versionName=1.0.0 in {gradle_file.relative_to(project_path)}")
                change_count += 1
        except Exception as e:
            import traceback
            logs.append(f"[VERSION] ❌ ERROR updating {gradle_file}: {str(e)}")
            logs.append(f"[VERSION] Traceback: {traceback.format_exc()}")

    logs.append(f"[VERSION] 📊 Total changes: {change_count} files")
    return logs, change_count
