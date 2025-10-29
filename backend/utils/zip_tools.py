"""
ZIP 압축 해제 및 재압축 유틸리티
"""
import zipfile
import os
from pathlib import Path
from typing import List


def extract_zip(zip_path: str, extract_to: str) -> str:
    """
    ZIP 파일을 지정된 경로에 압축 해제

    Args:
        zip_path: ZIP 파일 경로
        extract_to: 압축 해제 대상 디렉토리

    Returns:
        압축 해제된 프로젝트 루트 디렉토리 경로
    """
    logs = []

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        logs.append(f"[ZIP] Extracted {len(zip_ref.namelist())} files to {extract_to}")

    # 압축 해제 후 실제 프로젝트 루트 찾기
    # __MACOSX와 같은 시스템 폴더는 무시
    items = [item for item in Path(extract_to).iterdir()
             if item.name not in {'__MACOSX', '.DS_Store', 'Thumbs.db'} and item.is_dir()]

    # 단일 폴더가 있는 경우, 그 폴더 내부를 확인
    if len(items) == 1:
        candidate = items[0]

        # 해당 폴더 내부에 build.gradle이나 settings.gradle이 있는지 확인
        has_gradle_root = any((candidate / name).exists()
                             for name in ['build.gradle', 'build.gradle.kts', 'settings.gradle', 'settings.gradle.kts'])

        if has_gradle_root:
            # Gradle 프로젝트 루트 파일이 있으면 해당 폴더를 루트로 사용
            project_root = str(candidate)
            logs.append(f"[ZIP] Detected project root: {project_root}")
        else:
            # Gradle 파일이 없으면, 하위 폴더 중 Gradle 프로젝트 찾기
            sub_items = [item for item in candidate.iterdir()
                        if item.is_dir() and item.name not in {'__MACOSX', '.DS_Store'}]

            gradle_projects = []
            for sub_item in sub_items:
                if any((sub_item / name).exists()
                      for name in ['build.gradle', 'build.gradle.kts', 'settings.gradle', 'settings.gradle.kts']):
                    gradle_projects.append(sub_item)

            if len(gradle_projects) == 1:
                # 하위에 Gradle 프로젝트가 하나만 있으면 그것을 루트로 사용
                project_root = str(gradle_projects[0])
                logs.append(f"[ZIP] Detected nested project root: {project_root}")
            else:
                # 여러 개이거나 없으면 최상위 폴더 사용
                project_root = str(candidate)
                logs.append(f"[ZIP] Using top folder as project root: {project_root}")
    else:
        project_root = extract_to
        logs.append(f"[ZIP] Using extract directory as project root: {project_root}")

    return project_root, logs


def create_zip(source_dir: str, output_zip: str, log_content: str = None, new_folder_name: str = None) -> List[str]:
    """
    디렉토리를 ZIP 파일로 압축

    Args:
        source_dir: 압축할 디렉토리
        output_zip: 생성할 ZIP 파일 경로
        log_content: ANDROID_REBUILDER_LOG.txt 내용 (있으면 포함)
        new_folder_name: ZIP 내부의 새 폴더명 (있으면 루트 폴더명 변경)

    Returns:
        로그 메시지 리스트
    """
    logs = []
    file_count = 0

    # 제외할 폴더 및 파일 패턴
    EXCLUDE_DIRS = {'build', '.gradle', '.idea', 'outputs', '__pycache__', '.git'}
    EXCLUDE_FILES = {'.DS_Store', 'Thumbs.db'}

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        source_path = Path(source_dir)

        # 로그 파일 추가 (루트 또는 새 폴더 내부)
        if log_content:
            if new_folder_name:
                zipf.writestr(f'{new_folder_name}/ANDROID_REBUILDER_LOG.txt', log_content)
            else:
                zipf.writestr('ANDROID_REBUILDER_LOG.txt', log_content)
            logs.append("[ZIP] Added ANDROID_REBUILDER_LOG.txt to ZIP")

        # 모든 파일 순회하며 압축
        for file_path in source_path.rglob('*'):
            # 제외 조건 확인
            if any(excluded in file_path.parts for excluded in EXCLUDE_DIRS):
                continue
            if file_path.name in EXCLUDE_FILES:
                continue
            if not file_path.is_file():
                continue

            # 상대 경로로 압축
            relative_path = file_path.relative_to(source_path)

            # 새 폴더명이 지정되면 경로 앞에 추가
            if new_folder_name:
                archive_path = Path(new_folder_name) / relative_path
            else:
                archive_path = relative_path

            zipf.write(file_path, archive_path)
            file_count += 1

    if new_folder_name:
        logs.append(f"[ZIP] Created {output_zip} with {file_count} files (folder: {new_folder_name})")
    else:
        logs.append(f"[ZIP] Created {output_zip} with {file_count} files")
    return logs


def get_app_module_path(project_root: str) -> tuple:
    """
    Android 프로젝트에서 app 모듈 경로 탐지

    Args:
        project_root: 프로젝트 루트 디렉토리

    Returns:
        (app_module_path, logs)
    """
    logs = []
    project_path = Path(project_root)

    # 1순위: app 디렉토리
    app_dir = project_path / 'app'
    if app_dir.exists() and (app_dir / 'src' / 'main').exists():
        logs.append(f"[DETECT] Found app module at: {app_dir}")
        return str(app_dir), logs

    # 2순위: build.gradle(.kts) + src/main 조합
    for gradle_file in project_path.rglob('build.gradle*'):
        module_dir = gradle_file.parent
        if (module_dir / 'src' / 'main').exists():
            logs.append(f"[DETECT] Found app module at: {module_dir}")
            return str(module_dir), logs

    logs.append("[DETECT] WARNING: Could not detect app module, using project root")
    return project_root, logs
