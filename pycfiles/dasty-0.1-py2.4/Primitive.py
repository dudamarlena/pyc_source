# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/dasty/core/Primitive.py
# Compiled at: 2007-06-28 09:07:49
"""Define the Primitive class

Author: Jean-Christophe Hoelt <hoelt@irit.fr>
Copyright (c) 2007, IRIT-CNRS

This file is released under the CECILL-C licence.
"""

class Primitive(object):
    """An object having ability to draw itself.

    Attributes:
    aabbox -- Axis Aligned Bounding Box (xmin,xmax,ymin,ymax,zmin,zmax)

    """
    __module__ = __name__

    def __init__(self):
        self.aabbox = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    def compile(self):
        """Perform necessary precomputations"""
        pass

    def gl_draw(self, viewplatform, wsize):
        """Draw the primitive to OpenGL active context.

        Keyword arguments:
        viewplatform -- a ViewPlatform defining the user camera
        wsize -- size in pixels of the aabbox projected on screen (w,h)

        """
        pass