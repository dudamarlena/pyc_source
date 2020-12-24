# uncompyle6 version 3.6.7
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/pykmer/codec16.py
# Compiled at: 2017-01-24 00:15:59
__doc__ = '\nThis module provides a sequential access variable 16-bit coding scheme.\n\nThe basic method is to produce 1 or more 16-bit code words comprised of\n15 data bits and a *continuation* bit. An encoded integer is composed of\nzero or more code words with the continuation bit set, followed by exactly\none code word with an unset (0) continuation bit. The integer is composed\nfrom the sequence of groups of 15 data bits, most significant "word" first.\n'
__docformat__ = 'restructuredtext'

def encode(x):
    """encode an integer using a 15-bit+continuation-bit encodeing"""
    r = []
    while True:
        r.append(x & 32767)
        x >>= 15
        if x == 0:
            break

    r = r[::-1]
    n = len(r) - 1
    i = 0
    while i < n:
        r[i] |= 32768
        i += 1

    return r


def encodeInto(x, r):
    """encode an integer using a 7-bit+continuation-bit encodeing into an existing list"""
    n = 0
    y = x
    while True:
        n += 1
        y >>= 15
        r.append(0)
        if y == 0:
            break

    v = n
    i = -1
    m = 0
    while n > 0:
        r[i] = x & 32767 | m
        x >>= 15
        i -= 1
        m = 32768
        n -= 1


def decode(itr):
    """dencode an integer from a 7-bit+continuation-bit encodeing"""
    r = 0
    x = itr.next()
    r = x & 32767
    while x & 32768:
        x = itr.next()
        r = r << 15 | x & 32767

    return r