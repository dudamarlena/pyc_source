# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\setup2.py
# Compiled at: 2012-10-13 10:51:14
try:
    try:
        import py2exe.mf as modulefinder
    except ImportError:
        import modulefinder

    import win32com, sys
    for p in win32com.__path__[1:]:
        modulefinder.AddPackagePath('win32com', p)

    for extra in ['win32com.shell']:
        __import__(extra)
        m = sys.modules[extra]
        for p in m.__path__[1:]:
            modulefinder.AddPackagePath(extra, p)

except ImportError:
    pass

from distutils.core import setup
import py2exe
setup(console=['startmenu_snapshot.py'], options={'py2exe': {'optimize': 2, 'bundle_files': 1, 'excludes': [
                         'doctest', 'pdb', 'unitest', 'difflib',
                         'inspect', 'calender']}}, zipfile=None)