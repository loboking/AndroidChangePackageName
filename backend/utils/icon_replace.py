"""
앱 아이콘 교체 (자동 리사이징)
"""
import re
import shutil
from pathlib import Path
from typing import List, Dict

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


# Android 아이콘 해상도 매핑
ICON_SIZES: Dict[str, int] = {
    'mdpi': 48,
    'hdpi': 72,
    'xhdpi': 96,
    'xxhdpi': 144,
    'xxxhdpi': 192,
}


def replace_app_icon(project_root: str, icon_path: str, splash_path: str = None) -> List[str]:
    """
    업로드된 아이콘 이미지를 각 해상도에 맞게 리사이징하여 mipmap-* 폴더에 저장
    스플래시 이미지도 함께 처리

    Args:
        project_root: 프로젝트 루트
        icon_path: 새 아이콘 이미지 경로 (PNG/JPG, 권장: 512x512 이상)
        splash_path: 스플래시 이미지 경로 (PNG/JPG, 선택)

    Returns:
        로그 메시지 리스트
    """
    logs = []

    if not icon_path or not Path(icon_path).exists():
        logs.append("[ICON] No icon image provided, skipping")
        return logs

    if not PILLOW_AVAILABLE:
        logs.append("[ICON] ERROR: Pillow library not installed, cannot resize images")
        logs.append("[ICON] Please install: pip install Pillow")
        return logs

    project_path = Path(project_root)
    icon_file = Path(icon_path)

    # 원본 이미지 열기
    try:
        original_image = Image.open(icon_file)
        logs.append(f"[ICON] Loaded original image: {original_image.size[0]}x{original_image.size[1]}")

        # RGBA 모드로 변환 (투명도 지원)
        if original_image.mode != 'RGBA':
            original_image = original_image.convert('RGBA')
    except Exception as e:
        logs.append(f"[ICON] ERROR: Failed to open image: {str(e)}")
        return logs

    # app/src/main/res 디렉토리 찾기
    res_dirs = list(project_path.rglob('src/main/res'))
    if not res_dirs:
        logs.append("[ICON] ERROR: res directory not found")
        return logs

    res_dir = res_dirs[0]

    # 교체할 아이콘 파일 목록 (모든 런처 아이콘 파일)
    icon_targets = [
        'ic_launcher.png',
        'ic_launcher_round.png',
        'ic_launcher_background.png',
        'ic_launcher_foreground.png',
        'ic_launcher_monochrome.png'
    ]

    replaced_count = 0

    # mipmap-* 폴더 순회
    for density, size in ICON_SIZES.items():
        mipmap_dir = res_dir / f'mipmap-{density}'

        # mipmap 디렉토리가 없으면 생성
        if not mipmap_dir.exists():
            mipmap_dir.mkdir(parents=True, exist_ok=True)
            logs.append(f"[ICON] Created directory: {mipmap_dir.relative_to(project_path)}")

        # 해당 해상도로 리사이징
        try:
            resized_image = original_image.resize((size, size), Image.Resampling.LANCZOS)

            for icon_name in icon_targets:
                target_path = mipmap_dir / icon_name

                # 파일이 존재하지 않으면 스킵 (선택적 교체)
                # 단, ic_launcher와 ic_launcher_round는 항상 생성
                if not target_path.exists() and icon_name not in ['ic_launcher.png', 'ic_launcher_round.png']:
                    continue

                try:
                    # PNG로 저장
                    resized_image.save(target_path, 'PNG')
                    logs.append(f"[ICON] ✅ Created {density} ({size}x{size}): {target_path.relative_to(project_path)}")
                    replaced_count += 1
                except Exception as e:
                    logs.append(f"[ICON] ❌ ERROR saving to {target_path}: {str(e)}")
        except Exception as e:
            logs.append(f"[ICON] ❌ ERROR resizing for {density}: {str(e)}")

    if replaced_count == 0:
        logs.append("[ICON] ⚠️ WARNING: No icon files were created")
    else:
        logs.append(f"[ICON] 📊 Successfully created {replaced_count} icon files across all densities")

    # AndroidManifest.xml 아이콘 참조 수정
    manifest_logs = _update_manifest_icon_references(project_path)
    logs.extend(manifest_logs)

    # 스플래시 이미지 처리
    if splash_path and Path(splash_path).exists():
        splash_logs = _replace_splash_image(project_path, splash_path)
        logs.extend(splash_logs)

    return logs


