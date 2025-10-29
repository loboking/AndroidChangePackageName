# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Android Project Rebuilder - Windows Version
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
        'tkinter',
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AndroidProjectRebuilder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (important for GUI app!)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icon.ico'  # Windows icon
)

# Note: Windows doesn't use BUNDLE like macOS
# The EXE above creates a single .exe file
