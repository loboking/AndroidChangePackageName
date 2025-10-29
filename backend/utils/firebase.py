"""
Firebase google-services.json 교체 및 패키지명 변경
"""
import shutil
import json
from pathlib import Path
from typing import List, Optional


def replace_google_services(
    project_root: str,
    google_services_path: str,
    old_package: Optional[str] = None,
    new_package: Optional[str] = None
) -> List[str]:
    """
    google-services.json을 app 모듈의 여러 위치에 교체하고 패키지명 변경

    Args:
        project_root: 프로젝트 루트
        google_services_path: 새 google-services.json 파일 경로
        old_package: 이전 패키지명 (패키지명 변경 시)
        new_package: 새 패키지명 (패키지명 변경 시)

    Returns:
        로그 메시지 리스트
    """
    logs = []

    if not google_services_path or not Path(google_services_path).exists():
        logs.append("[FIREBASE] No google-services.json provided, skipping")
        return logs

    project_path = Path(project_root)

    # 프로젝트 내 기존 google-services.json 파일들을 모두 찾기
    existing_files = list(project_path.rglob('google-services.json'))

    # 제외할 폴더 (build 등)
    EXCLUDE_DIRS = {'build', '.gradle', 'outputs'}
    existing_files = [f for f in existing_files
                     if not any(excluded in f.parts for excluded in EXCLUDE_DIRS)]

    if not existing_files:
        # 기존 파일이 없으면 기본 위치들에 배치
        logs.append("[FIREBASE] No existing google-services.json found, placing in default locations")

        # app 모듈 찾기
        app_module = project_path / 'app'
        if not app_module.exists():
            for gradle_file in project_path.rglob('build.gradle*'):
                app_module = gradle_file.parent
                if (app_module / 'src').exists():
                    break

        target_locations = [
            app_module / 'google-services.json',
            app_module / 'src' / 'debug' / 'google-services.json',
            app_module / 'src' / 'release' / 'google-services.json',
        ]
    else:
        # 기존 파일이 있는 위치들을 타겟으로 사용
        target_locations = existing_files
        logs.append(f"[FIREBASE] Found {len(existing_files)} existing google-services.json file(s)")

    replaced_count = 0

    for target_path in target_locations:
        try:
            # 부모 디렉토리가 없으면 생성
            target_path.parent.mkdir(parents=True, exist_ok=True)

            # 패키지명 변경이 필요한 경우
            if old_package and new_package:
                # JSON 파일 읽기
                with open(google_services_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # 패키지명 변경
                modified = _update_package_in_json(data, old_package, new_package)

                # 변경된 내용 저장
                with open(target_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                if modified:
                    logs.append(f"[FIREBASE] ✅ Updated & placed at {target_path.relative_to(project_path)} (package changed)")
                else:
                    logs.append(f"[FIREBASE] ✅ Placed at {target_path.relative_to(project_path)} (no package match found)")

            else:
                # 패키지명 변경 없이 그대로 복사
                shutil.copy2(google_services_path, target_path)
                logs.append(f"[FIREBASE] ✅ Placed at {target_path.relative_to(project_path)}")

            replaced_count += 1

        except Exception as e:
            logs.append(f"[FIREBASE] ❌ ERROR placing at {target_path.relative_to(project_path)}: {str(e)}")

    if replaced_count == 0:
        logs.append("[FIREBASE] ⚠️ WARNING: No files were placed")
    else:
        logs.append(f"[FIREBASE] 📊 Successfully placed {replaced_count} google-services.json file(s)")

    return logs


def _update_package_in_json(data: dict, old_package: str, new_package: str) -> bool:
    """
    JSON 데이터 내에서 패키지명을 재귀적으로 변경

    Args:
        data: JSON 데이터 (dict 또는 list)
        old_package: 이전 패키지명
        new_package: 새 패키지명

    Returns:
        변경이 발생했는지 여부
    """
    modified = False

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and value == old_package:
                data[key] = new_package
                modified = True
            elif isinstance(value, (dict, list)):
                if _update_package_in_json(value, old_package, new_package):
                    modified = True

    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, str) and item == old_package:
                data[i] = new_package
                modified = True
            elif isinstance(item, (dict, list)):
                if _update_package_in_json(item, old_package, new_package):
                    modified = True

    return modified
