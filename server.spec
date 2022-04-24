# -*- mode: python ; coding: utf-8 -*-
import os
import shutil

block_cipher = None


a = Analysis(['src/server.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[
                'uvicorn.logging',
                'uvicorn.loops',
                'uvicorn.loops.auto',
                'uvicorn.protocols',
                'uvicorn.protocols.http',
                'uvicorn.protocols.http.auto',
                'uvicorn.protocols.websockets',
                'uvicorn.protocols.websockets.auto',
                'uvicorn.lifespan',
                'uvicorn.lifespan.on',
             ],
             hookspath=[],
             hooksconfig={},
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='syno-manage-server',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          icon='icon.ico',
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )

shutil.copy('res/mimetypes.csv', 'dist/mimetypes.csv')
os.makedirs('dist/html', exist_ok=True)
shutil.copy('html/favicon.ico', 'dist/html/favicon.ico')