def _replace_splash_image(project_path: Path, splash_path: str) -> List[str]:
    """
    스플래시 이미지를 각 해상도에 맞게 리사이징하여 mipmap-* 폴더에 저장

    Args:
        project_path: 프로젝트 루트
        splash_path: 스플래시 이미지 경로 (PNG/JPG)

    Returns:
        로그 메시지 리스트
    """
    logs = []
    splash_file = Path(splash_path)

    # 원본 이미지 열기
    try:
        splash_image = Image.open(splash_file)
        logs.append(f"[SPLASH] Loaded splash image: {splash_image.size[0]}x{splash_image.size[1]}")

        # RGBA 모드로 변환
        if splash_image.mode != 'RGBA':
            splash_image = splash_image.convert('RGBA')
    except Exception as e:
        logs.append(f"[SPLASH] ERROR: Failed to open splash image: {str(e)}")
        return logs

    # res 디렉토리 찾기
    res_dirs = list(project_path.rglob('src/main/res'))
    if not res_dirs:
        logs.append("[SPLASH] ERROR: res directory not found")
        return logs

    res_dir = res_dirs[0]
    splash_filename = 'splash_screen.png'
    replaced_count = 0

    # mipmap-* 폴더 순회하여 스플래시 이미지 저장
    for density, size in ICON_SIZES.items():
        mipmap_dir = res_dir / f'mipmap-{density}'

        if not mipmap_dir.exists():
            mipmap_dir.mkdir(parents=True, exist_ok=True)
            logs.append(f"[SPLASH] Created directory: {mipmap_dir.relative_to(project_path)}")

        try:
            # 해상도별 리사이징
            resized_splash = splash_image.resize((size, size), Image.Resampling.LANCZOS)
            target_path = mipmap_dir / splash_filename

            # PNG로 저장
            resized_splash.save(target_path, 'PNG')
            logs.append(f"[SPLASH] ✅ Created {density} ({size}x{size}): {target_path.relative_to(project_path)}")
            replaced_count += 1
        except Exception as e:
            logs.append(f"[SPLASH] ❌ ERROR creating splash for {density}: {str(e)}")

    if replaced_count == 0:
        logs.append("[SPLASH] ⚠️ WARNING: No splash images were created")
    else:
        logs.append(f"[SPLASH] 📊 Successfully created {replaced_count} splash images across all densities")

    # layout XML 파일에서 스플래시 이미지 참조 업데이트
    layout_logs = _update_splash_references_in_layouts(project_path, splash_filename)
    logs.extend(layout_logs)

    return logs


def _update_splash_references_in_layouts(project_path: Path, splash_filename: str) -> List[str]:
    """
    layout XML 파일에서 스플래시 이미지 참조를 새로운 파일명으로 업데이트

    Args:
        project_path: 프로젝트 루트
        splash_filename: 새 스플래시 이미지 파일명 (확장자 제외)

    Returns:
        로그 메시지 리스트
    """
    logs = []
    splash_name_without_ext = splash_filename.replace('.png', '')

    # layout 디렉토리 찾기
    layout_dirs = list(project_path.rglob('src/main/res/layout*'))
    if not layout_dirs:
        logs.append("[SPLASH] ⚠️ WARNING: No layout directories found")
        return logs

    updated_files = 0

    for layout_dir in layout_dirs:
        if not layout_dir.is_dir():
            continue

        # layout XML 파일들 순회
        for xml_file in layout_dir.glob('*.xml'):
            try:
                content = xml_file.read_text(encoding='utf-8', errors='ignore')
                original_content = content

                # @mipmap/xxx 형태의 스플래시 참조를 찾아서 교체
                # android:src="@mipmap/기존이름" -> android:src="@mipmap/splash_screen"
                # id가 splash인 ImageView를 찾아서 src 속성 업데이트
                pattern = r'(<ImageView[^>]*android:id="@\+?id/splash"[^>]*android:src=")@mipmap/[^"]*(")'
                if re.search(pattern, content):
                    content = re.sub(pattern, rf'\1@mipmap/{splash_name_without_ext}\2', content)

                # 반대 순서 (src가 id보다 먼저 오는 경우)
                pattern2 = r'(<ImageView[^>]*android:src=")@mipmap/[^"]*("[^>]*android:id="@\+?id/splash")'
                if re.search(pattern2, content):
                    content = re.sub(pattern2, rf'\1@mipmap/{splash_name_without_ext}\2', content)

                if content != original_content:
                    xml_file.write_text(content, encoding='utf-8')
                    logs.append(f"[SPLASH] ✅ Updated splash reference in {xml_file.relative_to(project_path)}")
                    updated_files += 1

            except Exception as e:
                import traceback
                logs.append(f"[SPLASH] ❌ ERROR updating {xml_file}: {str(e)}")
                logs.append(f"[SPLASH] Traceback: {traceback.format_exc()}")

    if updated_files == 0:
        logs.append("[SPLASH] ℹ️ No splash references found in layout files")
    else:
        logs.append(f"[SPLASH] 📊 Updated {updated_files} layout file(s)")

    return logs


def _update_manifest_icon_references(project_path: Path) -> List[str]:
    """
    AndroidManifest.xml에서 아이콘 참조를 ic_launcher로 통일

    Args:
        project_path: 프로젝트 루트

    Returns:
        로그 메시지 리스트
    """
    logs = []

    # AndroidManifest.xml 파일 찾기
    manifests = list(project_path.rglob('AndroidManifest.xml'))
    if not manifests:
        logs.append("[ICON] ⚠️ WARNING: No AndroidManifest.xml found")
        return logs

    for manifest in manifests:
        try:
            content = manifest.read_text(encoding='utf-8', errors='ignore')
            original_content = content

            # android:icon 속성 수정
            content = re.sub(
                r'android:icon="@mipmap/[^"]*"',
                r'android:icon="@mipmap/ic_launcher"',
                content
            )

            # android:roundIcon 속성 수정
            content = re.sub(
                r'android:roundIcon="@mipmap/[^"]*"',
                r'android:roundIcon="@mipmap/ic_launcher_round"',
                content
            )

            if content != original_content:
                manifest.write_text(content, encoding='utf-8')
                logs.append(f"[ICON] ✅ Updated icon references in {manifest.relative_to(project_path)}")
            else:
                logs.append(f"[ICON] ℹ️ No icon reference changes needed in {manifest.relative_to(project_path)}")

        except Exception as e:
            import traceback
            logs.append(f"[ICON] ❌ ERROR updating {manifest}: {str(e)}")
            logs.append(f"[ICON] Traceback: {traceback.format_exc()}")

    return logs
