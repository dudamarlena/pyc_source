# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/spoon/ber/common.py
# Compiled at: 2006-11-19 22:32:48
import struct
UNIVERSAL = 0
APPLICATION = 1
CONTEXT = 2
PRIVATE = 3

class BERException(Exception):
    __module__ = __name__


def inflate_long(s, always_positive=False):
    """turns a normalized byte string into a long-int (adapted from Crypto.Util.number)"""
    out = 0
    negative = 0
    if not always_positive and len(s) > 0 and ord(s[0]) >= 128:
        negative = 1
    if len(s) % 4:
        filler = '\x00'
        if negative:
            filler = b'\xff'
        s = filler * (4 - len(s) % 4) + s
    for i in range(0, len(s), 4):
        out = (out << 32) + struct.unpack('>I', s[i:i + 4])[0]

    if negative:
        out -= 1 << 8 * len(s)
    return out


def deflate_long(n, add_sign_padding=True):
    """turns a long-int into a normalized byte string (adapted from Crypto.Util.number)"""
    s = ''
    n = long(n)
    while n != 0 and n != -1:
        s = struct.pack('>I', n & 4294967295) + s
        n = n >> 32

    for i in enumerate(s):
        if n == 0 and i[1] != '\x00':
            break
        if n == -1 and i[1] != b'\xff':
            break
    else:
        i = (0, )
        if n == 0:
            s = '\x00'
        else:
            s = b'\xff'

    s = s[i[0]:]
    if add_sign_padding:
        if n == 0 and ord(s[0]) >= 128:
            s = '\x00' + s
        if n == -1 and ord(s[0]) < 128:
            s = b'\xff' + s
    return s