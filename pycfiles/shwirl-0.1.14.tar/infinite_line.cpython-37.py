# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/visuals/infinite_line.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 5103 bytes
import numpy as np
from .. import gloo
from .visual import Visual
VERT_SHADER = '\n    attribute vec2 a_pos;\n    varying vec4 v_color;\n\n    void main() {\n        vec4 pos = vec4(a_pos, 0, 1);\n\n        if($is_vertical==1)\n        {\n            pos.y = $render_to_visual(pos).y;\n        }\n        else\n        {\n            pos.x = $render_to_visual(pos).x;\n        }\n\n        gl_Position = $transform(pos);\n        gl_PointSize = 10;\n        v_color = $color;\n    }\n    '
FRAG_SHADER = '\n    varying vec4 v_color;\n\n    void main() {\n        gl_FragColor = v_color;\n    }\n    '

class InfiniteLineVisual(Visual):
    __doc__ = 'Infinite horizontal or vertical line for 2D plots.\n\n    Parameters\n    ----------\n    pos : float\n        Position of the line along the axis.\n    color : list, tuple, or array\n        The color to use when drawing the line. If an array is given, it\n        must be of shape (1, 4) and provide one rgba color per vertex.\n    vertical:\n        True for drawing a vertical line, False for an horizontal line\n    '

    def __init__(self, pos=None, color=(1.0, 1.0, 1.0, 1.0), vertical=True, **kwargs):
        """

        """
        (Visual.__init__)(self, vcode=VERT_SHADER, fcode=FRAG_SHADER, **kwargs)
        self._changed = {'pos':False, 
         'color':False}
        self.pos_buf = gloo.VertexBuffer()
        self.shared_program['a_pos'] = self.pos_buf
        self._program.vert['is_vertical'] = 1 if vertical else 0
        self._need_upload = False
        self._is_vertical = bool(vertical)
        self._pos = np.zeros((2, 2), dtype=(np.float32))
        self._color = np.ones(4, dtype=(np.float32))
        self._draw_mode = 'line_strip'
        self.set_gl_state('translucent', depth_test=False)
        self.set_data(pos=pos, color=color)

    def set_data(self, pos=None, color=None):
        """Set the data

        Parameters
        ----------
        pos : float
            Position of the line along the axis.
        color : list, tuple, or array
            The color to use when drawing the line. If an array is given, it
            must be of shape (1, 4) and provide one rgba color per vertex.
        """
        if pos is not None:
            pos = float(pos)
            xy = self._pos
            if self._is_vertical:
                xy[(0, 0)] = pos
                xy[(0, 1)] = -1
                xy[(1, 0)] = pos
                xy[(1, 1)] = 1
            else:
                xy[(0, 0)] = -1
                xy[(0, 1)] = pos
                xy[(1, 0)] = 1
                xy[(1, 1)] = pos
            self._changed['pos'] = True
        if color is not None:
            color = np.array(color, dtype=(np.float32))
            if color.ndim != 1 or color.shape[0] != 4:
                raise ValueError('color must be a 4 element float rgba tuple, list or array')
            self._color = color
            self._changed['color'] = True

    @property
    def color(self):
        return self._color

    @property
    def pos(self):
        if self._is_vertical:
            return self._pos[(0, 0)]
        return self._pos[(0, 1)]

    def _compute_bounds(self, axis, view):
        """Return the (min, max) bounding values of this visual along *axis*
        in the local coordinate system.
        """
        is_vertical = self._is_vertical
        pos = self._pos
        if axis == 0:
            if is_vertical:
                return (
                 pos[(0, 0)], pos[(0, 0)])
        if axis == 1:
            if not is_vertical:
                return (
                 self._pos[(0, 1)], self._pos[(0, 1)])

    @property
    def is_vertical(self):
        return self._is_vertical

    def _prepare_transforms(self, view=None):
        program = view.view_program
        transforms = view.transforms
        program.vert['render_to_visual'] = transforms.get_transform('render', 'visual')
        program.vert['transform'] = transforms.get_transform('visual', 'render')

    def _prepare_draw(self, view=None):
        """This method is called immediately before each draw.

        The *view* argument indicates which view is about to be drawn.
        """
        if self._changed['pos']:
            self.pos_buf.set_data(self._pos)
            self._changed['pos'] = False
        if self._changed['color']:
            self._program.vert['color'] = self._color
            self._changed['color'] = False