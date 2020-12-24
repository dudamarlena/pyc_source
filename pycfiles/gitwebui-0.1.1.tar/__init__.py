# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Workspace/gitwebui/gitwebui/__init__.py
# Compiled at: 2017-11-25 09:39:33
"""
    Module gitwebui
"""
__version_info__ = (0, 1, 1)
__version__ = ('.').join([ str(val) for val in __version_info__ ])
__namepkg__ = 'gitwebui'
__desc__ = 'GitWebUi module'
__urlpkg__ = 'https://github.com/fraoustin/gitwebui.git'
__entry_points__ = {'console_scripts': [
                     'gitwebui = gitwebui.main:main']}