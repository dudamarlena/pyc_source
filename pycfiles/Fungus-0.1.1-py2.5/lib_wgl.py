# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/gl/lib_wgl.py
# Compiled at: 2009-02-18 19:37:25
"""
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: lib_glx.py 597 2007-02-03 16:13:07Z Alex.Holkner $'
import ctypes
from ctypes import *
import pyglet
from pyglet.gl.lib import missing_function, decorate_function
__all__ = [
 'link_GL', 'link_GLU', 'link_WGL']
_debug_trace = pyglet.options['debug_trace']
gl_lib = ctypes.windll.opengl32
glu_lib = ctypes.windll.glu32
wgl_lib = gl_lib
if _debug_trace:
    from pyglet.lib import _TraceLibrary
    gl_lib = _TraceLibrary(gl_lib)
    glu_lib = _TraceLibrary(glu_lib)
    wgl_lib = _TraceLibrary(wgl_lib)
try:
    wglGetProcAddress = wgl_lib.wglGetProcAddress
    wglGetProcAddress.restype = CFUNCTYPE(POINTER(c_int))
    wglGetProcAddress.argtypes = [c_char_p]
    _have_get_proc_address = True
except AttributeError:
    _have_get_proc_address = False

class WGLFunctionProxy(object):
    __slots__ = [
     'name', 'requires', 'suggestions', 'ftype', 'func']

    def __init__(self, name, ftype, requires, suggestions):
        assert _have_get_proc_address
        self.name = name
        self.ftype = ftype
        self.requires = requires
        self.suggestions = suggestions
        self.func = None
        return

    def __call__(self, *args, **kwargs):
        if self.func:
            return self.func(*args, **kwargs)
        from pyglet.gl import current_context
        if not current_context:
            raise Exception('Call to function "%s" before GL context created' % self.name)
        address = wglGetProcAddress(self.name)
        if cast(address, POINTER(c_int)):
            self.func = cast(address, self.ftype)
            decorate_function(self.func, self.name)
        else:
            self.func = missing_function(self.name, self.requires, self.suggestions)
        result = self.func(*args, **kwargs)
        return result


def link_GL(name, restype, argtypes, requires=None, suggestions=None):
    try:
        func = getattr(gl_lib, name)
        func.restype = restype
        func.argtypes = argtypes
        decorate_function(func, name)
        return func
    except AttributeError, e:
        try:
            fargs = (
             restype,) + tuple(argtypes)
            ftype = ctypes.WINFUNCTYPE(*fargs)
            if _have_get_proc_address:
                from pyglet.gl import gl_info
                if gl_info.have_context():
                    address = wglGetProcAddress(name)
                    if address:
                        func = cast(address, ftype)
                        decorate_function(func, name)
                        return func
                else:
                    return WGLFunctionProxy(name, ftype, requires, suggestions)
        except:
            pass
        else:
            return missing_function(name, requires, suggestions)


def link_GLU(name, restype, argtypes, requires=None, suggestions=None):
    try:
        func = getattr(glu_lib, name)
        func.restype = restype
        func.argtypes = argtypes
        decorate_function(func, name)
        return func
    except AttributeError, e:
        try:
            fargs = (
             restype,) + tuple(argtypes)
            ftype = ctypes.WINFUNCTYPE(*fargs)
            if _have_get_proc_address:
                from pyglet.gl import gl_info
                if gl_info.have_context():
                    address = wglGetProcAddress(name)
                    if address:
                        func = cast(address, ftype)
                        decorate_function(func, name)
                        return func
                else:
                    return WGLFunctionProxy(name, ftype, requires, suggestions)
        except:
            pass
        else:
            return missing_function(name, requires, suggestions)


link_WGL = link_GL