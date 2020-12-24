# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Ctrax/houghcircles.py
# Compiled at: 2013-09-24 00:46:30
__doc__ = 'houghcircles interface using ctypes.\n'
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