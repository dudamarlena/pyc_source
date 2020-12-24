# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/gl/wgl_info.py
# Compiled at: 2009-02-07 06:48:49
"""Cached information about version and extensions of current WGL
implementation.
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: glx_info.py 615 2007-02-07 13:17:05Z Alex.Holkner $'
from ctypes import *
import warnings
from pyglet.gl.lib import MissingFunctionException
from pyglet.gl.gl import *
from pyglet.gl import gl_info
from pyglet.gl.wgl import *
from pyglet.gl.wglext_arb import *

class WGLInfoException(Exception):
    pass


class WGLInfo(object):

    def get_extensions(self):
        if not gl_info.have_context():
            warnings.warn("Can't query WGL until a context is created.")
            return []
        try:
            return wglGetExtensionsStringEXT().split()
        except MissingFunctionException:
            return cast(glGetString(GL_EXTENSIONS), c_char_p).value.split()

    def have_extension(self, extension):
        return extension in self.get_extensions()


_wgl_info = WGLInfo()
get_extensions = _wgl_info.get_extensions
have_extension = _wgl_info.have_extension