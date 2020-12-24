# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\kanzhun\projects\graph\graphic\src\graphic\compat.py
# Compiled at: 2018-11-05 01:18:16
# Size of source mod 2**32: 263 bytes
import sys
_ver = sys.version_info

def is_py37():
    return _ver.major == 3 and _ver.minor == 7


try:
    import ModuleNotFoundError
except ImportError:
    ModuleNotFoundError = ImportError