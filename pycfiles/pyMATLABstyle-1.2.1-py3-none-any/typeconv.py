# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymatlab/typeconv.py
# Compiled at: 2013-10-24 08:37:24
__doc__ = '\nCopyright 2010-2013 Joakim Möller\n\nThis file is part of pymatlab.\n\npymatlab is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\npymatlab is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with pymatlab.  If not, see <http://www.gnu.org/licenses/>.\n'
from ctypes import *
from numpy import array, ndarray, dtype
from os.path import join
import platform, sys, numpy

def numpy_to_ctype(np_variable):
    dtype = str(np_variable.dtype)
    ctype = c_double
    if 'uint' in dtype:
        if '8' in dtype:
            ctype = c_ubyte
        elif '16' in dtype:
            ctype = c_ushort
        elif '32' in dtype:
            ctype = c_uint
        elif '64' in dtype:
            ctype = c_ulong
    elif 'int' in dtype:
        if '8' in dtype:
            ctype = c_byte
        elif '16' in dtype:
            ctype = c_short
        elif '32' in dtype:
            ctype = c_int
        elif '64' in dtype:
            ctype = c_long
    elif 'float' in dtype:
        if '32' in dtype:
            ctype = c_float
        elif '64' in dtype:
            ctype = c_double
        else:
            ctype = c_double
    return ctype


def mat_to_ctype(classname):
    dtype = classname
    ctype = c_double
    if 'uint' in dtype:
        if '8' in dtype:
            ctype = c_ubyte
        elif '16' in dtype:
            ctype = c_ushort
        elif '32' in dtype:
            ctype = c_uint
        elif '64' in dtype:
            ctype = c_ulong
    elif 'int' in dtype:
        if '8' in dtype:
            ctype = c_byte
        elif '16' in dtype:
            ctype = c_short
        elif '32' in dtype:
            ctype = c_int
        elif '64' in dtype:
            ctype = c_long
    elif 'single' in dtype:
        ctype = c_float
    elif 'double' in dtype:
        ctype = c_double
    return ctype


def np_to_mat(np_variable):
    if np_variable.dtype.type == numpy.bool:
        matlab_type = c_int(3)
    elif np_variable.dtype.type == numpy.str:
        matlab_type = c_int(4)
    elif np_variable.dtype.type == numpy.void:
        matlab_type = c_int(5)
    elif np_variable.dtype.type == numpy.complex128:
        matlab_type = c_int(6)
    elif np_variable.dtype.type == numpy.float64:
        matlab_type = c_int(6)
    elif np_variable.dtype.type == numpy.complex64:
        matlab_type = c_int(7)
    elif np_variable.dtype.type == numpy.float32:
        matlab_type = c_int(7)
    elif np_variable.dtype.type == numpy.int8:
        matlab_type = c_int(8)
    elif np_variable.dtype.type == numpy.uint8:
        matlab_type = c_int(9)
    elif np_variable.dtype.type == numpy.int16:
        matlab_type = c_int(10)
    elif np_variable.dtype.type == numpy.uint16:
        matlab_type = c_int(11)
    elif np_variable.dtype.type == numpy.int32:
        matlab_type = c_int(12)
    elif np_variable.dtype.type == numpy.uint32:
        matlab_type = c_int(13)
    elif np_variable.dtype.type == numpy.int64:
        matlab_type = c_int(14)
    elif np_variable.dtype.type == numpy.uint64:
        matlab_type = c_int(15)
    else:
        matlab_type = c_int(5)
    return matlab_type