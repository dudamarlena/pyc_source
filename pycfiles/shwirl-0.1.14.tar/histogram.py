# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/visuals/histogram.py
# Compiled at: 2016-11-03 01:40:19
import numpy as np
from .mesh import MeshVisual
from ..ext.six import string_types

class HistogramVisual(MeshVisual):
    """Visual that calculates and displays a histogram of data

    Parameters
    ----------
    data : array-like
        Data to histogram. Currently only 1D data is supported.
    bins : int | array-like
        Number of bins, or bin edges.
    color : instance of Color
        Color of the histogram.
    orientation : {'h', 'v'}
        Orientation of the histogram.
    """

    def __init__(self, data, bins=10, color='w', orientation='h'):
        data = np.asarray(data)
        if data.ndim != 1:
            raise ValueError('Only 1D data currently supported')
        if not isinstance(orientation, string_types) or orientation not in ('h', 'v'):
            raise ValueError('orientation must be "h" or "v", not %s' % (
             orientation,))
        X, Y = (0, 1) if orientation == 'h' else (1, 0)
        data, bin_edges = np.histogram(data, bins)
        rr = np.zeros((3 * len(bin_edges) - 2, 3), np.float32)
        rr[:, X] = np.repeat(bin_edges, 3)[1:-1]
        rr[1::3, Y] = data
        rr[2::3, Y] = data
        bin_edges.astype(np.float32)
        tris = np.zeros((2 * len(bin_edges) - 2, 3), np.uint32)
        offsets = 3 * np.arange(len(bin_edges) - 1, dtype=np.uint32)[:, np.newaxis]
        tri_1 = np.array([0, 2, 1])
        tri_2 = np.array([2, 0, 3])
        tris[::2] = tri_1 + offsets
        tris[1::2] = tri_2 + offsets
        MeshVisual.__init__(self, rr, tris, color=color)