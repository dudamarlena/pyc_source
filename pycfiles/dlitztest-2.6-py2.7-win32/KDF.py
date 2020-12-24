# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\Protocol\KDF.py
# Compiled at: 2013-03-14 04:43:25
"""This file contains a collection of standard key derivation functions.

A key derivation function derives one or more secondary secret keys from
one primary secret (a master key or a pass phrase).

This is typically done to insulate the secondary keys from each other,
to avoid that leakage of a secondary key compromises the security of the
master key, or to thwart attacks on pass phrases (e.g. via rainbow tables).

:undocumented: __revision__
"""
__revision__ = '$Id$'
import math, struct
from Crypto.Util.py3compat import *
from Crypto.Hash import SHA1, HMAC
from Crypto.Util.strxor import strxor

def PBKDF1(password, salt, dkLen, count=1000, hashAlgo=None):
    """Derive one key from a password (or passphrase).

    This function performs key derivation according an old version of
    the PKCS#5 standard (v1.5).
    
    This algorithm is called ``PBKDF1``. Even though it is still described
    in the latest version of the PKCS#5 standard (version 2, or RFC2898),
    newer applications should use the more secure and versatile `PBKDF2` instead.

    :Parameters:
     password : string
        The secret password or pass phrase to generate the key from.
     salt : byte string
        An 8 byte string to use for better protection from dictionary attacks.
        This value does not need to be kept secret, but it should be randomly
        chosen for each derivation.
     dkLen : integer
        The length of the desired key. Default is 16 bytes, suitable for instance for `Crypto.Cipher.AES`.
     count : integer
        The number of iterations to carry out. It's recommended to use at least 1000.
     hashAlgo : module
        The hash algorithm to use, as a module or an object from the `Crypto.Hash` package.
        The digest length must be no shorter than ``dkLen``.
        The default algorithm is `SHA1`.

    :Return: A byte string of length `dkLen` that can be used as key.
    """
    if not hashAlgo:
        hashAlgo = SHA1
    password = tobytes(password)
    pHash = hashAlgo.new(password + salt)
    digest = pHash.digest_size
    if dkLen > digest:
        raise ValueError('Selected hash algorithm has a too short digest (%d bytes).' % digest)
    if len(salt) != 8:
        raise ValueError('Salt is not 8 bytes long.')
    for i in xrange(count - 1):
        pHash = pHash.new(pHash.digest())

    return pHash.digest()[:dkLen]


def PBKDF2(password, salt, dkLen=16, count=1000, prf=None):
    """Derive one or more keys from a password (or passphrase).

    This performs key derivation according to the PKCS#5 standard (v2.0),
    by means of the ``PBKDF2`` algorithm.

    :Parameters:
     password : string
        The secret password or pass phrase to generate the key from.
     salt : string
        A string to use for better protection from dictionary attacks.
        This value does not need to be kept secret, but it should be randomly
        chosen for each derivation. It is recommended to be at least 8 bytes long.
     dkLen : integer
        The cumulative length of the desired keys. Default is 16 bytes, suitable for instance for `Crypto.Cipher.AES`.
     count : integer
        The number of iterations to carry out. It's recommended to use at least 1000.
     prf : callable
        A pseudorandom function. It must be a function that returns a pseudorandom string
        from two parameters: a secret and a salt. If not specified, HMAC-SHA1 is used.

    :Return: A byte string of length `dkLen` that can be used as key material.
        If you wanted multiple keys, just break up this string into segments of the desired length.
"""
    password = tobytes(password)
    if prf is None:
        prf = lambda p, s: HMAC.new(p, s, SHA1).digest()
    key = b('')
    i = 1
    while len(key) < dkLen:
        U = previousU = prf(password, salt + struct.pack('>I', i))
        for j in xrange(count - 1):
            previousU = t = prf(password, previousU)
            U = strxor(U, t)

        key += U
        i = i + 1

    return key[:dkLen]