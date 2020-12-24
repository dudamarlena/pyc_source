# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/visuals/isoline.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 8458 bytes
from __future__ import division
import numpy as np
from .line import LineVisual
from ..color import ColorArray
from color.colormap import _normalize, get_colormap

def iso_mesh_line(vertices, tris, vertex_data, levels):
    """Generate an isocurve from vertex data in a surface mesh.

    Parameters
    ----------
    vertices : ndarray, shape (Nv, 3)
        Vertex coordinates.
    tris : ndarray, shape (Nf, 3)
        Indices of triangular element into the vertices array.
    vertex_data : ndarray, shape (Nv,)
        data at vertex.
    levels : ndarray, shape (Nl,)
        Levels at which to generate an isocurve

    Returns
    -------
    lines : ndarray, shape (Nvout, 3)
        Vertex coordinates for lines points
    connects : ndarray, shape (Ne, 2)
        Indices of line element into the vertex array.
    vertex_level: ndarray, shape (Nvout,)
        level for vertex in lines

    Notes
    -----
    Uses a marching squares algorithm to generate the isolines.
    """
    lines = None
    connects = None
    vertex_level = None
    level_index = None
    if not all([isinstance(x, np.ndarray) for x in (vertices, tris,
     vertex_data, levels)]):
        raise ValueError('all inputs must be numpy arrays')
    elif vertices.shape[1] <= 3:
        verts = vertices
    else:
        if vertices.shape[1] == 4:
            verts = vertices[:, :-1]
        else:
            verts = None
    if verts is not None:
        if tris.shape[1] == 3:
            if vertex_data.shape[0] == verts.shape[0]:
                edges = np.vstack((tris.reshape(-1),
                 np.roll(tris, (-1), axis=1).reshape(-1))).T
                edge_datas = vertex_data[edges]
                edge_coors = verts[edges].reshape(tris.shape[0] * 3, 2, 3)
                for lev in levels:
                    index = edge_datas >= lev
                    index = index[:, 0] ^ index[:, 1]
                    edge_datas_Ok = edge_datas[index, :]
                    xyz = edge_coors[index]
                    ratio = np.array([
                     (lev - edge_datas_Ok[:, 0]) / (edge_datas_Ok[:, 1] - edge_datas_Ok[:, 0])])
                    point = xyz[:, 0, :] + ratio.T * (xyz[:, 1, :] - xyz[:, 0, :])
                    nbr = point.shape[0] // 2
                    if connects is not None:
                        connect = np.arange(0, nbr * 2).reshape((nbr, 2)) + len(lines)
                        connects = np.append(connects, connect, axis=0)
                        lines = np.append(lines, point, axis=0)
                        vertex_level = np.append(vertex_level, np.zeros(len(point)) + lev)
                        level_index = np.append(level_index, np.array(len(point)))
                    else:
                        lines = point
                        connects = np.arange(0, nbr * 2).reshape((nbr, 2))
                        vertex_level = np.zeros(len(point)) + lev
                        level_index = np.array(len(point))
                    vertex_level = vertex_level.reshape((vertex_level.size, 1))

    return (
     lines, connects, vertex_level, level_index)


