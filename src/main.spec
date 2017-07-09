# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/Users/yangxinlei/Desktop/PathPlanning/src'],
             binaries=[],
             datas=[('/Pathplanning/data/map.osm', '/data' ),
             ('/Pathplanning/data/icons/*.png', '/data/icons' ),
             ('/Pathplanning/data/icons/add/*.png', '/data/icons/add'),
             ('/Pathplanning/data/icons/bike/*.png', '/data/icons/bike')，
             ('/Pathplanning/data/icons/minus/*.png', '/data/icons/minus'),
             ('/Pathplanning/data/icons/pin/*.png', '/data/icons/pin'),
             ('/Pathplanning/data/icons/swap/*.png', '/data/icons/swap'),
             ('/Pathplanning/data/icons/walk/*.png', '/data/icons/walk'),
             ],
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
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name='main.app',
             icon=None,
             bundle_identifier=None)
