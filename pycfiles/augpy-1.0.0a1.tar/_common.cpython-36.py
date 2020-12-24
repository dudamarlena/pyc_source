# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/folz/DFKI/Hacks/augpy/test/_common.py
# Compiled at: 2020-03-09 10:20:54
# Size of source mod 2**32: 1482 bytes
import numpy as np, augpy
from augpy.numeric_limits import CAST_LIMITS
I_TYPES = [
 (
  augpy.uint8, np.uint8),
 (
  augpy.int8, np.int8),
 (
  augpy.uint16, np.uint16),
 (
  augpy.int16, np.int16),
 (
  augpy.uint32, np.uint32),
 (
  augpy.int32, np.int32),
 (
  augpy.uint64, np.uint64),
 (
  augpy.int64, np.int64)]
F_TYPES = [
 (
  augpy.float32, np.float32),
 (
  augpy.float64, np.float64)]
TYPES = I_TYPES + F_TYPES

def dtype_info(dtype):
    try:
        return np.iinfo(dtype)
    except ValueError:
        try:
            return np.finfo(dtype)
        except ValueError:
            raise ValueError('%r is neither int nor float type' % dtype)


def is_int(dtype):
    try:
        np.iinfo(dtype)
        return True
    except ValueError:
        return False


def is_float(dtype):
    try:
        np.finfo(dtype)
        return True
    except ValueError:
        return False


def safe_cast(a, dtype):
    if isinstance(dtype, np.dtype):
        dtype = dtype.type
    else:
        vmin, vmax = CAST_LIMITS.get((a.dtype.type, dtype), (None, None))
        if is_float(a.dtype):
            if not is_float(dtype):
                a = np.round(a)
        a = a.astype(np.float128)
        vmin = None if vmin is None else np.float128(vmin)
        vmax = None if vmax is None else np.float128(vmax)
        if vmin is not None or vmax is not None:
            a = np.clip(a, vmin, vmax)
    return np.asanyarray(a).astype(dtype)