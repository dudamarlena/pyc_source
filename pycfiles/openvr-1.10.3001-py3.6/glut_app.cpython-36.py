# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\openvr\glframework\glut_app.py
# Compiled at: 2017-04-12 18:00:37
# Size of source mod 2**32: 2508 bytes
from OpenGL.GL import *
from OpenGL.GLUT import *

class GlutApp(object):
    __doc__ = 'GlutApp uses freeglut library to create an opengl context, listen to keyboard events, and clean up'

    def __init__(self, renderer, title=b'GLUT test'):
        """Creates an OpenGL context and a window, and acquires OpenGL resources"""
        self.renderer = renderer
        self.title = title
        self.window = None
        self.init_gl()

    def __enter__(self):
        """setup for RAII using 'with' keyword"""
        return self

    def __exit__(self, type_arg, value, traceback):
        """cleanup for RAII using 'with' keyword"""
        self.dispose_gl()

    def init_gl(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH | GLUT_SINGLE)
        if bool(glutInitContextVersion):
            glutInitContextVersion(4, 1)
        glutInitWindowSize(800, 600)
        glutInitWindowPosition(50, 50)
        self.window = glutCreateWindow(self.title)
        glutDisplayFunc(self.render_scene)
        glutIdleFunc(self.render_scene)
        glutReshapeFunc(self.resize_gl)
        glutKeyboardFunc(self.key_press)
        if self.renderer is not None:
            self.renderer.init_gl()

    def render_scene(self):
        """render scene one time"""
        self.renderer.render_scene()
        glFlush()

    def dispose_gl(self):
        if self.window is not None:
            if self.renderer is not None:
                self.renderer.dispose_gl()
            self.window = None
        self._is_initialized = False

    def key_press(self, key, x, y):
        """Close the application when the player presses ESCAPE"""
        if ord(key) == 27:
            if bool(glutLeaveMainLoop):
                glutLeaveMainLoop()
            else:
                raise Exception('Application quit')

    def resize_gl(self, width, height):
        """Called every time the on-screen window is resized"""
        glViewport(0, 0, width, height)

    def run_loop(self):
        """keep rendering until the user says quit"""
        glutMainLoop()