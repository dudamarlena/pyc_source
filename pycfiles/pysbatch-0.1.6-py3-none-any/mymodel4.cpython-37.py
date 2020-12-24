# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/alex/git/VU/pysb/doc/examples/mymodel4.py
# Compiled at: 2019-03-05 14:00:16
# Size of source mod 2**32: 765 bytes
from pysb import *
Model()
Monomer('C8', ['b'])
Monomer('Bid', ['b', 'S'], {'S': ['u', 't']})
Parameter('kf', 1e-07)
Parameter('kr', 0.001)
Parameter('kc', 1.0)
Rule('C8_Bid_bind', C8(b=None) + Bid(b=None, S='u') | C8(b=1) % Bid(b=1, S='u'), *[kf, kr])
Rule('tBid_from_C8Bid', C8(b=1) % Bid(b=1, S='u') >> C8(b=None) + Bid(b=None, S='t'), kc)
Parameter('C8_0', 1000)
Parameter('Bid_0', 10000)
Initial(C8(b=None), C8_0)
Initial(Bid(b=None, S='u'), Bid_0)
Observable('obsC8', C8(b=None))
Observable('obsBid', Bid(b=None, S='u'))
Observable('obstBid', Bid(b=None, S='t'))