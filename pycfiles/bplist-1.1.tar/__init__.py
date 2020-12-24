# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bplib/__init__.py
# Compiled at: 2019-05-26 22:32:33
try:
    from . import bp
    from . import pack
except:
    pass

__doc__ = 'The ``bplib`` is a library implementing support for computations on groups supporting \nbilinear pairings, as used in modern cryptography. \n\nIt is based on the OpenPairing library by \nDiego Aranha (https://github.com/dfaranha/OpenPairing), which is itself based on, and compatible \nwith, OpenSSL math functions (``bn`` and ``ec``). The ``bplib`` is compatible with ``petlib`` types\nincluding ``petlib.bn`` and the group G1 is a ``petlib.ec`` EC group. Along with ``petlib``, \nthey provide easy to use \nsupport for maths and ciphers used in modern Privacy Enhancing Technologies."\n\nA set of bilinear EC groups is defined as:\n\n    >>> G = bp.BpGroup()\n\nSuch a BpGroup describes 3 groups G1, G2 and GT such that pair(G1,G2)->GT. Generators \nfor the groups G1 and G2 are denoted by:\n\n    >>> g1, g2 = G.gen1(), G.gen2()\n\nThe special ``pair`` operation computes to pairing into GT:\n\n    >>> gt = G.pair(g1, g2)\n\nOperations are defined on all elements of G1, G2 or GT in a natural additive infix notation for G1 and G2, and a multiplicative notation for GT:\n    \n    >>> gt6 = gt**6\n\nAs expected the ``pair`` operations is additive:\n\n    >>> G.pair(g1, 6*g2) == gt6\n    True\n    >>> G.pair(6*g1, g2) == gt6\n    True\n    >>> G.pair(2*g1, 3*g2) == gt6\n    True\n\n'
VERSION = '0.0.6'