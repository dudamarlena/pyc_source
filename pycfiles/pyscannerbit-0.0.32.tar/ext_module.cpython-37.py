# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gmartine/pyscannerbit/pyscannerbit/ext_module.py
# Compiled at: 2020-03-19 02:50:26
# Size of source mod 2**32: 194 bytes
import sys, ctypes
saved_flags = sys.getdlopenflags()
sys.setdlopenflags(saved_flags | ctypes.RTLD_GLOBAL)
import ScannerBit.python as sb
sys.setdlopenflags(saved_flags)