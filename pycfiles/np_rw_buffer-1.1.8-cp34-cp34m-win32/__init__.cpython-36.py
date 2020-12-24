# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\repos\testlibs\np_rw_buffer\np_rw_buffer\__init__.py
# Compiled at: 2020-02-17 15:26:19
# Size of source mod 2**32: 341 bytes
from .circular_indexes import get_indexes
py_get_indexes = get_indexes
try:
    from ._circular_indexes import get_indexes
    USING_C = True
    c_get_indexes = get_indexes
except (ImportError, Exception):
    USING_C = False
    c_get_indexes = None

from .buffer import *
from .audio_buffer import *
from .manager import *