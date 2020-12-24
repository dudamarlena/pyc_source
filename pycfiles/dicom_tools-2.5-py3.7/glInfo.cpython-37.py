# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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