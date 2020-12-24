# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mariojayakumar/Documents/School/2019_2020/Sem2/MAgent/magent/c_lib.py
# Compiled at: 2020-04-05 20:40:34
# Size of source mod 2**32: 1194 bytes
""" some utility for call C++ code"""
from __future__ import absolute_import
import os, ctypes, platform, multiprocessing

def _load_lib():
    """ Load library in build/lib. """
    cur_path = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))
    lib_path = os.path.join(cur_path, 'build/')
    if platform.system() == 'Darwin':
        path_to_so_file = os.path.join(lib_path, 'libmagent.dylib')
    else:
        if platform.system() == 'Linux':
            path_to_so_file = os.path.join(lib_path, 'libmagent.so')
        else:
            raise BaseException('unsupported system: ' + platform.system())
    lib = ctypes.CDLL(path_to_so_file, ctypes.RTLD_GLOBAL)
    return lib


def as_float_c_array(buf):
    """numpy to ctypes array"""
    return buf.ctypes.data_as(ctypes.POINTER(ctypes.c_float))


def as_int32_c_array(buf):
    """numpy to ctypes array"""
    return buf.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))


def as_bool_c_array(buf):
    """numpy to ctypes array"""
    return buf.ctypes.data_as(ctypes.POINTER(ctypes.c_bool))


if 'OMP_NUM_THREADS' not in os.environ:
    os.environ['OMP_NUM_THREADS'] = str(multiprocessing.cpu_count() // 2)
_LIB = _load_lib()