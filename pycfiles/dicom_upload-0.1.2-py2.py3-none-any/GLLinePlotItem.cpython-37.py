# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/opengl/items/GLLinePlotItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 4374 bytes
from OpenGL.GL import *
from OpenGL.arrays import vbo
from ..GLGraphicsItem import GLGraphicsItem
from .. import shaders
from ... import QtGui
import numpy as np
__all__ = ['GLLinePlotItem']

class GLLinePlotItem(GLGraphicsItem):
    """GLLinePlotItem"""

    def __init__(self, **kwds):
        """All keyword arguments are passed to setData()"""
        GLGraphicsItem.__init__(self)
        glopts = kwds.pop('glOptions', 'additive')
        self.setGLOptions(glopts)
        self.pos = None
        self.mode = 'line_strip'
        self.width = 1.0
        self.color = (1.0, 1.0, 1.0, 1.0)
        (self.setData)(**kwds)

    def setData(self, **kwds):
        """
        Update the data displayed by this item. All arguments are optional; 
        for example it is allowed to update vertex positions while leaving 
        colors unchanged, etc.
        
        ====================  ==================================================
        **Arguments:**
        ------------------------------------------------------------------------
        pos                   (N,3) array of floats specifying point locations.
        color                 (N,4) array of floats (0.0-1.0) or
                              tuple of floats specifying
                              a single color for the entire item.
        width                 float specifying line width
        antialias             enables smooth line drawing
        mode                  'lines': Each pair of vertexes draws a single line
                                       segment.
                              'line_strip': All vertexes are drawn as a
                                            continuous set of line segments.
        ====================  ==================================================
        """
        args = [
         'pos', 'color', 'width', 'mode', 'antialias']
        for k in kwds.keys():
            if k not in args:
                raise Exception('Invalid keyword argument: %s (allowed arguments are %s)' % (k, str(args)))

        self.antialias = False
        for arg in args:
            if arg in kwds:
                setattr(self, arg, kwds[arg])

        self.update()

    def initializeGL(self):
        pass

    def paint(self):
        if self.pos is None:
            return
        self.setupGLState()
        glEnableClientState(GL_VERTEX_ARRAY)
        try:
            glVertexPointerf(self.pos)
            if isinstance(self.color, np.ndarray):
                glEnableClientState(GL_COLOR_ARRAY)
                glColorPointerf(self.color)
            elif isinstance(self.color, QtGui.QColor):
                glColor4f(*fn.glColor(self.color))
            else:
                glColor4f(*self.color)
            glLineWidth(self.width)
            if self.antialias:
                glEnable(GL_LINE_SMOOTH)
                glEnable(GL_BLEND)
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
            elif self.mode == 'line_strip':
                glDrawArrays(GL_LINE_STRIP, 0, int(self.pos.size / self.pos.shape[(-1)]))
            elif self.mode == 'lines':
                glDrawArrays(GL_LINES, 0, int(self.pos.size / self.pos.shape[(-1)]))
            else:
                raise Exception("Unknown line mode '%s'. (must be 'lines' or 'line_strip')" % self.mode)
        finally:
            glDisableClientState(GL_COLOR_ARRAY)
            glDisableClientState(GL_VERTEX_ARRAY)