# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/brianbruggeman/repos/mine/oogli/oogli/utils.py
# Compiled at: 2016-02-05 22:07:28
import glfw
from glfw import gl
import numpy as np

def screenshot(win, pixels=None):
    width, height = win.width, win.height
    if not isinstance(pixels, np.ndarray):
        shape = (
         width, height, 3)
        pixels = np.zeros(shape, dtype=np.uint8)
    return gl.read_pixels(0, 0, width, height, gl.RGB, gl.UNSIGNED_BYTE, pixels)


def opengl_supported(major, minor):
    """Determines if opengl is supported for the version provided"""
    assert glfw.core.init() != 0
    version = (major, minor)
    glfw.core.window_hint(glfw.CONTEXT_VERSION_MAJOR, major)
    glfw.core.window_hint(glfw.CONTEXT_VERSION_MINOR, minor)
    profile = glfw.OPENGL_ANY_PROFILE if version < (3, 2) else glfw.OPENGL_CORE_PROFILE
    glfw.core.window_hint(glfw.OPENGL_PROFILE, profile)
    forward_compat = gl.FALSE if version < (3, 0) else gl.TRUE
    glfw.core.window_hint(glfw.OPENGL_FORWARD_COMPAT, forward_compat)
    glfw.core.window_hint(glfw.VISIBLE, gl.FALSE)
    glfw.core.window_hint(glfw.FOCUSED, gl.FALSE)
    win = glfw.create_window(title='test', width=1, height=1)
    return win is not None


uniform_mapping = {'vec1': gl.uniform_1f, 
   'vec2': gl.uniform_2f, 
   'vec3': gl.uniform_3f}