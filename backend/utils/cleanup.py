"""
불필요한 빌드 아티팩트 및 캐시 폴더 삭제
"""
import shutil
from pathlib import Path
from typing import List


def clean_build_artifacts(project_root: str) -> List[str]:
    """
    build/, .gradle/, .idea/, outputs/ 등 불필요한 폴더 삭제

    Args:
        project_root: 프로젝트 루트 디렉토리

    Returns:
        로그 메시지 리스트
    """
    logs = []
    project_path = Path(project_root)

    # 삭제할 폴더 패턴
    CLEANUP_TARGETS = [
        'build',
        '.gradle',
        '.idea',
        'outputs',
        '.externalNativeBuild',
        '.cxx',
        'captures',
        'local.properties'
    ]

    deleted_count = 0

    for target in CLEANUP_TARGETS:
        for item in project_path.rglob(target):
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                    logs.append(f"[CLEANUP] Deleted directory: {item.relative_to(project_path)}")
                    deleted_count += 1
                elif item.is_file():
                    item.unlink()
                    logs.append(f"[CLEANUP] Deleted file: {item.relative_to(project_path)}")
                    deleted_count += 1
            except Exception as e:
                logs.append(f"[CLEANUP] Failed to delete {item}: {str(e)}")

    if deleted_count == 0:
        logs.append("[CLEANUP] No build artifacts found")
    else:
        logs.append(f"[CLEANUP] Total deleted: {deleted_count} items")

    return logs
