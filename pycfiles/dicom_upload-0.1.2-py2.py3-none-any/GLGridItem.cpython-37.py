# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/opengl/items/GLGridItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2277 bytes
import numpy as np
from OpenGL.GL import *
from ..GLGraphicsItem import GLGraphicsItem
from ... import QtGui
__all__ = [
 'GLGridItem']

class GLGridItem(GLGraphicsItem):
    """GLGridItem"""

    def __init__(self, size=None, color=None, antialias=True, glOptions='translucent'):
        GLGraphicsItem.__init__(self)
        self.setGLOptions(glOptions)
        self.antialias = antialias
        if size is None:
            size = QtGui.QVector3D(20, 20, 1)
        self.setSize(size=size)
        self.setSpacing(1, 1, 1)

    def setSize(self, x=None, y=None, z=None, size=None):
        """
        Set the size of the axes (in its local coordinate system; this does not affect the transform)
        Arguments can be x,y,z or size=QVector3D().
        """
        if size is not None:
            x = size.x()
            y = size.y()
            z = size.z()
        self._GLGridItem__size = [
         x, y, z]
        self.update()

    def size(self):
        return self._GLGridItem__size[:]

    def setSpacing(self, x=None, y=None, z=None, spacing=None):
        """
        Set the spacing between grid lines.
        Arguments can be x,y,z or spacing=QVector3D().
        """
        if spacing is not None:
            x = spacing.x()
            y = spacing.y()
            z = spacing.z()
        self._GLGridItem__spacing = [
         x, y, z]
        self.update()

    def spacing(self):
        return self._GLGridItem__spacing[:]

    def paint(self):
        self.setupGLState()
        if self.antialias:
            glEnable(GL_LINE_SMOOTH)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glBegin(GL_LINES)
        x, y, z = self.size()
        xs, ys, zs = self.spacing()
        xvals = np.arange(-x / 2.0, x / 2.0 + xs * 0.001, xs)
        yvals = np.arange(-y / 2.0, y / 2.0 + ys * 0.001, ys)
        glColor4f(1, 1, 1, 0.3)
        for x in xvals:
            glVertex3f(x, yvals[0], 0)
            glVertex3f(x, yvals[(-1)], 0)

        for y in yvals:
            glVertex3f(xvals[0], y, 0)
            glVertex3f(xvals[(-1)], y, 0)

        glEnd()