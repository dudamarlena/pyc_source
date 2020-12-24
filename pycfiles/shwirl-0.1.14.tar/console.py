# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/scene/widgets/console.py
# Compiled at: 2016-11-03 01:40:19
""" Fast and failsafe GL console """
import numpy as np
from .widget import Widget
from ...visuals import Visual
from ...gloo import VertexBuffer
from ...color import Color
from ...ext.six import string_types
__font_6x8__ = np.array([
 (0, 0, 0, 0, 0, 0), (16, 227, 132, 16, 1, 0),
 (109, 180, 128, 0, 0, 0), (0, 167, 202, 41, 242, 128),
 (32, 228, 12, 9, 193, 0), (101, 144, 132, 33, 52, 192),
 (33, 69, 8, 85, 35, 64), (48, 194, 0, 0, 0, 0),
 (16, 130, 8, 32, 129, 0), (32, 65, 4, 16, 66, 0),
 (0, 163, 159, 56, 160, 0), (0, 65, 31, 16, 64, 0),
 (0, 0, 0, 0, 195, 8), (0, 0, 31, 0, 0, 0),
 (0, 0, 0, 0, 195, 0), (0, 16, 132, 33, 0, 0),
 (57, 20, 213, 101, 19, 128), (16, 193, 4, 16, 67, 128),
 (57, 16, 70, 33, 7, 192), (57, 16, 78, 5, 19, 128),
 (8, 98, 146, 124, 32, 128), (125, 4, 30, 5, 19, 128),
 (24, 132, 30, 69, 19, 128), (124, 16, 132, 32, 130, 0),
 (57, 20, 78, 69, 19, 128), (57, 20, 79, 4, 35, 0),
 (0, 3, 12, 0, 195, 0), (0, 3, 12, 0, 195, 8),
 (8, 66, 16, 32, 64, 128), (0, 7, 192, 1, 240, 0),
 (32, 64, 129, 8, 66, 0), (57, 16, 70, 16, 1, 0),
 (57, 21, 213, 93, 3, 128), (57, 20, 81, 125, 20, 64),
 (121, 20, 94, 69, 23, 128), (57, 20, 16, 65, 19, 128),
 (121, 20, 81, 69, 23, 128), (125, 4, 30, 65, 7, 192),
 (125, 4, 30, 65, 4, 0), (57, 20, 23, 69, 19, 192),
 (69, 20, 95, 69, 20, 64), (56, 65, 4, 16, 67, 128),
 (4, 16, 65, 69, 19, 128), (69, 37, 24, 81, 36, 64),
 (65, 4, 16, 65, 7, 192), (69, 181, 81, 69, 20, 64),
 (69, 149, 83, 69, 20, 64), (57, 20, 81, 69, 19, 128),
 (121, 20, 94, 65, 4, 0), (57, 20, 81, 85, 35, 64),
 (121, 20, 94, 73, 20, 64), (57, 20, 14, 5, 19, 128),
 (124, 65, 4, 16, 65, 0), (69, 20, 81, 69, 19, 128),
 (69, 20, 81, 68, 161, 0), (69, 21, 85, 85, 82, 128),
 (69, 18, 132, 41, 20, 64), (69, 20, 74, 16, 65, 0),
 (120, 33, 8, 65, 7, 128), (56, 130, 8, 32, 131, 128),
 (1, 2, 4, 8, 16, 0), (56, 32, 130, 8, 35, 128),
 (16, 164, 64, 0, 0, 0), (0, 0, 0, 0, 0, 63),
 (48, 193, 0, 0, 0, 0), (0, 3, 129, 61, 19, 192),
 (65, 7, 145, 69, 23, 128), (0, 3, 145, 65, 19, 128),
 (4, 19, 209, 69, 19, 192), (0, 3, 145, 121, 3, 128),
 (24, 130, 30, 32, 130, 0), (0, 3, 209, 68, 240, 78),
 (65, 7, 18, 73, 36, 128), (16, 1, 4, 16, 65, 128),
 (8, 1, 130, 8, 36, 140), (65, 4, 148, 97, 68, 128),
 (16, 65, 4, 16, 65, 128), (0, 6, 149, 85, 20, 64),
 (0, 7, 18, 73, 36, 128), (0, 3, 145, 69, 19, 128),
 (0, 7, 145, 69, 23, 144), (0, 3, 209, 69, 19, 193),
 (0, 5, 137, 32, 135, 0), (0, 3, 144, 56, 19, 128),
 (0, 135, 136, 32, 161, 0), (0, 4, 146, 73, 98, 128),
 (0, 4, 81, 68, 161, 0), (0, 4, 81, 85, 242, 128),
 (0, 4, 146, 49, 36, 128), (0, 4, 146, 72, 225, 24),
 (0, 7, 130, 49, 7, 128), (24, 130, 24, 32, 129, 128),
 (16, 65, 0, 16, 65, 0), (48, 32, 131, 8, 35, 0),
 (41, 64, 0, 0, 0, 0), (16, 230, 209, 69, 240, 0)], dtype=np.float32)
