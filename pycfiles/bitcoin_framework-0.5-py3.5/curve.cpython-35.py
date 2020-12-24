# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitcoin/crypto/ecdsa/curve.py
# Compiled at: 2017-07-08 11:42:23
# Size of source mod 2**32: 655 bytes
"""
Models the parameters an ECDSA curve must contain
"""

class CurveParams(object):
    __doc__ = '\n    Defines the parameters an ECDSA algorithm elliptic curve must define\n    https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm\n\n    Attributes:\n        g (tuple): ellpitic curve base point, generator of the elliptic curve\n                   with large prime order n, as a tuple of x, y longs\n        n (long): integer order of G, means that n X G = 0\n    '
    __slots__ = ['g', 'n']

    def __init__(self, g, n):
        """
        Initializes a basic curve with parameters G and N
        """
        self.n = n
        self.g = g