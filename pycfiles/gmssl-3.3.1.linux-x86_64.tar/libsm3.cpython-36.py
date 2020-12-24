# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/gmssl/libsm3/libsm3.py
# Compiled at: 2020-03-10 11:26:45
# Size of source mod 2**32: 3122 bytes
import os, sys, platform, ctypes, time
from functools import wraps
__all__ = [
 'SM3Context', 'lib_sm3', 'sm3_starts', 'sm3_update', 'sm3_finish', 'sm3']

def timethis(func):
    """
    Decorator that reports the execution time.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end - start)
        return result

    return wrapper


c_ubyte_p = ctypes.POINTER(ctypes.c_ubyte)

class SM3Context(ctypes.Structure):
    _fields_ = [
     (
      'total', ctypes.c_ulong * 2),
     (
      'state', ctypes.c_ulong * 8),
     (
      'buffer', ctypes.c_ubyte * 64),
     (
      'ipad', ctypes.c_ubyte * 64),
     (
      'opad', ctypes.c_ubyte * 64)]


lib_sm3 = None
sm3_starts = None
sm3_update = None
sm3_finish = None
sm3 = None
if platform.system() == 'Windows':
    lib_file = 'libsm3.dll'
else:
    lib_file = 'libsm3.so'
try:
    library_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), lib_file)
    if not os.path.exists(library_path):
        library_path = os.path.join(os.getcwd(), lib_file)
    lib_sm3 = ctypes.CDLL(library_path)
except Exception as e:
    lib_sm3 = None

if lib_sm3 is not None:
    sm3_starts = lib_sm3.sm3_starts
    sm3_starts.restype = None
    sm3_starts.argtypes = (ctypes.POINTER(SM3Context),)
    sm3_update = lib_sm3.sm3_update
    sm3_update.restype = None
    sm3_update.argtypes = (ctypes.POINTER(SM3Context), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int)
    sm3_finish = lib_sm3.sm3_finish
    sm3_finish.restype = None
    sm3_finish.argtypes = (ctypes.POINTER(SM3Context), ctypes.POINTER(ctypes.c_ubyte * 32))
    sm3 = lib_sm3.sm3
    sm3.restype = None
    sm3.argtypes = (ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte * 32))