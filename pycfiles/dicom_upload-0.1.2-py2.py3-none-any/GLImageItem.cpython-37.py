# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/opengl/items/GLImageItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 3664 bytes
from OpenGL.GL import *
from ..GLGraphicsItem import GLGraphicsItem
from ...Qt import QtGui
import numpy as np
__all__ = ['GLImageItem']

class GLImageItem(GLGraphicsItem):
    """GLImageItem"""

    def __init__(self, data, smooth=False, glOptions='translucent'):
        """
        
        ==============  =======================================================================================
        **Arguments:**
        data            Volume data to be rendered. *Must* be 3D numpy array (x, y, RGBA) with dtype=ubyte.
                        (See functions.makeRGBA)
        smooth          (bool) If True, the volume slices are rendered with linear interpolation 
        ==============  =======================================================================================
        """
        self.smooth = smooth
        self._needUpdate = False
        GLGraphicsItem.__init__(self)
        self.setData(data)
        self.setGLOptions(glOptions)

    def initializeGL(self):
        glEnable(GL_TEXTURE_2D)
        self.texture = glGenTextures(1)

    def setData(self, data):
        self.data = data
        self._needUpdate = True
        self.update()

    def _updateTexture(self):
        glBindTexture(GL_TEXTURE_2D, self.texture)
        if self.smooth:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        else:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        shape = self.data.shape
        glTexImage2D(GL_PROXY_TEXTURE_2D, 0, GL_RGBA, shape[0], shape[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        if glGetTexLevelParameteriv(GL_PROXY_TEXTURE_2D, 0, GL_TEXTURE_WIDTH) == 0:
            raise Exception('OpenGL failed to create 2D texture (%dx%d); too large for this hardware.' % shape[:2])
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, shape[0], shape[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, self.data.transpose((1,
                                                                                                                       0,
                                                                                                                       2)))
        glDisable(GL_TEXTURE_2D)

    def paint(self):
        if self._needUpdate:
            self._updateTexture()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        self.setupGLState()
        glColor4f(1, 1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(0, 0, 0)
        glTexCoord2f(1, 0)
        glVertex3f(self.data.shape[0], 0, 0)
        glTexCoord2f(1, 1)
        glVertex3f(self.data.shape[0], self.data.shape[1], 0)
        glTexCoord2f(0, 1)
        glVertex3f(0, self.data.shape[1], 0)
        glEnd()
        glDisable(GL_TEXTURE_3D)