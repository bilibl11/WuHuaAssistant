# -*- mode: python -*-


block_cipher = None

a = Analysis(
    ['MainWindow.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'sip',
        'Utils',
        'DataPack.FilePath',
        'DataPack.GameState',
        'DataPack.Level',
        'Scripts.CleanHP',
        'Scripts.DispatchCompany',
        'Scripts.GameStateServlet',
        'Scripts.Task',
        'Scripts.MainWindowServlet',
        'Scripts.YIWUSUO'
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

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='WuHua Assistant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    console=False,
    icon='i:\icon.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WuHua Assistant',
)
