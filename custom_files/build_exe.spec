# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for videodl
用于构建 videodl 的 Windows 可执行文件
"""

import sys
import site
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# 收集所有数据文件
datas = []
datas += collect_data_files('videodl')

# 动态获取 rich 的 Unicode 数据文件路径
try:
    rich_unicode_path = os.path.join(site.getsitepackages()[0], 'rich/_unicode_data')
    if os.path.exists(rich_unicode_path):
        for file in os.listdir(rich_unicode_path):
            if file.endswith('.py') and not file.startswith('__'):
                datas.append((os.path.join(rich_unicode_path, file), 'rich/_unicode_data'))
except:
    pass  # 如果找不到，跳过手动添加

datas += collect_data_files('playwright')  # playwright 驱动文件
datas += collect_data_files('curl_cffi')  # curl_cffi 数据文件

# 隐藏导入（可能需要动态导入的模块）
hiddenimports = []
hiddenimports += collect_submodules('videodl')
hiddenimports += ['click', 'rich', 'prettytable', 'json_repair', 'pathvalidate']
hiddenimports += ['platformdirs', 'emoji', 'bleach', 'beautifulsoup4', 'parsel', 'tqdm']
hiddenimports += ['pycryptodomex', 'pycryptodome', 'cryptography', 'tldextract', 'fake_useragent']
hiddenimports += ['pyfreeproxy', 'playwright', 'questionary', 'pywidevine', 'curl_cffi', 'm3u8']
hiddenimports += ['Crypto', 'Crypto.Cipher', 'Crypto.Random']
hiddenimports += ['nodejs_wheel']

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='videodl',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
