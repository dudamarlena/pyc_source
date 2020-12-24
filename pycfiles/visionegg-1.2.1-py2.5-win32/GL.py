# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\GL.py
# Compiled at: 2009-07-07 11:29:42
"""
Vision Egg GL module -- lump all OpenGL names in one namespace.

"""
from OpenGL.GL import *
import OpenGL, numpy
if OpenGL.__version__.startswith('3.0.0b'):
    raise RuntimeError('PyOpenGL 3beta has known incompatibilities with the Vision Egg. Please upgrade to PyOpenGL 3.')
__version__ = OpenGL.__version__
try:
    import OpenGL.GL.GL__init___
except:
    pass

try:
    import OpenGL.GL.ARB.multitexture
except:
    pass

try:
    import OpenGL.GL.EXT.bgra
except:
    pass

try:
    import SGIS.texture_edge_clamp
except:
    pass

try:
    GL_UNSIGNED_INT_8_8_8_8_REV
except NameError:
    GL_UNSIGNED_INT_8_8_8_8_REV = 33639

if OpenGL.__version__[0] == '3':
    if OpenGL.__version__.startswith('3.0.0a') or OpenGL.__version__ == '3.0.0b1':
        _orig_glLoadMatrixf = glLoadMatrixf

        def glLoadMatrixf(M):
            M = numpy.array([ Mi for Mi in M ])
            return _orig_glLoadMatrixf(M)