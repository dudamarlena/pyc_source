# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/gl/lib_glx.py
# Compiled at: 2009-02-07 06:48:49
"""
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: lib_glx.py 1579 2008-01-15 14:47:19Z Alex.Holkner $'
from ctypes import *
import pyglet.lib
from pyglet.gl.lib import missing_function, decorate_function
__all__ = [
 'link_GL', 'link_GLU', 'link_GLX']
gl_lib = pyglet.lib.load_library('GL')
glu_lib = pyglet.lib.load_library('GLU')
try:
    glXGetProcAddressARB = getattr(gl_lib, 'glXGetProcAddressARB')
    glXGetProcAddressARB.restype = POINTER(CFUNCTYPE(None))
    glXGetProcAddressARB.argtypes = [POINTER(c_ubyte)]
    _have_getprocaddress = True
except AttributeError:
    _have_get_procaddress = False

def link_GL(name, restype, argtypes, requires=None, suggestions=None):
    try:
        func = getattr(gl_lib, name)
        func.restype = restype
        func.argtypes = argtypes
        decorate_function(func, name)
        return func
    except AttributeError, e:
        if _have_getprocaddress:
            bname = cast(pointer(create_string_buffer(name)), POINTER(c_ubyte))
            addr = glXGetProcAddressARB(bname)
            if addr:
                ftype = CFUNCTYPE(*((restype,) + tuple(argtypes)))
                func = cast(addr, ftype)
                decorate_function(func, name)
                return func

    return missing_function(name, requires, suggestions)


link_GLX = link_GL

def link_GLU(name, restype, argtypes, requires=None, suggestions=None):
    try:
        func = getattr(glu_lib, name)
        func.restype = restype
        func.argtypes = argtypes
        decorate_function(func, name)
        return func
    except AttributeError, e:
        return missing_function(name, requires, suggestions)