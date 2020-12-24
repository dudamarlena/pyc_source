# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/opengl/glInfo.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 504 bytes
from ..Qt import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
app = QtGui.QApplication([])

class GLTest(QtOpenGL.QGLWidget):

    def __init__(self):
        QtOpenGL.QGLWidget.__init__(self)
        self.makeCurrent()
        print('GL version:' + glGetString(GL_VERSION))
        print('MAX_TEXTURE_SIZE: %d' % glGetIntegerv(GL_MAX_TEXTURE_SIZE))
        print('MAX_3D_TEXTURE_SIZE: %d' % glGetIntegerv(GL_MAX_3D_TEXTURE_SIZE))
        print('Extensions: ' + glGetString(GL_EXTENSIONS))


GLTest()