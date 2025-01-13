# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 添加数据文件
added_files = [
    ('config.py', '.'),
    ('in_order_data.yaml', '.'),
    ('qc_data.yaml', '.'),
    ('ac_data.yaml', '.')
]

a = Analysis(
    ['main.py'],  # 主程序入口
    pathex=[],
    binaries=[],
    datas=added_files,  # 添加数据文件
    hiddenimports=[
        'PyQt5',
        'requests',
        'yaml',
        'datetime',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='百洋一体化测试工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 临时改为True以查看错误信息
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
) 