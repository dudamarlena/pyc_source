# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\__init__.py
# Compiled at: 2016-04-18 03:20:12
# Size of source mod 2**32: 351 bytes
version = '4.3.4'
import sys
from cx_Freeze.dist import *
if sys.platform == 'win32' and sys.version_info[:2] >= (2, 5):
    from cx_Freeze.windist import *
elif sys.platform == 'darwin':
    from cx_Freeze.macdist import *
from cx_Freeze.finder import *
from cx_Freeze.freezer import *
from cx_Freeze.main import *
del dist
del finder
del freezer