# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gmartine/pyscannerbit/pyscannerbit/ext_module.py
# Compiled at: 2020-03-19 02:50:26
# Size of source mod 2**32: 194 bytes
import sys, ctypes
saved_flags = sys.getdlopenflags()
sys.setdlopenflags(saved_flags | ctypes.RTLD_GLOBAL)
import ScannerBit.python as sb
sys.setdlopenflags(saved_flags)