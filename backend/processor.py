"""
Android 프로젝트 리빌드 전체 파이프라인
"""
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List

from backend.utils.zip_tools import extract_zip, create_zip, get_app_module_path
from backend.utils.cleanup import clean_build_artifacts
from backend.utils.file_replace import (
    detect_old_package_name,
    replace_package_name,
    replace_app_name,
    reset_version
)
from backend.utils.firebase import replace_google_services
from backend.utils.icon_replace import replace_app_icon
from backend.utils.baseurl_replace import replace_base_url


class AndroidProjectProcessor:
    """Android 프로젝트 리빌드 프로세서"""

    def __init__(self):
        self.logs: List[str] = []
        self.temp_dir = None
        self.project_root = None

    def process(
        self,
        zip_path: str,
        new_package: str,
        new_app_name: str,
        google_services_path: str = None,
        icon_path: str = None,
        splash_path: str = None,
        new_base_url: str = None,
        include_log: bool = True
    ) -> Dict:
        """
        전체 리빌드 프로세스 실행

        Args:
            zip_path: 업로드된 프로젝트 ZIP 경로
            new_package: 새 패키지명
            new_app_name: 새 앱 이름
            google_services_path: google-services.json 경로 (선택)
            icon_path: 앱 아이콘 이미지 경로 (선택)
            splash_path: 스플래시 이미지 경로 (선택)
            new_base_url: 새 BASE_URL (선택)
            include_log: 로그 파일 포함 여부 (기본: True)

        Returns:
            {
                'success': bool,
                'output_zip': str,
                'logs': List[str]
            }
        """
        try:
            self.logs.append("=" * 60)
            self.logs.append("Android Project Rebuilder - Processing Started")
            self.logs.append("=" * 60)

            # 1. 임시 디렉토리 생성
            self.temp_dir = tempfile.mkdtemp(prefix='android_rebuild_')
            self.logs.append(f"[INIT] Created temp directory: {self.temp_dir}")

            # 2. ZIP 압축 해제
            self.logs.append("\n--- Step 1: Extract ZIP ---")
            self.project_root, extract_logs = extract_zip(zip_path, self.temp_dir)
            self.logs.extend(extract_logs)

            # 3. 빌드 아티팩트 정리
            self.logs.append("\n--- Step 2: Clean Build Artifacts ---")
            cleanup_logs = clean_build_artifacts(self.project_root)
            self.logs.extend(cleanup_logs)

            # 4. app 모듈 탐지
            self.logs.append("\n--- Step 3: Detect App Module ---")
            app_module, detect_logs = get_app_module_path(self.project_root)
            self.logs.extend(detect_logs)

            # 5. 기존 패키지명 탐지
            self.logs.append("\n--- Step 4: Detect Old Package ---")
            old_package, pkg_detect_logs = detect_old_package_name(app_module)
            self.logs.extend(pkg_detect_logs)

            # 6. 패키지명 교체
            self.logs.append("\n--- Step 5: Replace Package Name ---")
            if old_package:
                pkg_logs, pkg_changes = replace_package_name(self.project_root, old_package, new_package)
                self.logs.extend(pkg_logs)
                if pkg_changes == 0:
                    self.logs.append("[PACKAGE] ⚠️ WARNING: No changes were made!")
            else:
                self.logs.append("[PACKAGE] Skipped (old package not detected)")

            # 7. 앱 이름 교체
            self.logs.append("\n--- Step 6: Replace App Name ---")
            app_name_logs, app_name_changes = replace_app_name(self.project_root, new_app_name)
            self.logs.extend(app_name_logs)
            if app_name_changes == 0:
                self.logs.append("[APP_NAME] ⚠️ WARNING: No changes were made!")

            # 8. 버전 초기화
            self.logs.append("\n--- Step 7: Reset Version ---")
            version_logs, version_changes = reset_version(self.project_root)
            self.logs.extend(version_logs)
            if version_changes == 0:
                self.logs.append("[VERSION] ⚠️ WARNING: No changes were made!")

            # 9. Firebase 설정 교체
            self.logs.append("\n--- Step 8: Replace Firebase Config ---")
            firebase_logs = replace_google_services(
                self.project_root,
                google_services_path,
                old_package,
                new_package
            )
            self.logs.extend(firebase_logs)

            # 10. 앱 아이콘 및 스플래시 이미지 교체
            self.logs.append("\n--- Step 9: Replace App Icon & Splash ---")
            icon_logs = replace_app_icon(self.project_root, icon_path, splash_path)
            self.logs.extend(icon_logs)

            # 11. BASE_URL 교체
            self.logs.append("\n--- Step 10: Replace BASE_URL ---")
            baseurl_logs = replace_base_url(self.project_root, None, new_base_url)
            self.logs.extend(baseurl_logs)

            # 12. 결과 ZIP 생성
            self.logs.append("\n--- Step 11: Create Output ZIP ---")
            output_zip = Path(self.temp_dir) / 'rebuilt_project.zip'

            # 로그 파일 포함 여부에 따라 log_content 설정
            log_content = '\n'.join(self.logs) if include_log else None
            if not include_log:
                self.logs.append("[ZIP] Log file will not be included in output")

            zip_logs = create_zip(self.project_root, str(output_zip), log_content, new_app_name)
            self.logs.extend(zip_logs)

            self.logs.append("\n" + "=" * 60)
            self.logs.append("Processing Completed Successfully")
            self.logs.append("=" * 60)

            return {
                'success': True,
                'output_zip': str(output_zip),
                'logs': self.logs
            }

        except Exception as e:
            error_msg = f"[ERROR] Processing failed: {str(e)}"
            self.logs.append(error_msg)
            return {
                'success': False,
                'output_zip': None,
                'logs': self.logs,
                'error': str(e)
            }

    def cleanup(self):
        """임시 디렉토리 정리"""
        if self.temp_dir and Path(self.temp_dir).exists():
            try:
                shutil.rmtree(self.temp_dir)
                self.logs.append(f"[CLEANUP] Removed temp directory: {self.temp_dir}")
            except Exception as e:
                self.logs.append(f"[CLEANUP] Failed to remove temp directory: {str(e)}")
