# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\cocos2020\cocos\gl_framebuffer_object.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 3589 bytes
"""A thin wrapper for OpenGL framebuffer objets. For implementation use only"""
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import ctypes as ct
from pyglet import gl

class FramebufferObject(object):
    __doc__ = '\n    Wrapper for framebuffer objects. See\n\n    http://oss.sgi.com/projects/ogl-sample/registry/EXT/framebuffer_object.txt\n\n    API is not very OO, should be improved.\n    '

    def __init__(self):
        """Create a new framebuffer object"""
        id = gl.GLuint(0)
        gl.glGenFramebuffersEXT(1, ct.byref(id))
        self._id = id.value

    def bind(self):
        """Set FBO as current rendering target"""
        gl.glBindFramebufferEXT(gl.GL_FRAMEBUFFER_EXT, self._id)

    def unbind(self):
        """Set default framebuffer as current rendering target"""
        gl.glBindFramebufferEXT(gl.GL_FRAMEBUFFER_EXT, 0)

    def texture2d(self, texture):
        """Map currently bound framebuffer (not necessarily self) to texture"""
        gl.glFramebufferTexture2DEXT(gl.GL_FRAMEBUFFER_EXT, gl.GL_COLOR_ATTACHMENT0_EXT, texture.target, texture.id, texture.level)

    def check_status(self):
        """Check that currently set framebuffer is ready for rendering"""
        status = gl.glCheckFramebufferStatusEXT(gl.GL_FRAMEBUFFER_EXT)
        if status != gl.GL_FRAMEBUFFER_COMPLETE_EXT:
            raise Exception('Frambuffer not complete: %d' % status)

    def __del__(self):
        """Delete the framebuffer from the GPU memory"""
        id = gl.GLuint(self._id)
        gl.glDeleteFramebuffersEXT(1, ct.byref(id))