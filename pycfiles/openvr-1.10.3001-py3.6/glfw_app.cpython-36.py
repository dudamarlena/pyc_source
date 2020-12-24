# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\openvr\glframework\glfw_app.py
# Compiled at: 2019-07-06 13:14:09
# Size of source mod 2**32: 3577 bytes
import glfw
from OpenGL.GL import glFlush

class GlfwBaseApp(object):
    __doc__ = 'Base version renders to desktop'

    def __init__(self, renderer, title='GlfwBaseApp'):
        """Creates an OpenGL context and a window, and acquires OpenGL resources"""
        self.renderer = renderer
        self.title = title
        self._is_initialized = False
        if not glfw.init():
            raise Exception('GLFW Initialization error')
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 5)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        self._configure_context()
        self.window = glfw.create_window(self.renderer.window_size[0], self.renderer.window_size[1], self.title, None, None)
        if self.window is None:
            glfw.terminate()
            raise Exception('GLFW window creation error')
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.make_context_current(self.window)

    def _configure_context(self):
        pass

    def __enter__(self):
        """setup for RAII using 'with' keyword"""
        return self

    def __exit__(self, type_arg, value, traceback):
        """cleanup for RAII using 'with' keyword"""
        self.dispose_gl()

    def init_gl(self):
        if self._is_initialized:
            return
        glfw.make_context_current(self.window)
        if self.renderer:
            self.renderer.init_gl()
        self._is_initialized = True

    def render_scene(self):
        """render scene one time"""
        self.init_gl()
        glfw.make_context_current(self.window)
        self.renderer.render_scene()
        glFlush()
        glfw.poll_events()

    def dispose_gl(self):
        if self.window:
            glfw.make_context_current(self.window)
            if self.renderer:
                self.renderer.dispose_gl()
        glfw.destroy_window(self.window)
        glfw.terminate()
        self._is_initialized = False

    def key_callback(self, window, key, scancode, action, mods):
        """press ESCAPE to quit the application"""
        if key == glfw.KEY_ESCAPE:
            if action == glfw.PRESS:
                glfw.set_window_should_close(self.window, True)

    def run_loop(self):
        """keep rendering until the user says quit"""
        while not glfw.window_should_close(self.window):
            self.render_scene()


class GlfwApp(GlfwBaseApp):
    __doc__ = 'GlfwApp uses glfw library to create an opengl context, listen to keyboard events, and clean up'

    def __init__(self, renderer, title='GlfwApp'):
        super(GlfwApp, self).__init__(renderer=renderer, title=title)
        glfw.swap_interval(0)

    def _configure_context(self):
        glfw.window_hint(glfw.DOUBLEBUFFER, False)


class GlfwVrApp(GlfwApp):

    def __init__(self, actors=[], title='GlfwVrApp'):
        import openvr.gl_renderer
        renderer = openvr.gl_renderer.OpenVrGlRenderer(actor=actors, multisample=2)
        super(GlfwVrApp, self).__init__(renderer=renderer)
        glfw.swap_interval(0)