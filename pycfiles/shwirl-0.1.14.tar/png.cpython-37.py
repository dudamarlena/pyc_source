# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/ext/png.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 313 bytes
"""
Handle loading png package from system or from the bundled copy
"""
try:
    from ._bundled.png import *
except ImportError:
    from png import *