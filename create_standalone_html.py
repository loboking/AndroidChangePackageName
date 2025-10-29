#!/usr/bin/env python3
"""
Create standalone HTML by modifying the original index.html
"""

import sys

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace file inputs with button-based file selection
replacements = [
    # Project ZIP
    (
        '<input type="file" id="projectZip" accept=".zip" required>',
        '<button type="button" class="file-select-btn" onclick="selectZipFile()">📁 ZIP 파일 선택</button>\n                <input type="hidden" id="projectZipPath">'
    ),
    (
        '<div class="file-info">압축된 Android 프로젝트 파일을 선택하세요</div>',
        '<div class="file-info" id="zipFileInfo">압축된 Android 프로젝트 파일을 선택하세요</div>'
    ),
    # Google Services
    (
        '<input type="file" id="googleServices" accept=".json">',
        '<button type="button" class="file-select-btn" onclick="selectGoogleServicesFile()">📄 JSON 파일 선택</button>\n                <input type="hidden" id="googleServicesPath">'
    ),
    (
        '<div class="file-info">Firebase 설정 파일 (선택)</div>',
        '<div class="file-info" id="googleServicesInfo">Firebase 설정 파일 (선택)</div>'
    ),
    # App Icon
    (
        '<input type="file" id="appIcon" accept="image/*">',
        '<button type="button" class="file-select-btn" onclick="selectAppIconFile()">🖼️ 아이콘 선택</button>\n                <input type="hidden" id="appIconPath">'
    ),
    (
        '<div class="file-info">PNG 또는 JPG 형식 (모든 해상도에 적용)</div>',
        '<div class="file-info" id="appIconInfo">PNG 또는 JPG 형식 (모든 해상도에 적용)</div>'
    ),
    # Splash Image
    (
        '<input type="file" id="splashImage" accept="image/*">',
        '<button type="button" class="file-select-btn" onclick="selectSplashFile()">🖼️ 스플래시 선택</button>\n                <input type="hidden" id="splashPath">'
    ),
    (
        '<div class="file-info">PNG 또는 JPG 형식 - 스플래시 화면에 사용되는 이미지</div>',
        '<div class="file-info" id="splashInfo">PNG 또는 JPG 형식 - 스플래시 화면에 사용되는 이미지</div>'
    ),
]

# Apply replacements
for old, new in replacements:
    html = html.replace(old, new)

# Add CSS for file-select-btn
css_insert = """
        .file-select-btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 600;
        }

        .file-select-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }

"""

# Insert CSS before </style>
html = html.replace('    </style>', css_insert + '    </style>')

# Replace the inline script with external standalone.js
# Find script tag and replace everything between <script> and </script>
import re
html = re.sub(
    r'<script>.*?</script>',
    '<script src="standalone.js"></script>',
    html,
    flags=re.DOTALL
)

# Write output
with open('frontend/index_standalone.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✓ Created frontend/index_standalone.html")
