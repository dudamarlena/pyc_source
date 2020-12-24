# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\spyre_objects.py
# Compiled at: 2006-01-06 22:08:10
""" Object classes for spyre engines
"""
__program__ = 'stereo_zoe_objects'
__author__ = 'David Keeney <dkeeney@travelbyroad.net>'
__copyright__ = 'Copyright (C) 2004 David Keeney'
__license__ = 'Python '
import spyre, sys, OpenGL.GL as ogl

class DisplayListObject(spyre.Object):
    """Object that stores graphic elements as OpenGL Display
    Lists for quicker display
    """
    __module__ = __name__

    def __init__(self):
        """Initialize new instance. """
        spyre.Object.__init__(self)
        self.DLId = 0
        spyre.Object.opengl_state_dependent.append(self)

    def display(self):
        """Compiles display into display list and displays it"""
        if self.DLId > 0:
            ogl.glCallList(self.DLId)
        else:
            if self.DLId == 0:
                self.DLId = ogl.glGenLists(1)
            else:
                self.DLId = -self.DLId
            ogl.glNewList(self.DLId, ogl.GL_COMPILE_AND_EXECUTE)
            self._display()
            ogl.glEndList()

    def _display(self):
        """Display the object.  This method must be overridden."""
        raise NotImplementedError

    def regenerate(self):
        """Regenerate display list """
        self.DLId = -self.DLId