VERTEX_SHADER = '\nuniform vec2 u_logical_scale;\nuniform float u_physical_scale;\nuniform vec4 u_color;\nuniform vec4 u_origin; \n\nattribute vec2 a_position;\nattribute vec3 a_bytes_012;\nattribute vec3 a_bytes_345;\n\nvarying vec4 v_color;\nvarying vec3 v_bytes_012, v_bytes_345;\n\nvoid main (void)\n{\n    gl_Position = u_origin + vec4(a_position * u_logical_scale, 0., 0.);\n    gl_PointSize = 8.0 * u_physical_scale;\n    v_color = u_color;\n    v_bytes_012 = a_bytes_012;\n    v_bytes_345 = a_bytes_345;\n}\n'
FRAGMENT_SHADER = '\nfloat segment(float edge0, float edge1, float x)\n{\n    return step(edge0,x) * (1.0-step(edge1,x));\n}\n\nvarying vec4 v_color;\nvarying vec3 v_bytes_012, v_bytes_345;\n\nvec4 glyph_color(vec2 uv) {\n    if(uv.x > 5.0 || uv.y > 7.0)\n        return vec4(0, 0, 0, 0);\n    else {\n        float index  = floor( (uv.y*6.0+uv.x)/8.0 );\n        float offset = floor( mod(uv.y*6.0+uv.x,8.0));\n        float byte = segment(0.0,1.0,index) * v_bytes_012.x\n                   + segment(1.0,2.0,index) * v_bytes_012.y\n                   + segment(2.0,3.0,index) * v_bytes_012.z\n                   + segment(3.0,4.0,index) * v_bytes_345.x\n                   + segment(4.0,5.0,index) * v_bytes_345.y\n                   + segment(5.0,6.0,index) * v_bytes_345.z;\n        if( floor(mod(byte / (128.0/pow(2.0,offset)), 2.0)) > 0.0 )\n            return v_color;\n        else\n            return vec4(0, 0, 0, 0);\n    }\n}\n\nvoid main(void)\n{\n    vec2 loc = gl_PointCoord.xy * 8.0;\n    vec2 uv = floor(loc);\n    // use multi-sampling to make the text look nicer\n    vec2 dxy = 0.25*(abs(dFdx(loc)) + abs(dFdy(loc)));\n    vec4 box = floor(vec4(loc-dxy, loc+dxy));\n    vec4 color = glyph_color(floor(loc)) +\n                 0.25 * glyph_color(box.xy) +\n                 0.25 * glyph_color(box.xw) +\n                 0.25 * glyph_color(box.zy) +\n                 0.25 * glyph_color(box.zw);\n    gl_FragColor = color / 2.;\n}\n'

class Console(Widget):
    """Fast and failsafe text console

    Parameters
    ----------
    text_color : instance of Color
        Color to use.
    font_size : float
        Point size to use.
    """

    def __init__(self, text_color='black', font_size=12.0, **kwargs):
        self._visual = ConsoleVisual(text_color, font_size)
        Widget.__init__(self, **kwargs)
        self.add_subvisual(self._visual)

    def on_resize(self, event):
        """Resize event handler

        Parameters
        ----------
        event : instance of Event
            The event.
        """
        self._visual.size = self.size

    def clear(self):
        """Clear the console"""
        self._visual.clear()

    def write(self, text='', wrap=True):
        """Write text and scroll

        Parameters
        ----------
        text : str
            Text to write. ``''`` can be used for a blank line, as a newline
            is automatically added to the end of each line.
        wrap : str
            If True, long messages will be wrapped to span multiple lines.
        """
        self._visual.write(text)

    @property
    def text_color(self):
        """The color of the text"""
        return self._visual._text_color

    @text_color.setter
    def text_color(self, color):
        self._visual._text_color = Color(color)

    @property
    def font_size(self):
        """The font size (in points) of the text"""
        return self._visual._font_size

    @font_size.setter
    def font_size(self, font_size):
        self._visual._font_size = float(font_size)


