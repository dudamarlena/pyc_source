# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/RawImageWidget.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 5410 bytes
from ..Qt import QtCore, QtGui
try:
    from ..Qt import QtOpenGL
    from OpenGL.GL import *
    HAVE_OPENGL = True
except ImportError:
    HAVE_OPENGL = False

from .. import functions as fn
import numpy as np

class RawImageWidget(QtGui.QWidget):
    __doc__ = '\n    Widget optimized for very fast video display. \n    Generally using an ImageItem inside GraphicsView is fast enough.\n    On some systems this may provide faster video. See the VideoSpeedTest example for benchmarking.\n    '

    def __init__(self, parent=None, scaled=False):
        """
        Setting scaled=True will cause the entire image to be displayed within the boundaries of the widget. This also greatly reduces the speed at which it will draw frames.
        """
        QtGui.QWidget.__init__(self, parent=None)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        self.scaled = scaled
        self.opts = None
        self.image = None

    def setImage(self, img, *args, **kargs):
        """
        img must be ndarray of shape (x,y), (x,y,3), or (x,y,4).
        Extra arguments are sent to functions.makeARGB
        """
        self.opts = (
         img, args, kargs)
        self.image = None
        self.update()

    def paintEvent(self, ev):
        if self.opts is None:
            return
        else:
            if self.image is None:
                argb, alpha = (fn.makeARGB)(self.opts[0], *(self.opts[1]), **self.opts[2])
                self.image = fn.makeQImage(argb, alpha)
                self.opts = ()
            p = QtGui.QPainter(self)
            if self.scaled:
                rect = self.rect()
                ar = rect.width() / float(rect.height())
                imar = self.image.width() / float(self.image.height())
                if ar > imar:
                    rect.setWidth(int(rect.width() * imar / ar))
                else:
                    rect.setHeight(int(rect.height() * ar / imar))
                p.drawImage(rect, self.image)
            else:
                p.drawImage(QtCore.QPointF(), self.image)
        p.end()


if HAVE_OPENGL:

    class RawImageGLWidget(QtOpenGL.QGLWidget):
        __doc__ = '\n        Similar to RawImageWidget, but uses a GL widget to do all drawing.\n        Perfomance varies between platforms; see examples/VideoSpeedTest for benchmarking.\n        '

        def __init__(self, parent=None, scaled=False):
            QtOpenGL.QGLWidget.__init__(self, parent=None)
            self.scaled = scaled
            self.image = None
            self.uploaded = False
            self.smooth = False
            self.opts = None

        def setImage(self, img, *args, **kargs):
            """
            img must be ndarray of shape (x,y), (x,y,3), or (x,y,4).
            Extra arguments are sent to functions.makeARGB
            """
            self.opts = (
             img, args, kargs)
            self.image = None
            self.uploaded = False
            self.update()

        def initializeGL(self):
            self.texture = glGenTextures(1)

        def uploadTexture(self):
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            if self.smooth:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            else:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
            shape = self.image.shape
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, shape[0], shape[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, self.image.transpose((1,
                                                                                                                            0,
                                                                                                                            2)))
            glDisable(GL_TEXTURE_2D)

        def paintGL(self):
            if self.image is None:
                if self.opts is None:
                    return
                img, args, kwds = self.opts
                kwds['useRGBA'] = True
                self.image, alpha = (fn.makeARGB)(img, *args, **kwds)
            if not self.uploaded:
                self.uploadTexture()
            glViewport(0, 0, self.width(), self.height())
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glColor4f(1, 1, 1, 1)
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex3f(-1, -1, 0)
            glTexCoord2f(1, 0)
            glVertex3f(1, -1, 0)
            glTexCoord2f(1, 1)
            glVertex3f(1, 1, 0)
            glTexCoord2f(0, 1)
            glVertex3f(-1, 1, 0)
            glEnd()
            glDisable(GL_TEXTURE_3D)