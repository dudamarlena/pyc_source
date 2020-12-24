# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/pykmer/bits.py
# Compiled at: 2017-01-23 23:56:05
"""
This module provides a collection of low level bit manipulation functions.
Some, such as `popcnt` and `ffs` can actually be evaluated with single
machine instructions, but unfortunately these are not exposed at the
Python language level. However, the implementations below have been
tuned somewhat and with pypy run pretty fast.

Most of the functions are adaptions of those at
https://graphics.stanford.edu/~seander/bithacks.html
"""
__docformat__ = 'restructuredtext'
m1 = 6148914691236517205
m2 = 3689348814741910323
m3 = 1085102592571150095
m4 = 71777214294589695
m5 = 281470681808895
m6 = 4294967295

def rev(x):
    """
    Reverse the bit-pairs in the 64-bit integer `x`.
    """
    x = x >> 2 & m2 | (x & m2) << 2
    x = x >> 4 & m3 | (x & m3) << 4
    x = x >> 8 & m4 | (x & m4) << 8
    x = x >> 16 & m5 | (x & m5) << 16
    x = x >> 32 & m6 | (x & m6) << 32
    return x


def popcnt(x):
    """
    Compute the number of set bits (i.e 1s) in the 64-bit integer `x`.
    """
    x = (x & m1) + (x >> 1 & m1)
    x = (x & m2) + (x >> 2 & m2)
    x = (x & m3) + (x >> 4 & m3)
    x = (x & m4) + (x >> 8 & m4)
    x = (x & m5) + (x >> 16 & m5)
    x = (x & m6) + (x >> 32 & m6)
    return x & 127


def _ffs0(x):
    r = (x > 4294967295) << 5
    x >>= r
    s = (x > 65535) << 4
    x >>= s
    r |= s
    s = (x > 255) << 3
    x >>= s
    r |= s
    s = (x > 15) << 2
    x >>= s
    r |= s
    s = (x > 3) << 1
    x >>= s
    r |= s
    r |= x >> 1
    return r


_ffsBits = [ _ffs0(i) ]

def ffs(x):
    """
    Find the position of the most significant set bit (i.e. 1)
    in the 64-bit integer `x`.
    """
    x32 = x >> 32
    if x32 > 0:
        x48 = x >> 48
        if x48 > 0:
            x56 = x >> 56
            if x56 > 0:
                return _ffsBits[x56] + 56
            return _ffsBits[x48] + 48
        else:
            x40 = x >> 40
            if x40 > 0:
                return _ffsBits[x40] + 40
            return _ffsBits[x32] + 32
    else:
        x16 = x >> 16
        if x16 > 0:
            x24 = x >> 24
            if x24 > 0:
                return _ffsBits[x24] + 24
            return _ffsBits[x16] + 16
        else:
            x8 = x >> 8
            if x8 > 0:
                return _ffsBits[x8] + 8
            return _ffsBits[x]