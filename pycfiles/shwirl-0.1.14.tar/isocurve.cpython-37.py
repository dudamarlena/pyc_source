# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/visuals/isocurve.py
# Compiled at: 2018-10-02 11:14:03
# Size of source mod 2**32: 8039 bytes
from __future__ import division
import numpy as np
from .line import LineVisual
from ..color import ColorArray
from color.colormap import _normalize, get_colormap
import geometry.isocurve as isocurve
from ..testing import has_matplotlib
_HAS_MPL = has_matplotlib()
if _HAS_MPL:
    try:
        from matplotlib import _cntr as cntr
    except ImportError:
        import warnings
        _HAS_MPL = False
        cntr = None

class IsocurveVisual(LineVisual):
    __doc__ = 'Displays an isocurve of a 2D scalar array.\n\n    Parameters\n    ----------\n    data : ndarray | None\n        2D scalar array.\n    levels : ndarray, shape (Nlev,) | None\n        The levels at which the isocurve is constructed from "*data*".\n    color_lev : Color, colormap name, tuple, list or array\n        The color to use when drawing the line. If a list is given, it\n        must be of shape (Nlev), if an array is given, it must be of\n        shape (Nlev, ...). and provide one color per level (rgba, colorname).\n    clim : tuple\n        (min, max) limits to apply when mapping level values through a\n        colormap.\n    **kwargs : dict\n        Keyword arguments to pass to `LineVisual`.\n\n    Notes\n    -----\n    '

    def __init__(self, data=None, levels=None, color_lev=None, clim=None, **kwargs):
        self._data = None
        self._levels = levels
        self._color_lev = color_lev
        self._clim = clim
        self._need_color_update = True
        self._need_level_update = True
        self._need_recompute = True
        self._X = None
        self._Y = None
        self._iso = None
        self._level_min = None
        self._data_is_uniform = False
        self._lc = None
        self._cl = None
        self._li = None
        self._connect = None
        self._verts = None
        kwargs['method'] = 'gl'
        kwargs['antialias'] = False
        (LineVisual.__init__)(self, **kwargs)
        if data is not None:
            self.set_data(data)

    @property
    def levels(self):
        """ The threshold at which the isocurve is constructed from the
        2D data.
        """
        return self._levels

    @levels.setter
    def levels(self, levels):
        self._levels = levels
        self._need_level_update = True
        self._need_recompute = True
        self.update()

    @property
    def color(self):
        return self._color_lev

    @color.setter
    def color(self, color):
        self._color_lev = color
        self._need_level_update = True
        self._need_color_update = True
        self.update()

    def set_data(self, data):
        """ Set the scalar array data

        Parameters
        ----------
        data : ndarray
            A 2D array of scalar values. The isocurve is constructed to show
            all locations in the scalar field equal to ``self.levels``.
        """
        self._data = data
        if _HAS_MPL and not self._X is None:
            if self._X.T.shape != data.shape:
                self._X, self._Y = np.meshgrid(np.arange(data.shape[0]), np.arange(data.shape[1]))
            self._iso = cntr.Cntr(self._X, self._Y, self._data.astype(float))
        else:
            if self._clim is None:
                self._clim = (
                 data.min(), data.max())
            if self._data.min() != self._data.max():
                self._data_is_uniform = False
            else:
                self._data_is_uniform = True
        self._need_recompute = True
        self.update()

    def _get_verts_and_connect(self, paths):
        """ retrieve vertices and connects from given paths-list
        """
        verts = np.vstack(paths)
        gaps = np.add.accumulate(np.array([len(x) for x in paths])) - 1
        connect = np.ones((gaps[(-1)]), dtype=bool)
        connect[gaps[:-1]] = False
        return (verts, connect)

    def _compute_iso_line(self):
        """ compute LineVisual vertices, connects and color-index
        """
        level_index = []
        connects = []
        verts = []
        choice = np.nonzero((self.levels > self._data.min()) & (self._levels < self._data.max()))
        levels_to_calc = np.array(self.levels)[choice]
        self._level_min = choice[0][0]
        for level in levels_to_calc:
            if _HAS_MPL:
                nlist = self._iso.trace(level, level, 0)
                paths = nlist[:len(nlist) // 2]
                v, c = self._get_verts_and_connect(paths)
                v += np.array([0.5, 0.5])
            else:
                paths = isocurve((self._data.astype(float).T), level, extend_to_edge=True,
                  connected=True)
                v, c = self._get_verts_and_connect(paths)
            level_index.append(v.shape[0])
            connects.append(np.hstack((c, [False])))
            verts.append(v)

        self._li = np.hstack(level_index)
        self._connect = np.hstack(connects)
        self._verts = np.vstack(verts)

    def _compute_iso_color(self):
        """ compute LineVisual color from level index and corresponding color
        """
        level_color = []
        colors = self._lc
        for i, index in enumerate(self._li):
            level_color.append(np.zeros((index, 4)) + colors[(i + self._level_min)])

        self._cl = np.vstack(level_color)

    def _levels_to_colors(self):
        try:
            f_color_levs = get_colormap(self._color_lev)
        except:
            colors = ColorArray(self._color_lev).rgba
        else:
            lev = _normalize(self._levels, self._clim[0], self._clim[1])
            colors = f_color_levs.map(lev[:, np.newaxis])
        if len(colors) == 1:
            colors = colors * np.ones((len(self._levels), 1))
        if len(colors) != len(self._levels):
            raise TypeError('Color/level mismatch. Color must be of shape (Nlev, ...) and provide one color per level')
        self._lc = colors

    def _prepare_draw--- This code section failed: ---

 L. 215         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _data
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_TRUE     36  'to 36'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _levels
               14  LOAD_CONST               None
               16  COMPARE_OP               is
               18  POP_JUMP_IF_TRUE     36  'to 36'

 L. 216        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _color_lev
               24  LOAD_CONST               None
               26  COMPARE_OP               is
               28  POP_JUMP_IF_TRUE     36  'to 36'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                _data_is_uniform
               34  POP_JUMP_IF_FALSE    40  'to 40'
             36_0  COME_FROM            28  '28'
             36_1  COME_FROM            18  '18'
             36_2  COME_FROM             8  '8'

 L. 217        36  LOAD_CONST               False
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'

 L. 219        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _need_level_update
               44  POP_JUMP_IF_FALSE    60  'to 60'

 L. 220        46  LOAD_FAST                'self'
               48  LOAD_METHOD              _levels_to_colors
               50  CALL_METHOD_0         0  '0 positional arguments'
               52  POP_TOP          

 L. 221        54  LOAD_CONST               False
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _need_level_update
             60_0  COME_FROM            44  '44'

 L. 223        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _need_recompute
               64  POP_JUMP_IF_FALSE   112  'to 112'

 L. 224        66  LOAD_FAST                'self'
               68  LOAD_METHOD              _compute_iso_line
               70  CALL_METHOD_0         0  '0 positional arguments'
               72  POP_TOP          

 L. 225        74  LOAD_FAST                'self'
               76  LOAD_METHOD              _compute_iso_color
               78  CALL_METHOD_0         0  '0 positional arguments'
               80  POP_TOP          

 L. 226        82  LOAD_GLOBAL              LineVisual
               84  LOAD_ATTR                set_data
               86  LOAD_FAST                'self'
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                _verts
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                _connect

 L. 227        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _cl
              100  LOAD_CONST               ('pos', 'connect', 'color')
              102  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              104  POP_TOP          

 L. 228       106  LOAD_CONST               False
              108  LOAD_FAST                'self'
              110  STORE_ATTR               _need_recompute
            112_0  COME_FROM            64  '64'

 L. 230       112  LOAD_FAST                'self'
              114  LOAD_ATTR                _need_color_update
              116  POP_JUMP_IF_FALSE   148  'to 148'

 L. 231       118  LOAD_FAST                'self'
              120  LOAD_METHOD              _compute_iso_color
              122  CALL_METHOD_0         0  '0 positional arguments'
              124  POP_TOP          

 L. 232       126  LOAD_GLOBAL              LineVisual
              128  LOAD_ATTR                set_data
              130  LOAD_FAST                'self'
              132  LOAD_FAST                'self'
              134  LOAD_ATTR                _cl
              136  LOAD_CONST               ('color',)
              138  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              140  POP_TOP          

 L. 233       142  LOAD_CONST               False
              144  LOAD_FAST                'self'
              146  STORE_ATTR               _need_color_update
            148_0  COME_FROM           116  '116'

 L. 235       148  LOAD_GLOBAL              LineVisual
              150  LOAD_METHOD              _prepare_draw
              152  LOAD_FAST                'self'
              154  LOAD_FAST                'view'
              156  CALL_METHOD_2         2  '2 positional arguments'
              158  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 158