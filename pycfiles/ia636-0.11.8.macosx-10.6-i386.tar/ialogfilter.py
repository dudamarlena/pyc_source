# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/ialogfilter.py
# Compiled at: 2014-08-21 22:30:04
from numpy.fft import fft2, ifft2
from numpy import *

def ialogfilter(f, sigma):
    from ialog import ialog
    from iaifftshift import iaifftshift
    from iaisdftsym import iaisdftsym
    if len(shape(f)) == 1:
        f = f[newaxis, :]
    h = ialog(shape(f), map(int, array(shape(f)) / 2.0), sigma)
    h = iaifftshift(h)
    H = fft2(h)
    if not iaisdftsym(H):
        raise Exception, 'error: log filter is not symmetrical'
    G = fft2(f) * H
    g = ifft2(G).real
    return g