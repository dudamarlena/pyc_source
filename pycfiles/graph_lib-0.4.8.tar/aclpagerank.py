# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mengliu/Dropbox/Research/graph_lib/graph_lib/wrappers/python/aclpagerank.py
# Compiled at: 2017-09-07 23:22:48
from operator import itemgetter
import numpy as np
from numpy.ctypeslib import ndpointer
import ctypes
from sys import platform
from os import path
libloc = path.join(path.abspath(path.dirname(__file__)), '../../lib/graph_lib_test/libgraph')

def aclpagerank(n, ai, aj, alpha, eps, seedids, nseedids, maxsteps, xlength, flag=0):
    float_type = ctypes.c_double
    dt = np.dtype(ai[0])
    itype, ctypes_itype = (np.int64, ctypes.c_int64) if dt.name == 'int64' else (np.uint32, ctypes.c_uint32)
    dt = np.dtype(aj[0])
    vtype, ctypes_vtype = (np.int64, ctypes.c_int64) if dt.name == 'int64' else (np.uint32, ctypes.c_uint32)
    if platform == 'linux2':
        extension = '.so'
    elif platform == 'darwin':
        extension = '.dylib'
    elif platform == 'win32':
        extension = '.dll'
    else:
        print 'Unknown system type!'
        return (True, 0, 0)
    lib = ctypes.cdll.LoadLibrary(libloc + extension)
    if (
     vtype, itype) == (np.int64, np.int64):
        fun = lib.aclpagerank64
    elif (
     vtype, itype) == (np.uint32, np.int64):
        fun = lib.aclpagerank32_64
    else:
        fun = lib.aclpagerank32
    seedids = np.array(seedids, dtype=vtype)
    xids = np.zeros(xlength, dtype=vtype)
    values = np.zeros(xlength, dtype=float_type)
    fun.restype = ctypes_vtype
    fun.argtypes = [ctypes_vtype, ndpointer(ctypes_itype, flags='C_CONTIGUOUS'),
     ndpointer(ctypes_vtype, flags='C_CONTIGUOUS'),
     ctypes_vtype, ctypes.c_double, ctypes.c_double,
     ndpointer(ctypes_vtype, flags='C_CONTIGUOUS'),
     ctypes_vtype, ctypes_vtype,
     ndpointer(ctypes_vtype, flags='C_CONTIGUOUS'),
     ctypes_vtype, ndpointer(ctypes.c_double, flags='C_CONTIGUOUS')]
    actual_length = fun(n, ai, aj, flag, alpha, eps, seedids, nseedids, maxsteps, xids, xlength, values)
    actual_values = np.empty(actual_length, dtype=float_type)
    actual_xids = np.empty(actual_length, dtype=vtype)
    actual_values[:] = [ values[i] for i in range(actual_length) ]
    actual_xids[:] = [ xids[i] for i in range(actual_length) ]
    return (
     actual_length, actual_xids, actual_values)