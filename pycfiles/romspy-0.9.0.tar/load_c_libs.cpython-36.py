# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicomuen/PycharmProjects/roms_tools/romspy/interpolation/vertical/load_c_libs.py
# Compiled at: 2019-09-04 10:19:54
# Size of source mod 2**32: 1094 bytes
import ctypes
from numpy.ctypeslib import ndpointer
import os
filepath = os.path.realpath(__file__)
libpath = os.path.join(os.path.split(filepath)[0], 'linear.so')
lib = ctypes.cdll.LoadLibrary(libpath)
gen_vert_bil = lib.create_weights
interp_bil = lib.apply_weights
bil_weight_extra_len = 3
gen_vert_bil.restype = None
gen_vert_bil.argtypes = [
 ndpointer(ctypes.c_float),
 ctypes.c_ulonglong,
 ndpointer(ctypes.c_float),
 ctypes.c_ulonglong,
 ctypes.c_ulonglong,
 ndpointer(ctypes.c_float)]
interp_bil.restype = None
interp_bil.argtypes = [
 ndpointer(ctypes.c_float),
 ndpointer(ctypes.c_float),
 ndpointer(ctypes.c_float),
 ctypes.c_ulonglong]