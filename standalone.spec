# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Android Project Rebuilder standalone app
"""

block_cipher = None

# Collect all backend modules
backend_hiddenimports = [
    'backend',
    'backend.processor',
    'backend.utils',
    'backend.utils.zip_tools',
    'backend.utils.cleanup',
    'backend.utils.file_replace',
    'backend.utils.firebase',
    'backend.utils.icon_replace',
    'backend.utils.baseurl_replace',
]

a = Analysis(
    ['standalone_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('frontend/index_standalone.html', 'frontend'),
        ('frontend/standalone.js', 'frontend'),
    ],
    hiddenimports=backend_hiddenimports + [
        'webview',
        'PIL',
        'PIL._tkinter_finder',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',  # Exclude if not needed
        'matplotlib',
        'numpy',
        'scipy',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AndroidProjectRebuilder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window on macOS
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AndroidProjectRebuilder',
)

app = BUNDLE(
    coll,
    name='AndroidProjectRebuilder.app',
    icon='resources/icon.icns',
    bundle_identifier='com.androidrebuilder.app',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'LSMinimumSystemVersion': '10.13.0',
        'CFBundleName': 'Android Project Rebuilder',
        'CFBundleDisplayName': 'Android Project Rebuilder',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2025',
    },
)
