# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud_Crypto/Util/number.py
# Compiled at: 2016-11-22 15:21:45
__revision__ = '$Id$'
from warnings import warn as _warn
import math, sys
from cgcloud_Crypto.pct_warnings import GetRandomNumber_DeprecationWarning, PowmInsecureWarning
from cgcloud_Crypto.Util.py3compat import *
bignum = long
try:
    from cgcloud_Crypto.PublicKey import _fastmath
except ImportError:
    _fastmath = None

if _fastmath is not None and not _fastmath.HAVE_DECL_MPZ_POWM_SEC:
    _warn('Not using mpz_powm_sec.  You should rebuild using libgmp >= 5 to avoid timing attack vulnerability.', PowmInsecureWarning)

def inverse(u, v):
    """inverse(u:long, v:long):long
    Return the inverse of u mod v.
    """
    u3, v3 = long(u), long(v)
    u1, v1 = (1, 0)
    while v3 > 0:
        q = divmod(u3, v3)[0]
        u1, v1 = v1, u1 - v1 * q
        u3, v3 = v3, u3 - v3 * q

    while u1 < 0:
        u1 = u1 + v

    return u1


import struct

def long_to_bytes(n, blocksize=0):
    """long_to_bytes(n:long, blocksize:int) : string
    Convert a long integer to a byte string.

    If optional blocksize is given and greater than zero, pad the front of the
    byte string with binary zeros so that the length is a multiple of
    blocksize.
    """
    s = b('')
    n = long(n)
    pack = struct.pack
    while n > 0:
        s = pack('>I', n & 4294967295) + s
        n = n >> 32

    for i in range(len(s)):
        if s[i] != b('\x00')[0]:
            break
    else:
        s = b('\x00')
        i = 0

    s = s[i:]
    if blocksize > 0 and len(s) % blocksize:
        s = (blocksize - len(s) % blocksize) * b('\x00') + s
    return s


def bytes_to_long(s):
    """bytes_to_long(string) : long
    Convert a byte string to a long integer.

    This is (essentially) the inverse of long_to_bytes().
    """
    acc = 0
    unpack = struct.unpack
    length = len(s)
    if length % 4:
        extra = 4 - length % 4
        s = b('\x00') * extra + s
        length = length + extra
    for i in range(0, length, 4):
        acc = (acc << 32) + unpack('>I', s[i:i + 4])[0]

    return acc


import warnings

def long2str(n, blocksize=0):
    warnings.warn('long2str() has been replaced by long_to_bytes()')
    return long_to_bytes(n, blocksize)


def str2long(s):
    warnings.warn('str2long() has been replaced by bytes_to_long()')
    return bytes_to_long(s)


def _import_Random():
    global Random
    global StrongRandom
    from cgcloud_Crypto import Random
    from cgcloud_Crypto.Random.random import StrongRandom