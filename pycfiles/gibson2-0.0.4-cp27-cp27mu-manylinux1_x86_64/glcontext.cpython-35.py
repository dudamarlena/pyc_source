# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fei/Development/gibsonv2/gibson2/core/render/mesh_renderer/glutils/glcontext.py
# Compiled at: 2020-03-24 04:06:03
# Size of source mod 2**32: 4305 bytes
"""Headless GPU-accelerated OpenGL context creation on Google Colaboratory.

Typical usage:

    # Optional PyOpenGL configuratiopn can be done here.
    # import OpenGL
    # OpenGL.ERROR_CHECKING = True

    # 'glcontext' must be imported before any OpenGL.* API.
    from lucid.misc.gl.glcontext import create_opengl_context

    # Now it's safe to import OpenGL and EGL functions
    import OpenGL.GL as gl

    # create_opengl_context() creates a GL context that is attached to an
    # offscreen surface of the specified size. Note that rendering to buffers
    # of other sizes and formats is still possible with OpenGL Framebuffers.
    #
    # Users are expected to directly use the EGL API in case more advanced
    # context management is required.
    width, height = 640, 480
    create_opengl_context((width, height))

    # OpenGL context is available here.

"""
from __future__ import print_function
try:
    import OpenGL
except:
    print('This module depends on PyOpenGL.')
    print('Please run "\x1b[1m!pip install -q pyopengl\x1b[0m" prior importing this module.')
    raise

import ctypes
from ctypes import pointer
from ctypes import util
from ctypes.util import find_library
import os
os.environ['PYOPENGL_PLATFORM'] = 'egl'
_find_library_old = ctypes.util.find_library
try:
    try:

        def _find_library_new(name):
            return {'GL': 'libOpenGL.so', 
             'EGL': 'libEGL.so'}.get(name, _find_library_old(name))


        ctypes.util.find_library = _find_library_new
        import OpenGL.GL as gl, OpenGL.EGL as egl
    except:
        print('Unable to load OpenGL libraries. Make sure you use GPU-enabled backend.')
        print('Press "Runtime->Change runtime type" and set "Hardware accelerator" to GPU.')
        raise

finally:
    ctypes.util.find_library = _find_library_old

class Context:

    def __init__(self):
        pass

    def create_opengl_context(self, surface_size=(640, 480)):
        """Create offscreen OpenGL context and make it current.

        Users are expected to directly use EGL API in case more advanced
        context management is required.

        Args:
        surface_size: (width, height), size of the offscreen rendering surface.
        """
        egl_display = egl.eglGetDisplay(egl.EGL_DEFAULT_DISPLAY)
        major, minor = egl.EGLint(), egl.EGLint()
        egl.eglInitialize(egl_display, pointer(major), pointer(minor))
        config_attribs = [
         egl.EGL_SURFACE_TYPE, egl.EGL_PBUFFER_BIT, egl.EGL_BLUE_SIZE, 8, egl.EGL_GREEN_SIZE, 8,
         egl.EGL_RED_SIZE, 8, egl.EGL_DEPTH_SIZE, 24, egl.EGL_RENDERABLE_TYPE,
         egl.EGL_OPENGL_BIT, egl.EGL_NONE]
        config_attribs = egl.EGLint * len(config_attribs)(*config_attribs)
        num_configs = egl.EGLint()
        egl_cfg = egl.EGLConfig()
        egl.eglChooseConfig(egl_display, config_attribs, pointer(egl_cfg), 1, pointer(num_configs))
        width, height = surface_size
        pbuffer_attribs = [
         egl.EGL_WIDTH,
         width,
         egl.EGL_HEIGHT,
         height,
         egl.EGL_NONE]
        pbuffer_attribs = egl.EGLint * len(pbuffer_attribs)(*pbuffer_attribs)
        egl_surf = egl.eglCreatePbufferSurface(egl_display, egl_cfg, pbuffer_attribs)
        egl.eglBindAPI(egl.EGL_OPENGL_API)
        egl_context = egl.eglCreateContext(egl_display, egl_cfg, egl.EGL_NO_CONTEXT, None)
        egl.eglMakeCurrent(egl_display, egl_surf, egl_surf, egl_context)
        self.display = egl_display

    def destroy(self):
        egl.eglTerminate(self.display)