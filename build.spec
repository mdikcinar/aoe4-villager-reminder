# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for AoE4 Villager Reminder

import re
from pathlib import Path

# Read version from constants.py
def get_version():
    """Read version number from constants.py file"""
    constants_file = Path("src/utils/constants.py")
    if constants_file.exists():
        with open(constants_file, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'APP_VERSION\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
    return "1.0.0"

VERSION = get_version()
APP_NAME = f"AoE4-Villager-Reminder-v{VERSION}"

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/sounds', 'assets/sounds'),
        ('src/locales', 'src/locales'),
    ],
    hiddenimports=[
        'pygame',
        'psutil',
        'requests',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.sip',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unused PyQt6 modules to reduce size
        'PyQt6.QtWebEngine',
        'PyQt6.QtWebEngineCore',
        'PyQt6.QtWebEngineWidgets',
        'PyQt6.QtSql',
        'PyQt6.QtTest',
        'PyQt6.QtDesigner',
        'PyQt6.QtHelp',
        'PyQt6.QtMultimedia',
        'PyQt6.QtMultimediaWidgets',
        'PyQt6.QtOpenGL',
        'PyQt6.QtOpenGLWidgets',
        'PyQt6.QtPositioning',
        'PyQt6.QtQml',
        'PyQt6.QtQuick',
        'PyQt6.QtQuickWidgets',
        'PyQt6.QtSvg',
        'PyQt6.QtSvgWidgets',
        'PyQt6.Qt3DCore',
        'PyQt6.Qt3DRender',
        'PyQt6.Qt3DInput',
        'PyQt6.Qt3DLogic',
        'PyQt6.Qt3DExtras',
        'PyQt6.Qt3DAnimation',
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
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # DISABLED - UPX corrupts Qt6 DLLs causing "ordinal not found" errors
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.png',  # Application icon
)
