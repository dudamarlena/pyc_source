# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/core/stats/emas_visualization.py
# Compiled at: 2015-12-21 17:12:57
from numpy import pi, sin, cos, mgrid
dphi, dtheta = pi / 20.0, pi / 10.0
phi, theta = mgrid[0:2 * pi + dphi * 1.5:dphi, 0:2 * pi + dtheta * 1.5:dtheta]
r = 1
R = 3
x = (R + r * cos(theta)) * cos(phi)
y = (R + r * cos(theta)) * sin(phi)
z = r * sin(theta)
from mayavi import mlab
s = mlab.mesh(x, y, z, representation='points', color=(0, 0, 0), scale_factor=0.9, mask=[])
mlab.show()