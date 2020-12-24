# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanghunkang/dev/aascraw/venv/lib/python3.7/site-packages/aascraw/test.kernels.py
# Compiled at: 2019-09-09 10:55:31
# Size of source mod 2**32: 968 bytes
import numpy as np
from functools import reduce
import ctypes
c_kernels = ctypes.CDLL('./kernels.so')
xpath_set = [
 'Some',
 'arbitasdasdrary',
 'length',
 'string',
 'string',
 'string']
SIZE_XPATH_SET = len(xpath_set)
c_kernels.rank_tuple_vicinity.restype = ctypes.c_float

def rank_tuple_vicinity(xpath_set, existing_records):
    xpath_set = [bytes(xpath, 'utf-8') for xpath in xpath_set]
    xpath_set.append(None)
    c_kernels.rank_tuple_vicinity.argtypes = (
     ctypes.c_wchar_p * (SIZE_XPATH_SET + 1),)
    arr = (ctypes.c_wchar_p * (SIZE_XPATH_SET + 1))(*xpath_set)
    return c_kernels.rank_tuple_vicinity(arr)


print(SIZE_XPATH_SET)
aa = rank_tuple_vicinity(xpath_set, None)
print(aa)