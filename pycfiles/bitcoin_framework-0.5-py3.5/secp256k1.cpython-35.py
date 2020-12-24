# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitcoin/crypto/ecdsa/secp256k1.py
# Compiled at: 2017-07-08 11:42:23
# Size of source mod 2**32: 941 bytes
"""
Contains constants for the secp256k1 curve

Sources:
https://en.bitcoin.it/wiki/Secp256k1
https://github.com/vbuterin/pybitcointools/blob/master/bitcoin/main.py
"""
from .curve import CurveParams
P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
A = 0
B = 7
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (Gx, Gy)
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
H = 1

class Secp256k1(CurveParams):
    __doc__ = '\n    Defines a Secp256k1 ECDSA Koblitz curve params used in Bitcoin\n    '
    __slots__ = ['p', 'a', 'b', 'g', 'n', 'h']

    def __init__(self):
        """ Initializes a secp256k1 curve parameters object """
        super().__init__(G, N)
        self.p = P
        self.a = A
        self.b = B
        self.h = H


PARAMS = Secp256k1()