# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/guillem.cabrera/pyvtt/build/lib/pyvtt/compat.py
# Compiled at: 2018-03-05 07:18:39
# Size of source mod 2**32: 290 bytes
import sys
_ver = sys.version_info
is_py2 = _ver[0] == 2
is_py3 = _ver[0] == 3
from io import open as io_open
if is_py2:
    str = str
    str = str
    open = io_open
elif is_py3:
    str = (
     str, bytes)
    str = str
    open = open