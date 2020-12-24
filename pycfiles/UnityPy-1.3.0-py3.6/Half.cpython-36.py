# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\math\Half.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 2447 bytes
import struct
from UnityPy import math
MaxValue = 65504.0
MinValue = -65504.0

def ToHalf(*args) -> float:
    """
        Converts the input into a half-float.
        Inputs:
                unsigned integer
                or
                buffer (bytes, buffer)
                offset
        """
    if len(args) == 1:
        data = struct.pack('H', args[0])
        val = struct.unpack('e', data)[0]
    else:
        if len(args) == 2:
            val = struct.unpack_from('e', args[0], args[1])[0]
    if math.isnan(val):
        return 0
    else:
        if math.isinf(val):
            return MaxValue
        return val