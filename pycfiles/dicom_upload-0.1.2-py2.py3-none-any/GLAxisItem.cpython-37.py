# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/opengl/items/GLAxisItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1792 bytes
from OpenGL.GL import *
from ..GLGraphicsItem import GLGraphicsItem
from ... import QtGui
__all__ = ['GLAxisItem']

class GLAxisItem(GLGraphicsItem):
    """GLAxisItem"""

    def __init__(self, size=None, antialias=True, glOptions='translucent'):
        GLGraphicsItem.__init__(self)
        if size is None:
            size = QtGui.QVector3D(1, 1, 1)
        self.antialias = antialias
        self.setSize(size=size)
        self.setGLOptions(glOptions)

    def setSize(self, x=None, y=None, z=None, size=None):
        """
        Set the size of the axes (in its local coordinate system; this does not affect the transform)
        Arguments can be x,y,z or size=QVector3D().
        """
        if size is not None:
            x = size.x()
            y = size.y()
            z = size.z()
        self._GLAxisItem__size = [
         x, y, z]
        self.update()

    def size(self):
        return self._GLAxisItem__size[:]

    def paint(self):
        self.setupGLState()
        if self.antialias:
            glEnable(GL_LINE_SMOOTH)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glBegin(GL_LINES)
        x, y, z = self.size()
        glColor4f(0, 1, 0, 0.6)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, z)
        glColor4f(1, 1, 0, 0.6)
        glVertex3f(0, 0, 0)
        glVertex3f(0, y, 0)
        glColor4f(0, 0, 1, 0.6)
        glVertex3f(0, 0, 0)
        glVertex3f(x, 0, 0)
        glEnd()