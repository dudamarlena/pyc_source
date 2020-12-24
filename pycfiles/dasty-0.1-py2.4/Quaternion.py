# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/dasty/core/Quaternion.py
# Compiled at: 2007-06-28 09:07:49
"""Define the Quaternion class

Author: Jean-Christophe Hoelt <hoelt@irit.fr>
Copyright (c) 2007, IRIT-CNRS

This file is released under the CECILL-C licence.
"""
import OpenGLContext.quaternion as quat

class Quaternion(quat.Quaternion):
    """Quaternion object implementing those methods required
    to be useful for OpenGL rendering (and not many others)"""
    __module__ = __name__

    def from_XYZR(x, y, z, r):
        """Create a new quaternion from a VRML-style rotation

        Keyword arguments:
        x,y,z -- Axis of rotation
        r - Rotation in radians.
           
        """
        return quat.fromXYZR(x, y, z, r)

    from_XYZR = staticmethod(from_XYZR)

    def from_euler(x=0.0, y=0.0, z=0.0):
        """Create a new quaternion from a 3-element euler-angle
        rotation about x, then y, then z

        """
        return quat.fromEuler(x, y, z)

    from_euler = staticmethod(from_euler)