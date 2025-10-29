"""
BASE_URL 문자열 교체
"""
import re
from pathlib import Path
from typing import List


def replace_base_url(project_root: str, old_url: str, new_url: str) -> List[str]:
    """
    프로젝트 전체에서 BASE_URL 관련 문자열 교체
    - build.gradle(.kts)의 buildConfigField "BASE_URL"
    - Kotlin/Java의 const val BASE_URL / static final String BASE_URL
    - strings.xml의 <string name="base_url">

    Args:
        project_root: 프로젝트 루트
        old_url: 기존 URL (선택, 탐지용)
        new_url: 새 URL

    Returns:
        로그 메시지 리스트
    """
    logs = []

    if not new_url:
        logs.append("[BASE_URL] No new BASE_URL provided, skipping")
        return logs

    project_path = Path(project_root)
    replaced_count = 0

    # 1. build.gradle(.kts) 수정
    for gradle_file in project_path.rglob('build.gradle*'):
        try:
            content = gradle_file.read_text(encoding='utf-8', errors='ignore')
            original_content = content

            # buildConfigField "BASE_URL", "..." 형태 찾아서 교체
            new_content = re.sub(
                r'(buildConfigField\s*\(\s*["\']String["\']\s*,\s*["\']BASE_URL["\']\s*,\s*["\'])[^"\']+(["\'])',
                r'\1' + new_url + r'\2',
                content
            )
            # Groovy 스타일: buildConfigField "String", "BASE_URL", "..."
            new_content = re.sub(
                r'(buildConfigField\s+["\']String["\']\s*,\s*["\']BASE_URL["\']\s*,\s*["\'])[^"\']+(["\'])',
                r'\1' + new_url + r'\2',
                new_content
            )

            if new_content != original_content:
                gradle_file.write_text(new_content, encoding='utf-8')
                logs.append(f"[BASE_URL] Updated buildConfigField in {gradle_file.relative_to(project_path)}")
                replaced_count += 1
        except Exception as e:
            logs.append(f"[BASE_URL] ERROR updating {gradle_file}: {str(e)}")

    # 2. Kotlin/Java 소스 파일 수정
    source_files = list(project_path.rglob('*.kt')) + list(project_path.rglob('*.java'))
    for source_file in source_files:
        if 'build' in source_file.parts:
            continue
        try:
            content = source_file.read_text(encoding='utf-8', errors='ignore')
            original_content = content

            # Kotlin: const val BASE_URL = "..."
            new_content = re.sub(
                r'(const\s+val\s+BASE_URL\s*=\s*["\'])[^"\']+(["\'])',
                r'\1' + new_url + r'\2',
                content
            )
            # Java: static final String BASE_URL = "...";
            new_content = re.sub(
                r'(static\s+final\s+String\s+BASE_URL\s*=\s*["\'])[^"\']+(["\'])',
                r'\1' + new_url + r'\2',
                new_content
            )
            # 일반 변수: val BASE_URL = "..."
            new_content = re.sub(
                r'(val\s+BASE_URL\s*=\s*["\'])[^"\']+(["\'])',
                r'\1' + new_url + r'\2',
                new_content
            )

            if new_content != original_content:
                source_file.write_text(new_content, encoding='utf-8')
                logs.append(f"[BASE_URL] Updated constant in {source_file.relative_to(project_path)}")
                replaced_count += 1
        except Exception as e:
            logs.append(f"[BASE_URL] ERROR updating {source_file}: {str(e)}")

    # 3. strings.xml 수정
    for strings_xml in project_path.rglob('strings.xml'):
        if 'values' not in strings_xml.parts:
            continue
        try:
            content = strings_xml.read_text(encoding='utf-8', errors='ignore')
            original_content = content

            # <string name="base_url">...</string>
            new_content = re.sub(
                r'(<string\s+name="base_url">)[^<]+(</string>)',
                r'\1' + new_url + r'\2',
                content
            )
            # <string name="BASE_URL">...</string>
            new_content = re.sub(
                r'(<string\s+name="BASE_URL">)[^<]+(</string>)',
                r'\1' + new_url + r'\2',
                new_content
            )

            if new_content != original_content:
                strings_xml.write_text(new_content, encoding='utf-8')
                logs.append(f"[BASE_URL] Updated base_url in {strings_xml.relative_to(project_path)}")
                replaced_count += 1
        except Exception as e:
            logs.append(f"[BASE_URL] ERROR updating {strings_xml}: {str(e)}")

    if replaced_count == 0:
        logs.append("[BASE_URL] WARNING: No BASE_URL definitions found")
    else:
        logs.append(f"[BASE_URL] Successfully replaced BASE_URL in {replaced_count} files")

    return logs
