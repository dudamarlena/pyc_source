# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/visuals/linear_region.py
# Compiled at: 2016-11-03 01:40:19
import numpy as np
from .. import gloo
from .visual import Visual
VERT_SHADER = '\n    attribute vec2 a_pos;\n    varying vec4 v_color;\n\n    void main() {\n        vec4 pos = vec4(a_pos, 0, 1);\n\n        if($is_vertical==1)\n        {\n            pos.y = $render_to_visual(pos).y;\n        }\n        else\n        {\n            pos.x = $render_to_visual(pos).x;\n        }\n\n        gl_Position = $transform(pos);\n        gl_PointSize = 10;\n        v_color = $color;\n    }\n    '
FRAG_SHADER = '\n    varying vec4 v_color;\n\n    void main() {\n        gl_FragColor = v_color;\n    }\n    '

class LinearRegionVisual(Visual):
    """Infinite horizontal or vertical region for 2D plots.

    Parameters
    ----------
    pos : list, tuple or numpy array
        Bounds of the region along the axis. len(pos) must be >=2.
    color : list, tuple, or array
        The color to use when drawing the line. It must have a shape of
        (1, 4) for a single color region or (len(pos), 4) for a multicolor
        region.
    vertical:
        True for drawing a vertical region, False for an horizontal region
    """

    def __init__(self, pos=None, color=[1.0, 1.0, 1.0, 1.0], vertical=True, **kwargs):
        """

        """
        Visual.__init__(self, vcode=VERT_SHADER, fcode=FRAG_SHADER, **kwargs)
        self._changed = {'pos': False, 'color': False}
        self.pos_buf = gloo.VertexBuffer()
        self.color_buf = gloo.VertexBuffer()
        self.shared_program['a_pos'] = self.pos_buf
        self._program.vert['is_vertical'] = 1 if vertical else 0
        self._need_upload = False
        self._is_vertical = bool(vertical)
        self._pos = np.zeros((4, 2), dtype=np.float32)
        self._color = np.ones((1, 4), dtype=np.float32)
        self._draw_mode = 'triangle_strip'
        self.set_gl_state('translucent', depth_test=False)
        self.set_data(pos=pos, color=color)

    def set_data(self, pos=None, color=None):
        """Set the data

        Parameters
        ----------
        pos : list, tuple or numpy array
            Bounds of the region along the axis. len(pos) must be >=2.
        color : list, tuple, or array
            The color to use when drawing the line. It must have a shape of
            (1, 4) for a single color region or (len(pos), 4) for a multicolor
            region.
        """
        new_pos = self._pos
        new_color = self._color
        if pos is not None:
            num_elements = len(pos)
            pos = np.array(pos, dtype=np.float32)
            if pos.ndim != 1:
                raise ValueError('Expected 1D array')
            vertex = np.empty((num_elements * 2, 2), dtype=np.float32)
            if self._is_vertical:
                vertex[:, 0] = np.repeat(pos, 2)
                vertex[:, 1] = np.tile([-1, 1], num_elements)
            else:
                vertex[:, 1] = np.repeat(pos, 2)
                vertex[:, 0] = np.tile([1, -1], num_elements)
            new_pos = vertex
            self._changed['pos'] = True
        if color is not None:
            color = np.array(color, dtype=np.float32)
            num_elements = new_pos.shape[0] / 2
            if color.ndim == 2:
                if color.shape[0] != num_elements:
                    raise ValueError('Expected a color for each pos')
                if color.shape[1] != 4:
                    raise ValueError('Each color must be a RGBA array')
                color = np.repeat(color, 2, axis=0).astype(np.float32)
            elif color.ndim == 1:
                if color.shape[0] != 4:
                    raise ValueError('Each color must be a RGBA array')
                color = np.repeat([color], new_pos.shape[0], axis=0)
                color = color.astype(np.float32)
            else:
                raise ValueError('Expected a numpy array of shape (%d, 4) or (1, 4)' % num_elements)
            new_color = color
            self._changed['color'] = True
        if new_pos.shape[0] != new_color.shape[0]:
            raise ValueError('pos and color does must have the same size')
        self._color = new_color
        self._pos = new_pos
        return

    @property
    def color(self):
        return self._color[::2]

    @property
    def pos(self):
        if self._is_vertical:
            return self._pos[:, 0].ravel()[::2]
        else:
            return self._pos[:, 1].ravel()[::2]

    def _compute_bounds(self, axis, view):
        """Return the (min, max) bounding values of this visual along *axis*
        in the local coordinate system.
        """
        is_vertical = self._is_vertical
        pos = self._pos
        if axis == 0 and is_vertical:
            return (pos[(0, 0)], pos[(-1, 0)])
        else:
            if axis == 1 and not is_vertical:
                return (pos[(0, 1)], pos[(-1, 1)])
            return

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
            self.color_buf.set_data(self._color)
            self._program.vert['color'] = self.color_buf
            self._changed['color'] = False
        return True