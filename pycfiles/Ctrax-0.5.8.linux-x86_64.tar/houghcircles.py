# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Ctrax/houghcircles.py
# Compiled at: 2013-09-24 00:46:30
"""houghcircles interface using ctypes.
"""
import numpy as num
from houghcircles_C import houghcircles_C

def houghcircles(x, y, w, binedgesa, bincentersb, bincentersr, hlib=None):
    npts = len(x)
    na = len(binedgesa) - 1
    nb = len(bincentersb)
    nr = len(bincentersr)
    acc = houghcircles_C(x, y, w, binedgesa, bincentersb, bincentersr)
    acc = acc.swapaxes(0, 2)
    return acc