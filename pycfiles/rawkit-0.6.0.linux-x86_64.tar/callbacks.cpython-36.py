# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.6/site-packages/libraw/callbacks.py
# Compiled at: 2015-07-19 23:14:00
# Size of source mod 2**32: 2320 bytes
""":mod:`libraw.callbacks` --- LibRaw callback definitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Warning:

    You will need to keep a reference to your callback functions for as long as
    you want to call them from C code, otherwise they may be garbage collected
    and lead to a segmentation fault.
"""
from ctypes import *
memory_callback = CFUNCTYPE(c_void_p, c_char_p, c_char_p)
data_callback = CFUNCTYPE(c_void_p, c_char_p, c_int)
progress_callback = CFUNCTYPE(c_void_p, c_int, c_int, c_int)