# -*- mode: python ; coding: utf-8 -*-
"""
VideoDL GUI 打包配置文件
使用 PyInstaller 将 GUI 程序打包成单个 exe 文件
"""

block_cipher = None

a = Analysis(
    ['videodl_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('videodl/modules/cdm/*.wvd', 'videodl/modules/cdm'),
        ('videodl/modules/js/youtube/*.js', 'videodl/modules/js/youtube'),
        ('videodl/modules/js/xmflv/*.js', 'videodl/modules/js/xmflv'),
        ('videodl/modules/js/xmflv/xiami_token.wasm', 'videodl/modules/js/xmflv'),
        ('videodl/modules/js/tencent/*.js', 'videodl/modules/js/tencent'),
        ('videodl/modules/js/tencent/ckey.wasm', 'videodl/modules/js/tencent'),
        ('videodl/modules/js/cctv/*.js', 'videodl/modules/js/cctv'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'videodl.videodl',
        'requests',
        'click',
        'json_repair',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'unittest',
        'pydoc',
        'doctest',
        'numpy',
        'scipy',
        'matplotlib',
        'PIL',
        'jinja2',
        'babel',
        'setuptools',
        'pkg_resources',
        'pip',
        'wheel',
        'beautifulsoup4',
        'parsel',
        'tqdm',
        'pycryptodomex',
        'cryptography',
        'tldextract',
        'fake_useragent',
        'nodejs_wheel',
        'pyfreeproxy',
        'playwright',
        'questionary',
        'pywidevine',
        'curl_cffi',
        'rich',
        'prettytable',
        'pathvalidate',
        'platformdirs',
        'emoji',
        'bleach',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=True,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VideoDL_GUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加图标文件路径
)
