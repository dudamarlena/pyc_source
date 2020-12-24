# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../..\cocos\framegrabber.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 6738 bytes
"""Utility classes for rendering to a texture.

It is mostly used for internal implementation of cocos, you normally shouldn't
need it. If you are curious, check implementation of effects to see an example.
"""
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
from pyglet import gl
from pyglet import image
import pyglet
from cocos.gl_framebuffer_object import FramebufferObject
import cocos.director as director
_best_grabber = None
__all__ = [
 'TextureGrabber']

def TextureGrabber--- This code section failed: ---

 L.  65         0  LOAD_GLOBAL              _best_grabber
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.  66         8  LOAD_GLOBAL              _best_grabber
               10  CALL_FUNCTION_0       0  ''
               12  RETURN_VALUE     
             14_0  COME_FROM             6  '6'

 L.  68        14  SETUP_FINALLY        28  'to 28'

 L.  71        16  LOAD_GLOBAL              FBOGrabber
               18  STORE_GLOBAL             _best_grabber

 L.  72        20  LOAD_GLOBAL              _best_grabber
               22  CALL_FUNCTION_0       0  ''
               24  POP_BLOCK        
               26  RETURN_VALUE     
             28_0  COME_FROM_FINALLY    14  '14'

 L.  73        28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.  74        34  LOAD_CONST               0
               36  LOAD_CONST               None
               38  IMPORT_NAME              traceback
               40  STORE_FAST               'traceback'

 L.  75        42  LOAD_FAST                'traceback'
               44  LOAD_METHOD              print_exc
               46  CALL_METHOD_0         0  ''
               48  POP_TOP          
               50  POP_EXCEPT       
               52  JUMP_FORWARD         56  'to 56'
               54  END_FINALLY      
             56_0  COME_FROM            52  '52'

 L.  77        56  LOAD_GLOBAL              Exception
               58  LOAD_STR                 "ERROR: GPU doesn't support Frame Buffers Objects. Can't continue"
               60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `IMPORT_NAME' instruction at offset 38


class _TextureGrabber(object):

    def __init__(self):
        """Create a texture grabber."""
        pass

    def grab(self, texture):
        """Capture the current screen."""
        pass

    def before_render(self, texture):
        """Setup call before rendering begins."""
        pass

    def after_render(self, texture):
        """Rendering done, make sure texture holds what has been rendered."""
        pass


class GenericGrabber(_TextureGrabber):
    __doc__ = 'A simple render-to-texture mechanism. Destroys the current GL display;\n    and considers the whole layer as opaque. But it works in any GL\n    implementation.'

    def __init__(self):
        self.before = None
        x1 = y1 = 0
        x2, y2 = director.get_window_size
        self.vertex_list = pyglet.graphics.vertex_list(4, (
         'v2f', [x1, y1, x2, y1, x2, y2, x1, y2]), (
         'c4B', [255, 255, 255, 255] * 4))

    def before_render(self, texture):
        director.window.clear

    def after_render(self, texture):
        buffer = image.get_buffer_manager.get_color_buffer
        texture.blit_into(buffer, 0, 0, 0)
        director.window.clear


class PbufferGrabber(_TextureGrabber):
    __doc__ = 'A render-to texture mechanism using pbuffers.\n    Requires pbuffer extensions. Currently only implemented in GLX.\n\n    Not working yet, very untested\n\n    TODO: finish pbuffer grabber\n    '

    def grab(self, texture):
        self.pbuf = gl.Pbuffer(director.window, [
         gl.GLX_CONFIG_CAVEAT, gl.GLX_NONE,
         gl.GLX_RED_SIZE, 8,
         gl.GLX_GREEN_SIZE, 8,
         gl.GLX_BLUE_SIZE, 8,
         gl.GLX_DEPTH_SIZE, 24,
         gl.GLX_DOUBLEBUFFER, 1])

    def before_render(self, texture):
        self.pbuf.switch_to
        gl.glViewport(0, 0, self.pbuf.width, self.pbuf.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity
        gl.glOrtho(0, self.pbuf.width, 0, self.pbuf.height, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glEnable(gl.GL_TEXTURE_2D)

    def after_render(self, texture):
        buffer = image.get_buffer_manager.get_color_buffer
        texture.blit_into(buffer, 0, 0, 0)
        director.window.switch_to


class FBOGrabber(_TextureGrabber):
    __doc__ = 'Render-to texture system based on framebuffer objects (the GL\n    extension). It is quite fast and portable, but requires a recent GL\n    implementation/driver.\n\n    Requires framebuffer_object extensions'

    def __init__(self):
        self.fbuf = FramebufferObject
        self.fbuf.check_status

    def grab(self, texture):
        self.fbuf.bind
        self.fbuf.texture2d(texture)
        self.fbuf.check_status
        self.fbuf.unbind

    def before_render(self, texture):
        self.fbuf.bind
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    def after_render(self, texture):
        self.fbuf.unbind


# global _best_grabber ## Warning: Unused global