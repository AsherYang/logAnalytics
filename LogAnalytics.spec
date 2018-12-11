# -*- mode: python -*-

block_cipher = None


a = Analysis(['LogAnalytics.py'],
             pathex=['D:\\program_file\\python\\install\\python', 'd:\\python_demo\\qt5\\logAnalytics'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [('\\img\\delete.png', 'd:\\python_demo\\qt5\\logAnalytics\\img\\delete.png', 'DATA'), 
           ('\\img\\check.png', 'd:\\python_demo\\qt5\\logAnalytics\\img\\check.png', 'DATA'),
		   ('\\img\\log.png', 'd:\\python_demo\\qt5\\logAnalytics\\img\\log.png', 'DATA')],
          name='LogAnalytics',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='log.ico')
