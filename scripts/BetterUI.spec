# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['BetterUI.py', 'QThreading.py'],
             pathex=['C:\\VMShare\\YtDl\\scripts'],
             binaries=[],
             datas=[('../assets/bg.jpg', 'assets'), ('../assets/folder.svg', 'assets'), ('../assets/search.svg', 'assets')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='BetterUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='BetterUI')
