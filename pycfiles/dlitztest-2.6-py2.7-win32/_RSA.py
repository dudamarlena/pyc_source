# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\PublicKey\_RSA.py
# Compiled at: 2013-03-13 13:15:35
__revision__ = '$Id$'
from Crypto.PublicKey import pubkey
from Crypto.Util import number

def generate_py(bits, randfunc, progress_func=None, e=65537):
    """generate(bits:int, randfunc:callable, progress_func:callable, e:int)

    Generate an RSA key of length 'bits', public exponent 'e'(which must be
    odd), using 'randfunc' to get random data and 'progress_func',
    if present, to display the progress of the key generation.
    """
    obj = RSAobj()
    obj.e = long(e)
    if progress_func:
        progress_func('p,q\n')
    p = q = 1
    while number.size(p * q) < bits:
        p = pubkey.getStrongPrime(bits >> 1, obj.e, 1e-12, randfunc)
        q = pubkey.getStrongPrime(bits - (bits >> 1), obj.e, 1e-12, randfunc)

    if p > q:
        p, q = q, p
    obj.p = p
    obj.q = q
    if progress_func:
        progress_func('u\n')
    obj.u = pubkey.inverse(obj.p, obj.q)
    obj.n = obj.p * obj.q
    if progress_func:
        progress_func('d\n')
    obj.d = pubkey.inverse(obj.e, (obj.p - 1) * (obj.q - 1))
    assert bits <= 1 + obj.size(), 'Generated key is too small'
    return obj


class RSAobj(pubkey.pubkey):

    def size(self):
        """size() : int
        Return the maximum number of bits that can be handled by this key.
        """
        return number.size(self.n) - 1