# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/gl/glext_missing.py
# Compiled at: 2009-02-07 06:48:48
"""Additional hand-coded GL extensions.

These are hand-wrapped extension tokens and functions that are in
the OpenGL Extension Registry but have not yet been added to either 
the registry's glext.h or nVidia's glext.h.  Remove wraps from here
when the headers are updated (and glext_arb.py or glext_nv.py are
regenerated).

When adding an extension here, include the name and URL, and any tokens and
functions appearing under "New Tokens" and "New Procedures" headings.  Don't
forget to add the GL_/gl prefix.

Unnumbered extensions in the registry are not included.
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: glext_missing.py 1579 2008-01-15 14:47:19Z Alex.Holkner $'
from ctypes import *
from pyglet.gl.lib import link_GL as _link_function
from pyglet.gl.lib import c_ptrdiff_t
GL_DEPTH_STENCIL_EXT = 34041
GL_UNSIGNED_INT_24_8_EXT = 34042
GL_DEPTH24_STENCIL8_EXT = 35056
GL_TEXTURE_STENCIL_SIZE_EXT = 35057
GL_SRGB_EXT = 35904
GL_SRGB8_EXT = 35905
GL_SRGB_ALPHA_EXT = 35906
GL_SRGB8_ALPHA8_EXT = 35907
GL_SLUMINANCE_ALPHA_EXT = 35908
GL_SLUMINANCE8_ALPHA8_EXT = 35909
GL_SLUMINANCE_EXT = 35910
GL_SLUMINANCE8_EXT = 35911
GL_COMPRESSED_SRGB_EXT = 35912
GL_COMPRESSED_SRGB_ALPHA_EXT = 35913
GL_COMPRESSED_SLUMINANCE_EXT = 35914
GL_COMPRESSED_SLUMINANCE_ALPHA_EXT = 35915
GL_COMPRESSED_SRGB_S3TC_DXT1_EXT = 35916
GL_COMPRESSED_SRGB_ALPHA_S3TC_DXT1_EXT = 35917
GL_COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT = 35918
GL_COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT = 35919
GLuint = c_uint
GLsizei = c_int
glStencilClearTagEXT = _link_function('glStencilClearTagEXT', None, [GLsizei, GLuint])
GL_STENCIL_TAG_BITS_EXT = 35058
GL_STENCIL_CLEAR_TAG_VALUE_EXT = 35059
GLenum = c_uint
GLint = c_int
glBlitFramebufferEXT = _link_function('glBlitFramebufferEXT', None, [GLint, GLint, GLint, GLint,
 GLint, GLint, GLint, GLint,
 GLuint, GLenum])
GL_READ_FRAMEBUFFER_EXT = 36008
GL_DRAW_FRAMEBUFFER_EXT = 36009
GL_DRAW_FRAMEBUFFER_BINDING_EXT = 36006
GL_READ_FRAMEBUFFER_BINDING_EXT = 36010
GL_RENDERBUFFER_SAMPLES_EXT = 36011
GL_TEXTURE_1D_STACK_MESAX = 34649
GL_TEXTURE_2D_STACK_MESAX = 34650
GL_PROXY_TEXTURE_1D_STACK_MESAX = 34651
GL_PROXY_TEXTURE_2D_STACK_MESAX = 34652
GL_TEXTURE_1D_STACK_BINDING_MESAX = 34653
GL_TEXTURE_2D_STACK_BINDING_MESAX = 34654