# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/visuals/line_plot.py
# Compiled at: 2017-04-05 22:13:00
# Size of source mod 2**32: 4614 bytes
import numpy as np
from .line import LineVisual
from .markers import MarkersVisual
from .visual import CompoundVisual

class LinePlotVisual(CompoundVisual):
    __doc__ = "Visual displaying a plot line with optional markers.\n\n    Parameters\n    ----------\n    data : array-like\n        Arguments can be passed as ``(Y,)``, ``(X, Y)``, ``(X, Y, Z)`` or\n        ``np.array((X, Y))``, ``np.array((X, Y, Z))``.\n    color : instance of Color\n        Color of the line.\n    symbol : str\n        Marker symbol to use.\n    line_kind : str\n        Kind of line to draw. For now, only solid lines (``'-'``)\n        are supported.\n    width : float\n        Line width.\n    marker_size : float\n        Marker size. If `size == 0` markers will not be shown.\n    edge_color : instance of Color\n        Color of the marker edge.\n    face_color : instance of Color\n        Color of the marker face.\n    edge_width : float\n        Edge width of the marker.\n    connect : str | array\n        See LineVisual.\n    **kwargs : keyword arguments\n        Argements to pass to the super class.\n\n    Examples\n    --------\n    All of these syntaxes will work:\n\n        >>> LinePlotVisual(y_vals)\n        >>> LinePlotVisual(x_vals, y_vals)\n        >>> LinePlotVisual(xy_vals)\n\n    See also\n    --------\n    LineVisual, MarkersVisual, marker_types\n    "
    _line_kwargs = ('color', 'width', 'connect')
    _marker_kwargs = ('edge_color', 'face_color', 'edge_width', 'marker_size', 'symbol')
    _kw_trans = dict(marker_size='size')

    def __init__(self, data=None, color='k', symbol=None, line_kind='-', width=1.0, marker_size=10.0, edge_color='k', face_color='w', edge_width=1.0, connect='strip'):
        if line_kind != '-':
            raise ValueError('Only solid lines currently supported')
        self._line = LineVisual(method='gl', antialias=False)
        self._markers = MarkersVisual()
        CompoundVisual.__init__(self, [self._line, self._markers])
        self.set_data(data, color=color, symbol=symbol, width=width, marker_size=marker_size, edge_color=edge_color, face_color=face_color, edge_width=edge_width, connect=connect)

    def set_data(self, data=None, **kwargs):
        """Set the line data

        Parameters
        ----------
        data : array-like
            The data.
        **kwargs : dict
            Keywoard arguments to pass to MarkerVisual and LineVisal.
        """
        if data is None:
            pos = None
        else:
            if isinstance(data, tuple):
                pos = np.array(data).T.astype(np.float32)
            else:
                pos = np.atleast_1d(data).astype(np.float32)
            if pos.ndim == 1:
                pos = pos[:, np.newaxis]
            else:
                if pos.ndim > 2:
                    raise ValueError('data must have at most two dimensions')
                if pos.size == 0:
                    pos = self._line.pos
                    if len(kwargs) == 0:
                        raise TypeError('neither line points nor line propertiesare provided')
                else:
                    if pos.shape[1] == 1:
                        x = np.arange(pos.shape[0], dtype=np.float32)[:, np.newaxis]
                        pos = np.concatenate((x, pos), axis=1)
                    elif pos.shape[1] > 3:
                        raise TypeError('Too many coordinates given (%s; max is 3).' % pos.shape[1])
            line_kwargs = {}
            for k in self._line_kwargs:
                if k in kwargs:
                    k_ = self._kw_trans[k] if k in self._kw_trans else k
                    line_kwargs[k] = kwargs.pop(k_)

            if pos is not None or len(line_kwargs) > 0:
                self._line.set_data(pos=pos, **line_kwargs)
        marker_kwargs = {}
        for k in self._marker_kwargs:
            if k in kwargs:
                k_ = self._kw_trans[k] if k in self._kw_trans else k
                marker_kwargs[k_] = kwargs.pop(k)

        if pos is not None or len(marker_kwargs) > 0:
            self._markers.set_data(pos=pos, **marker_kwargs)
        if len(kwargs) > 0:
            raise TypeError('Invalid keyword arguments: %s' % kwargs.keys())