class ConsoleVisual(Visual):

    def __init__(self, text_color, font_size, **kwargs):
        self.text_color = text_color
        self.font_size = font_size
        self._char_width = 6
        self._char_height = 10
        self._pending_writes = []
        self._text_lines = []
        self._col = 0
        self._current_sizes = (-1, -1, -1)
        self._size = (100, 100)
        Visual.__init__(self, VERTEX_SHADER, FRAGMENT_SHADER)
        self._draw_mode = 'points'
        self.set_gl_state(depth_test=False, blend=True, blend_func=('src_alpha', 'one_minus_src_alpha'))

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, s):
        self._size = s

    @property
    def text_color(self):
        """The color of the text"""
        return self._text_color

    @text_color.setter
    def text_color(self, color):
        self._text_color = Color(color)

    @property
    def font_size(self):
        """The font size (in points) of the text"""
        return self._font_size

    @font_size.setter
    def font_size(self, font_size):
        self._font_size = float(font_size)

    def _resize_buffers(self, font_scale):
        """Resize buffers only if necessary"""
        new_sizes = (
         font_scale,) + self.size
        if new_sizes == self._current_sizes:
            return
        self._n_rows = int(max(self.size[1] / (self._char_height * font_scale), 1))
        self._n_cols = int(max(self.size[0] / (self._char_width * font_scale), 1))
        self._bytes_012 = np.zeros((self._n_rows, self._n_cols, 3), np.float32)
        self._bytes_345 = np.zeros((self._n_rows, self._n_cols, 3), np.float32)
        pos = np.empty((self._n_rows, self._n_cols, 2), np.float32)
        C, R = np.meshgrid(np.arange(self._n_cols), np.arange(self._n_rows))
        x_off = 4.0
        y_off = 4 - self.size[1] / font_scale
        pos[(Ellipsis, 0)] = x_off + self._char_width * C
        pos[(Ellipsis, 1)] = y_off + self._char_height * R
        self._position = VertexBuffer(pos)
        for ii, line in enumerate(self._text_lines[:self._n_rows]):
            self._insert_text_buf(line, ii)

        self._current_sizes = new_sizes

    def _prepare_draw(self, view):
        xform = view.get_transform()
        tr = view.get_transform('document', 'render')
        logical_scale = np.diff(tr.map(([0, 1], [1, 0])), axis=0)[0, :2]
        tr = view.get_transform('document', 'framebuffer')
        log_to_phy = np.mean(np.diff(tr.map(([0, 1], [1, 0])), axis=0)[0, :2])
        n_pix = self.font_size / 72.0 * 92.0
        font_scale = max(n_pix / float(self._char_height - 2), 1)
        self._resize_buffers(font_scale)
        self._do_pending_writes()
        self._program['u_origin'] = xform.map((0, 0, 0, 1))
        self._program['u_logical_scale'] = font_scale * logical_scale
        self._program['u_color'] = self.text_color.rgba
        self._program['u_physical_scale'] = font_scale * log_to_phy
        self._program['a_position'] = self._position
        self._program['a_bytes_012'] = VertexBuffer(self._bytes_012)
        self._program['a_bytes_345'] = VertexBuffer(self._bytes_345)

    def _prepare_transforms(self, view):
        pass

    def clear(self):
        """Clear the console"""
        if hasattr(self, '_bytes_012'):
            self._bytes_012.fill(0)
            self._bytes_345.fill(0)
        self._text_lines = [] * self._n_rows
        self._pending_writes = []

    def write(self, text='', wrap=True):
        """Write text and scroll

        Parameters
        ----------
        text : str
            Text to write. ``''`` can be used for a blank line, as a newline
            is automatically added to the end of each line.
        wrap : str
            If True, long messages will be wrapped to span multiple lines.
        """
        if not isinstance(text, string_types):
            raise TypeError('text must be a string')
        text = text.encode('utf-8').decode('ascii', errors='replace')
        self._pending_writes.append((text, wrap))
        self.update()

    def _do_pending_writes(self):
        """Do any pending text writes"""
        for text, wrap in self._pending_writes:
            text = text[-self._n_cols * self._n_rows:]
            text = text.split('\n')
            text = [ t if len(t) > 0 else '' for t in text ]
            nr, nc = self._n_rows, self._n_cols
            for para in text:
                para = (wrap or para)[:nc] if 1 else para
                lines = [ para[ii:ii + nc] for ii in range(0, len(para), nc) ]
                lines = [''] if len(lines) == 0 else lines
                for line in lines:
                    self._text_lines.insert(0, line)
                    self._text_lines = self._text_lines[:nr]
                    self._bytes_012[1:] = self._bytes_012[:-1]
                    self._bytes_345[1:] = self._bytes_345[:-1]
                    self._insert_text_buf(line, 0)

        self._pending_writes = []

    def _insert_text_buf(self, line, idx):
        """Insert text into bytes buffers"""
        self._bytes_012[idx] = 0
        self._bytes_345[idx] = 0
        I = np.array([ ord(c) - 32 for c in line[:self._n_cols] ])
        I = np.clip(I, 0, len(__font_6x8__) - 1)
        if len(I) > 0:
            b = __font_6x8__[I]
            self._bytes_012[idx, :len(I)] = b[:, :3]
            self._bytes_345[idx, :len(I)] = b[:, 3:]