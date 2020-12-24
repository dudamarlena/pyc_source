# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ../..\cocos\layer\util_layers.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 5696 bytes
__doc__ = 'Special purpose layers\n'
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import pyglet
from pyglet import gl
from cocos.director import *
from .base_layers import Layer
__all__ = [
 'ColorLayer']

class ColorLayer(Layer):
    """ColorLayer"""

    def __init__(self, r, g, b, a, width=None, height=None):
        super(ColorLayer, self).__init__()
        self._batch = pyglet.graphics.Batch()
        self._vertex_list = None
        self._rgb = (r, g, b)
        self._opacity = a
        self.width = width
        self.height = height
        w, h = director.get_window_size()
        if not self.width:
            self.width = w
        if not self.height:
            self.height = h

    def on_enter(self):
        super(ColorLayer, self).on_enter()
        x, y = self.width, self.height
        ox, oy = (0, 0)
        self._vertex_list = self._batch.add(4, pyglet.gl.GL_QUADS, None, (
         'v2i',
         (ox, oy,
          ox, oy + y,
          ox + x, oy + y,
          ox + x, oy)), 'c4B')
        self._update_color()

    def on_exit(self):
        super(ColorLayer, self).on_exit()
        self._vertex_list.delete()
        self._vertex_list = None

    def draw(self):
        super(ColorLayer, self).draw()
        gl.glPushMatrix()
        self.transform()
        gl.glPushAttrib(gl.GL_CURRENT_BIT)
        self._batch.draw()
        gl.glPopAttrib()
        gl.glPopMatrix()

    def _update_color(self):
        if self._vertex_list:
            r, g, b = self._rgb
            self._vertex_list.colors[:] = [r, g, b, int(self._opacity)] * 4

    def _set_opacity(self, opacity):
        self._opacity = opacity
        self._update_color()

    opacity = property((lambda self: self._opacity), _set_opacity, doc="Blend opacity.\n\n    This property sets the alpha component of the colour of the layer's\n    vertices.  This allows the layer to be drawn with fractional opacity,\n    blending with the background.\n\n    An opacity of 255 (the default) has no effect.  An opacity of 128 will\n    make the ColorLayer appear translucent.\n\n    Arguments:\n        opacity (int): the opacity ranging from 0 (transparent) to 255 (opaque).\n    ")

    def _set_color(self, rgb):
        self._rgb = tuple(map(int, rgb))
        self._update_color()

    color = property((lambda self: self._rgb), _set_color, doc="Blend color.\n\n    This property sets the color of the layer's vertices. This allows the\n    layer to be drawn with a color tint.\n\n    \n\n    Arguments:\n        color (tuple[int, int, int]): The color is specified as an RGB tuple\n            of integers ``(red, green, blue)``.\n            Each color component must be in the range 0 (dark) to 255 (saturated).\n    ")