class IsolineVisual(LineVisual):
    __doc__ = 'Isocurves of a tri mesh with data at vertices at different levels.\n\n    Parameters\n    ----------\n    vertices : ndarray, shape (Nv, 3) | None\n        Vertex coordinates.\n    tris : ndarray, shape (Nf, 3) | None\n        Indices into the vertex array.\n    data : ndarray, shape (Nv,) | None\n        scalar at vertices\n    levels : ndarray, shape (Nlev,) | None\n        The levels at which the isocurve is constructed from "data".\n    color_lev : Color, tuple, colormap name or array\n        The color to use when drawing the line. If an array is given, it\n        must be of shape (Nlev, 4) and provide one rgba color by level.\n    **kwargs : dict\n        Keyword arguments to pass to `LineVisual`.\n    '

    def __init__(self, vertices=None, tris=None, data=None, levels=None, color_lev=None, **kwargs):
        self._data = None
        self._vertices = None
        self._tris = None
        self._levels = levels
        self._color_lev = color_lev
        self._need_color_update = True
        self._need_recompute = True
        self._v = None
        self._c = None
        self._vl = None
        self._li = None
        self._lc = None
        self._cl = None
        self._update_color_lev = False
        kwargs['antialias'] = False
        (LineVisual.__init__)(self, method='gl', **kwargs)
        self.set_data(vertices=vertices, tris=tris, data=data)

    @property
    def levels(self):
        """ The threshold at which the isocurves are constructed from the data.
        """
        return self._levels

    @levels.setter
    def levels(self, levels):
        self._levels = levels
        self._need_recompute = True
        self.update()

    @property
    def data(self):
        """The mesh data"""
        return (
         self._vertices, self._tris, self._data)

    def set_data(self, vertices=None, tris=None, data=None):
        """Set the data

        Parameters
        ----------
        vertices : ndarray, shape (Nv, 3) | None
            Vertex coordinates.
        tris : ndarray, shape (Nf, 3) | None
            Indices into the vertex array.
        data : ndarray, shape (Nv,) | None
            scalar at vertices
        """
        if data is not None:
            self._data = data
            self._need_recompute = True
        if vertices is not None:
            self._vertices = vertices
            self._need_recompute = True
        if tris is not None:
            self._tris = tris
            self._need_recompute = True
        self.update()

    @property
    def color(self):
        return self._color_lev

    def set_color(self, color):
        """Set the color

        Parameters
        ----------
        color : instance of Color
            The color to use.
        """
        if color is not None:
            self._color_lev = color
            self._need_color_update = True
            self.update()

    def _levels_to_colors(self):
        try:
            f_color_levs = get_colormap(self._color_lev)
        except:
            colors = ColorArray(self._color_lev).rgba
        else:
            lev = _normalize(self._levels, self._levels.min(), self._levels.max())
            colors = f_color_levs.map(lev[:, np.newaxis])
        if len(colors) == 1:
            colors = colors * np.ones((len(self._levels), 1))
        if len(colors) != len(self._levels):
            raise TypeError('Color/level mismatch. Color must be of shape (Nlev, ...) and provide one color per level')
        self._lc = colors

    def _compute_iso_color(self):
        """ compute LineVisual color from level index and corresponding level
        color
        """
        level_color = []
        colors = self._lc
        for i, index in enumerate(self._li):
            level_color.append(np.zeros((index, 4)) + colors[i])

        self._cl = np.vstack(level_color)

    def _prepare_draw--- This code section failed: ---

 L. 225         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _data
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_TRUE     50  'to 50'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _levels
               14  LOAD_CONST               None
               16  COMPARE_OP               is
               18  POP_JUMP_IF_TRUE     50  'to 50'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _tris
               24  LOAD_CONST               None
               26  COMPARE_OP               is
               28  POP_JUMP_IF_TRUE     50  'to 50'

 L. 226        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _vertices
               34  LOAD_CONST               None
               36  COMPARE_OP               is
               38  POP_JUMP_IF_TRUE     50  'to 50'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                _color_lev
               44  LOAD_CONST               None
               46  COMPARE_OP               is
               48  POP_JUMP_IF_FALSE    54  'to 54'
             50_0  COME_FROM            38  '38'
             50_1  COME_FROM            28  '28'
             50_2  COME_FROM            18  '18'
             50_3  COME_FROM             8  '8'

 L. 227        50  LOAD_CONST               False
               52  RETURN_VALUE     
             54_0  COME_FROM            48  '48'

 L. 229        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _need_recompute
               58  POP_JUMP_IF_FALSE   144  'to 144'

 L. 230        60  LOAD_GLOBAL              iso_mesh_line

 L. 231        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _vertices
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                _tris
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _data
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                _levels
               78  CALL_FUNCTION_4       4  '4 positional arguments'
               80  UNPACK_SEQUENCE_4     4 
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _v
               86  LOAD_FAST                'self'
               88  STORE_ATTR               _c
               90  LOAD_FAST                'self'
               92  STORE_ATTR               _vl
               94  LOAD_FAST                'self'
               96  STORE_ATTR               _li

 L. 232        98  LOAD_FAST                'self'
              100  LOAD_METHOD              _levels_to_colors
              102  CALL_METHOD_0         0  '0 positional arguments'
              104  POP_TOP          

 L. 233       106  LOAD_FAST                'self'
              108  LOAD_METHOD              _compute_iso_color
              110  CALL_METHOD_0         0  '0 positional arguments'
              112  POP_TOP          

 L. 234       114  LOAD_GLOBAL              LineVisual
              116  LOAD_ATTR                set_data
              118  LOAD_FAST                'self'
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                _v
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                _c

 L. 235       128  LOAD_FAST                'self'
              130  LOAD_ATTR                _cl
              132  LOAD_CONST               ('pos', 'connect', 'color')
              134  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              136  POP_TOP          

 L. 236       138  LOAD_CONST               False
              140  LOAD_FAST                'self'
              142  STORE_ATTR               _need_recompute
            144_0  COME_FROM            58  '58'

 L. 238       144  LOAD_FAST                'self'
              146  LOAD_ATTR                _need_color_update
              148  POP_JUMP_IF_FALSE   188  'to 188'

 L. 239       150  LOAD_FAST                'self'
              152  LOAD_METHOD              _levels_to_colors
              154  CALL_METHOD_0         0  '0 positional arguments'
              156  POP_TOP          

 L. 240       158  LOAD_FAST                'self'
              160  LOAD_METHOD              _compute_iso_color
              162  CALL_METHOD_0         0  '0 positional arguments'
              164  POP_TOP          

 L. 241       166  LOAD_GLOBAL              LineVisual
              168  LOAD_ATTR                set_data
              170  LOAD_FAST                'self'
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                _cl
              176  LOAD_CONST               ('color',)
              178  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              180  POP_TOP          

 L. 242       182  LOAD_CONST               False
              184  LOAD_FAST                'self'
              186  STORE_ATTR               _update_color_lev
            188_0  COME_FROM           148  '148'

 L. 244       188  LOAD_GLOBAL              LineVisual
              190  LOAD_METHOD              _prepare_draw
              192  LOAD_FAST                'self'
              194  LOAD_FAST                'view'
              196  CALL_METHOD_2         2  '2 positional arguments'
              198  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 198