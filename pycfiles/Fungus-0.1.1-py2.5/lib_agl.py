# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/gl/lib_agl.py
# Compiled at: 2009-02-07 06:48:49
"""
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: $'
from ctypes import *
import pyglet.lib
from pyglet.gl.lib import missing_function, decorate_function
__all__ = [
 'link_GL', 'link_GLU', 'link_AGL']
gl_lib = pyglet.lib.load_library(framework='/System/Library/Frameworks/OpenGL.framework')
agl_lib = pyglet.lib.load_library(framework='/System/Library/Frameworks/AGL.framework')

def link_GL(name, restype, argtypes, requires=None, suggestions=None):
    try:
        func = getattr(gl_lib, name)
        func.restype = restype
        func.argtypes = argtypes
        decorate_function(func, name)
        return func
    except AttributeError, e:
        return missing_function(name, requires, suggestions)


link_GLU = link_GL

def link_AGL(name, restype, argtypes, requires=None, suggestions=None):
    try:
        func = getattr(agl_lib, name)
        func.restype = restype
        func.argtypes = argtypes
        decorate_function(func, name)
        return func
    except AttributeError, e:
        return missing_function(name, requires, suggestions)