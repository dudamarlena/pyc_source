# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/window/xlib/xinerama.py
# Compiled at: 2009-02-07 06:48:50
"""Wrapper for Xinerama

Generated with:
tools/genwrappers.py

Do not modify this file.
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: xinerama.py 1579 2008-01-15 14:47:19Z Alex.Holkner $'
import ctypes
from ctypes import *
import pyglet.lib
_lib = pyglet.lib.load_library('Xinerama')
_int_types = (
 c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    _int_types += (ctypes.c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t

class c_void(Structure):
    _fields_ = [
     (
      'dummy', c_int)]


import pyglet.gl.glx, pyglet.window.xlib.xlib

class struct_anon_181(Structure):
    __slots__ = [
     'screen_number',
     'x_org',
     'y_org',
     'width',
     'height']


struct_anon_181._fields_ = [
 (
  'screen_number', c_int),
 (
  'x_org', c_short),
 (
  'y_org', c_short),
 (
  'width', c_short),
 (
  'height', c_short)]
XineramaScreenInfo = struct_anon_181
Display = pyglet.gl.glx.Display
XineramaQueryExtension = _lib.XineramaQueryExtension
XineramaQueryExtension.restype = c_int
XineramaQueryExtension.argtypes = [POINTER(Display), POINTER(c_int), POINTER(c_int)]
XineramaQueryVersion = _lib.XineramaQueryVersion
XineramaQueryVersion.restype = c_int
XineramaQueryVersion.argtypes = [POINTER(Display), POINTER(c_int), POINTER(c_int)]
XineramaIsActive = _lib.XineramaIsActive
XineramaIsActive.restype = c_int
XineramaIsActive.argtypes = [POINTER(Display)]
XineramaQueryScreens = _lib.XineramaQueryScreens
XineramaQueryScreens.restype = POINTER(XineramaScreenInfo)
XineramaQueryScreens.argtypes = [POINTER(Display), POINTER(c_int)]
__all__ = [
 'XineramaScreenInfo', 'XineramaQueryExtension',
 'XineramaQueryVersion', 'XineramaIsActive', 'XineramaQueryScreens']