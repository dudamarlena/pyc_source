# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/houghcircles.py
# Compiled at: 2008-01-29 20:48:29
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