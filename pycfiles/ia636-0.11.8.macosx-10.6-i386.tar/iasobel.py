# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iasobel.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *
import numpy.oldnumeric.mlab as Mlab
from numpy.oldnumeric.mlab import *

def iasobel(f):
    from iapconv import iapconv
    from ia636 import iaimginfo

    def test_arctan2(x, y):
        from numpy import arctan2
        try:
            return arctan2(x, y)
        except:
            return 0

    wx = array([[1.0, 2.0, 1.0],
     [
      0.0, 0.0, 0.0],
     [
      -1.0, -2.0, -1.0]])
    wy = array([[1.0, 0.0, -1.0],
     [
      2.0, 0.0, -2.0],
     [
      1.0, 0.0, -1.0]])
    gx = iapconv(f, wx)
    gy = iapconv(f, wy)
    mag = abs(gx + gy * complex(0.0, 1.0))
    theta = reshape(map(test_arctan2, ravel(gy), ravel(gx)), f.shape)
    return (mag, theta)