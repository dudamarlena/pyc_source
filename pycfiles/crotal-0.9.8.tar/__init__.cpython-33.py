# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\HSH\Workspace\py33\py33_projects\crosys-project\crosys\__init__.py
# Compiled at: 2016-06-03 14:38:43
# Size of source mod 2**32: 748 bytes
from __future__ import print_function
import platform, sys, site, os
__version__ = '0.0.1'
__short_description__ = 'Cross Operation System Compatible Library.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
WINDOWS, MACOS, LINUX = (False, False, False)
_system = platform.system()
if _system == 'Windows':
    WINDOWS = True
    SP_PATH = site.getsitepackages()[1]
    PROGRAM_FILES_64 = 'C:\\Program Files'
    PROGRAM_FILES_32 = 'C:\\Program Files (x86)'
else:
    if _system == 'Darwin':
        MACOS = True
        SP_PATH = site.getsitepackages()[0]
    elif _system == 'Linux':
        LINUX = True
        SP_PATH = site.getsitepackages()[0]
USER_PATH = os.path.expanduser('~')