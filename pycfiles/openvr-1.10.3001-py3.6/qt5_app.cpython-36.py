# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\openvr\glframework\qt5_app.py
# Compiled at: 2017-04-19 20:54:45
# Size of source mod 2**32: 3157 bytes
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtOpenGL import QGLWidget, QGLFormat

class MyGlWidget(QGLWidget):
    __doc__ = 'PySideApp uses Qt library to create an opengl context, listen to keyboard events, and clean up'

    def __init__(self, renderer, glformat, app):
        super(MyGlWidget, self).__init__(glformat)
        self.renderer = renderer
        self.app = app
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(0)
        self.timer.timeout.connect(self.render_vr)
        self.setFocusPolicy(Qt.StrongFocus)

    def __enter__(self):
        """setup for RAII using 'with' keyword"""
        return self

    def __exit__(self, type_arg, value, traceback):
        """cleanup for RAII using 'with' keyword"""
        self.dispose_gl()

    def initializeGL(self):
        if self.renderer is not None:
            self.renderer.init_gl()
        self.timer.start()

    def paintGL(self):
        """render scene one time"""
        self.renderer.render_scene()
        self.swapBuffers()

    def render_vr(self):
        self.makeCurrent()
        self.paintGL()
        self.doneCurrent()
        self.timer.start()

    def disposeGL(self):
        if self.renderer is not None:
            self.makeCurrent()
            self.renderer.dispose_gl()
            self.doneCurrent()

    def keyPressEvent(self, event):
        """press ESCAPE to quit the application"""
        key = event.key()
        if key == Qt.Key_Escape:
            self.app.quit()


class Qt5App(QApplication):

    def __init__(self, renderer, title):
        QApplication.__init__(self, sys.argv)
        self.window = QMainWindow()
        self.window.setWindowTitle(title)
        self.window.resize(800, 600)
        glformat = QGLFormat()
        glformat.setVersion(4, 1)
        glformat.setProfile(QGLFormat.CoreProfile)
        glformat.setDoubleBuffer(False)
        self.glwidget = MyGlWidget(renderer, glformat, self)
        self.window.setCentralWidget(self.glwidget)
        self.window.show()

    def __enter__(self):
        """setup for RAII using 'with' keyword"""
        return self

    def __exit__(self, type_arg, value, traceback):
        """cleanup for RAII using 'with' keyword"""
        self.glwidget.disposeGL()

    def run_loop(self):
        retval = self.exec_()
        sys.exit(retval)


if __name__ == '__main__':
    from openvr.gl_renderer import OpenVrGlRenderer
    from openvr.color_cube_actor import ColorCubeActor
    actor = ColorCubeActor()
    renderer = OpenVrGlRenderer(actor)
    with Qt5App(renderer, 'PySide OpenVR color cube') as (qtPysideApp):
        qtPysideApp.run_loop()