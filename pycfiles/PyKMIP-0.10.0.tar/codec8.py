# uncompyle6 version 3.6.7
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/pykmer/codec8.py
# Compiled at: 2016-12-19 02:55:29
__doc__ = '\nThis module provides a sequential access variable byte coding scheme.\n\nThe basic method is to produce 1 or more 8-bit code words comprised of\n7 data bits and a *continuation* bit. An encoded integer is composed of\nzero or more code words with the continuation bit set, followed by exactly\none code word with an unset (0) continuation bit. The integer is composed\nfrom the sequence of groups of 7 data bits, most significant "byte" first.\n'
__docformat__ = 'restructuredtext'

def encode(x):
    """
    Encode the integer `x` using a 7-bit+continuation-bit encoding,
    and return the list of 8-bit code words.
    """
    r = []
    while True:
        r.append(x & 127)
        x >>= 7
        if x == 0:
            break

    r = r[::-1]
    n = len(r) - 1
    i = 0
    while i < n:
        r[i] |= 128
        i += 1

    return r


def encodeInto(x, r):
    """
    Encode the integer `x` using a 7-bit+continuation-bit encoding,
    appending the 8-bit code words to an existing list/array.
    """
    n = 0
    y = x
    while True:
        n += 1
        y >>= 7
        r.append(0)
        if y == 0:
            break

    v = n
    i = -1
    m = 0
    while n > 0:
        r[i] = x & 127 | m
        x >>= 7
        i -= 1
        m = 128
        n -= 1


def decode(itr):
    """
    Dencode an integer from a 7-bit+continuation-bit encoding, reading
    8-bit code words from the iterator `itr`.
    """
    r = 0
    x = itr.next()
    r = x & 127
    while x & 128:
        x = itr.next()
        r = r << 7 | x & 127

    return r