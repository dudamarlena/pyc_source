# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mapy\constants.py
# Compiled at: 2017-04-20 23:17:36
# Size of source mod 2**32: 306 bytes
from alg3dpy.vector import asvector
from alg3dpy.constants import Z, O, FLOAT, ZER, INT
from mapy.model.coords import CoordR
vecxz = asvector([1.0, 0.0, 1.0])
CSYSGLOBAL = CoordR(0, O, None, Z, vecxz)
CSYSGLOBAL.rebuild(rcobj=None, force_new_axis=False)
CSYSGLOBAL.rcobj = CSYSGLOBAL
MAXID = 99999999