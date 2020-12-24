# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/googlesafebrowsing/util.py
# Compiled at: 2010-12-12 06:19:24
"""Common utilities.
"""
import hashlib, struct

def Bin2Hex(hash):
    hexchars = []
    for i in struct.unpack('%dB' % (len(hash),), hash):
        hexchars.append('%02x' % (i,))

    return ('').join(hexchars)


def GetHash256(expr):
    return hashlib.sha256(expr).digest()


def IsFullHash(expr):
    return len(expr) == 32