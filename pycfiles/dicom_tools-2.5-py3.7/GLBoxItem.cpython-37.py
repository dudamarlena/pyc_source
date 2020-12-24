# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/opengl/items/GLBoxItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2470 bytes
from OpenGL.GL import *
from ..GLGraphicsItem import GLGraphicsItem
from ...Qt import QtGui
from ... import functions as fn
__all__ = ['GLBoxItem']

class GLBoxItem(GLGraphicsItem):
    __doc__ = '\n    **Bases:** :class:`GLGraphicsItem <pyqtgraph.opengl.GLGraphicsItem>`\n    \n    Displays a wire-frame box.\n    '

    def __init__(self, size=None, color=None, glOptions='translucent'):
        GLGraphicsItem.__init__(self)
        if size is None:
            size = QtGui.QVector3D(1, 1, 1)
        self.setSize(size=size)
        if color is None:
            color = (255, 255, 255, 80)
        self.setColor(color)
        self.setGLOptions(glOptions)

    def setSize(self, x=None, y=None, z=None, size=None):
        """
        Set the size of the box (in its local coordinate system; this does not affect the transform)
        Arguments can be x,y,z or size=QVector3D().
        """
        if size is not None:
            x = size.x()
            y = size.y()
            z = size.z()
        self._GLBoxItem__size = [
         x, y, z]
        self.update()

    def size(self):
        return self._GLBoxItem__size[:]

    def setColor(self, *args):
        """Set the color of the box. Arguments are the same as those accepted by functions.mkColor()"""
        self._GLBoxItem__color = (fn.Color)(*args)

    def color(self):
        return self._GLBoxItem__color

    def paint(self):
        self.setupGLState()
        glBegin(GL_LINES)
        glColor4f(*self.color().glColor())
        x, y, z = self.size()
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, z)
        glVertex3f(x, 0, 0)
        glVertex3f(x, 0, z)
        glVertex3f(0, y, 0)
        glVertex3f(0, y, z)
        glVertex3f(x, y, 0)
        glVertex3f(x, y, z)
        glVertex3f(0, 0, 0)
        glVertex3f(0, y, 0)
        glVertex3f(x, 0, 0)
        glVertex3f(x, y, 0)
        glVertex3f(0, 0, z)
        glVertex3f(0, y, z)
        glVertex3f(x, 0, z)
        glVertex3f(x, y, z)
        glVertex3f(0, 0, 0)
        glVertex3f(x, 0, 0)
        glVertex3f(0, y, 0)
        glVertex3f(x, y, 0)
        glVertex3f(0, 0, z)
        glVertex3f(x, 0, z)
        glVertex3f(0, y, z)
        glVertex3f(x, y, z)
        glEnd()