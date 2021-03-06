# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/opengl/items/GLVolumeItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 7658 bytes
from OpenGL.GL import *
from ..GLGraphicsItem import GLGraphicsItem
from ...Qt import QtGui
import numpy as np
from ... import debug
__all__ = ['GLVolumeItem']

class GLVolumeItem(GLGraphicsItem):
    __doc__ = '\n    **Bases:** :class:`GLGraphicsItem <pyqtgraph.opengl.GLGraphicsItem>`\n    \n    Displays volumetric data. \n    '

    def __init__(self, data, sliceDensity=1, smooth=True, glOptions='translucent'):
        """
        ==============  =======================================================================================
        **Arguments:**
        data            Volume data to be rendered. *Must* be 4D numpy array (x, y, z, RGBA) with dtype=ubyte.
        sliceDensity    Density of slices to render through the volume. A value of 1 means one slice per voxel.
        smooth          (bool) If True, the volume slices are rendered with linear interpolation 
        ==============  =======================================================================================
        """
        self.sliceDensity = sliceDensity
        self.smooth = smooth
        self.data = None
        self._needUpload = False
        self.texture = None
        GLGraphicsItem.__init__(self)
        self.setGLOptions(glOptions)
        self.setData(data)

    def setData(self, data):
        self.data = data
        self._needUpload = True
        self.update()

    def _uploadData(self):
        glEnable(GL_TEXTURE_3D)
        if self.texture is None:
            self.texture = glGenTextures(1)
        else:
            glBindTexture(GL_TEXTURE_3D, self.texture)
            if self.smooth:
                glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            else:
                glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_BORDER)
        shape = self.data.shape
        glTexImage3D(GL_PROXY_TEXTURE_3D, 0, GL_RGBA, shape[0], shape[1], shape[2], 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        if glGetTexLevelParameteriv(GL_PROXY_TEXTURE_3D, 0, GL_TEXTURE_WIDTH) == 0:
            raise Exception('OpenGL failed to create 3D texture (%dx%dx%d); too large for this hardware.' % shape[:3])
        glTexImage3D(GL_TEXTURE_3D, 0, GL_RGBA, shape[0], shape[1], shape[2], 0, GL_RGBA, GL_UNSIGNED_BYTE, self.data.transpose((2,
                                                                                                                                 1,
                                                                                                                                 0,
                                                                                                                                 3)))
        glDisable(GL_TEXTURE_3D)
        self.lists = {}
        for ax in (0, 1, 2):
            for d in (-1, 1):
                l = glGenLists(1)
                self.lists[(ax, d)] = l
                glNewList(l, GL_COMPILE)
                self.drawVolume(ax, d)
                glEndList()

        self._needUpload = False

    def paint(self):
        if self.data is None:
            return
        if self._needUpload:
            self._uploadData()
        self.setupGLState()
        glEnable(GL_TEXTURE_3D)
        glBindTexture(GL_TEXTURE_3D, self.texture)
        glColor4f(1, 1, 1, 1)
        view = self.view()
        center = (QtGui.QVector3D)(*[x / 2.0 for x in self.data.shape[:3]])
        cam = self.mapFromParent(view.cameraPosition()) - center
        cam = np.array([cam.x(), cam.y(), cam.z()])
        ax = np.argmax(abs(cam))
        d = 1 if cam[ax] > 0 else -1
        glCallList(self.lists[(ax, d)])
        glDisable(GL_TEXTURE_3D)

    def drawVolume(self, ax, d):
        N = 5
        imax = [
         0, 1, 2]
        imax.remove(ax)
        tp = [
         [
          0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        vp = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        nudge = [0.5 / x for x in self.data.shape]
        tp[0][imax[0]] = 0 + nudge[imax[0]]
        tp[0][imax[1]] = 0 + nudge[imax[1]]
        tp[1][imax[0]] = 1 - nudge[imax[0]]
        tp[1][imax[1]] = 0 + nudge[imax[1]]
        tp[2][imax[0]] = 1 - nudge[imax[0]]
        tp[2][imax[1]] = 1 - nudge[imax[1]]
        tp[3][imax[0]] = 0 + nudge[imax[0]]
        tp[3][imax[1]] = 1 - nudge[imax[1]]
        vp[0][imax[0]] = 0
        vp[0][imax[1]] = 0
        vp[1][imax[0]] = self.data.shape[imax[0]]
        vp[1][imax[1]] = 0
        vp[2][imax[0]] = self.data.shape[imax[0]]
        vp[2][imax[1]] = self.data.shape[imax[1]]
        vp[3][imax[0]] = 0
        vp[3][imax[1]] = self.data.shape[imax[1]]
        slices = self.data.shape[ax] * self.sliceDensity
        r = list(range(slices))
        if d == -1:
            r = r[::-1]
        glBegin(GL_QUADS)
        tzVals = np.linspace(nudge[ax], 1.0 - nudge[ax], slices)
        vzVals = np.linspace(0, self.data.shape[ax], slices)
        for i in r:
            z = tzVals[i]
            w = vzVals[i]
            tp[0][ax] = z
            tp[1][ax] = z
            tp[2][ax] = z
            tp[3][ax] = z
            vp[0][ax] = w
            vp[1][ax] = w
            vp[2][ax] = w
            vp[3][ax] = w
            glTexCoord3f(*tp[0])
            glVertex3f(*vp[0])
            glTexCoord3f(*tp[1])
            glVertex3f(*vp[1])
            glTexCoord3f(*tp[2])
            glVertex3f(*vp[2])
            glTexCoord3f(*tp[3])
            glVertex3f(*vp[3])

        glEnd()