# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/ianormalize.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def ianormalize(f, range=[
 0, 255]):
    f = asarray(f)
    range = asarray(range)
    if f.dtype.char in ('D', 'F'):
        raise Exception, 'error: cannot normalize complex data'
    faux = ravel(f).astype(float)
    minimum = faux.min()
    maximum = faux.max()
    lower = range[0]
    upper = range[1]
    if upper == lower:
        g = ones(f.shape) * maximum
    if minimum == maximum:
        g = ones(f.shape) * (upper + lower) / 2.0
    else:
        g = (faux - minimum) * (upper - lower) / (maximum - minimum) + lower
    g = reshape(g, f.shape)
    if f.dtype == uint8:
        if upper > 255:
            raise Exception, 'ianormalize: warning, upper valuer larger than 255. Cannot fit in uint8 image'
    g = g.astype(f.dtype)
    return g