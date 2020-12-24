# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/gl/glxext_mesa.py
# Compiled at: 2009-02-07 06:48:49
"""This file is currently hand-coded; I don't have a MESA header file to build
off.
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: glxext_mesa.py 1579 2008-01-15 14:47:19Z Alex.Holkner $'
import ctypes
from ctypes import *
from pyglet.gl.lib import link_GLX as _link_function
glXSwapIntervalMESA = _link_function('glXSwapIntervalMESA', c_int, [c_int], 'MESA_swap_control')