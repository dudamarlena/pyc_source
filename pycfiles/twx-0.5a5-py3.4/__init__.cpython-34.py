# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\twx\__init__.py
# Compiled at: 2015-06-29 18:07:13
# Size of source mod 2**32: 387 bytes
import sys
if sys.version_info[0] == 3:
    if sys.version_info[1] >= 2:
        from pkgutil import extend_path
        __path__ = extend_path(__path__, __name__)
if sys.version_info[0] == 3:
    if sys.version_info[1] >= 4:
        from .twx import *