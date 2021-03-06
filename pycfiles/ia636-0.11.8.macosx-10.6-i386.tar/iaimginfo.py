# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iaimginfo.py
# Compiled at: 2014-08-21 22:30:04
import numpy as np

def iaimginfo(f):
    t = type(f)
    if t != np.ndarray:
        return 'Not a ndarray. It is %s' % (t,)
    else:
        dt = f.dtype
        if dt == 'bool':
            return '%s %s %s %s %s' % (t, np.shape(f), f.dtype, f.min(), f.max())
        if dt == 'uint8':
            return '%s %s %s %d %d' % (t, np.shape(f), f.dtype, f.min(), f.max())
        return '%s %s %s %f %f' % (t, np.shape(f), f.dtype, f.min(), f.max())