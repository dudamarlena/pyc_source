# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/geoms/geom_point.py
# Compiled at: 2016-07-31 12:14:34
from .geom import geom
import numpy as np
from ..utils import is_date

def _date_to_number(i):
    return i.toordinal() + i.time().hour / 24 + i.time().minute / 1440 + i.time().second / 86400


class geom_point(geom):
    """
    Scatterplot of (x, y) coordinates

    Parameters
    ----------
    x:
        x values for (x, y) coordinates
    y:
        y values for (x, y) coordinates
    color:
        color of points
    alpha:
        transparency of color
    shape:
        type of point used ('o', '^', 'D', 'v', 's', '*', 'p', '8', "_", "|", "_")
    edgecolors:
        color of the outer line of the point
    size:
        size of the point

    Examples
    --------
    """
    DEFAULT_AES = {'alpha': 1, 'color': 'black', 'shape': 'o', 'size': 20, 'edgecolors': 'none'}
    REQUIRED_AES = {
     'x', 'y'}
    _aes_renames = {'size': 's', 'shape': 'marker', 'color': 'c'}
    DEFAULT_PARAMS = {'position': None}

    def plot(self, ax, data, _aes):
        data, _aes = self._update_data(data, _aes)
        params = self._get_plot_args(data, _aes)
        variables = _aes.data
        x = data[variables['x']]
        y = data[variables['y']]
        if 'colormap' in variables:
            params['cmap'] = variables['colormap']
        if self.params.get('jitter'):
            x *= np.random.uniform(0.9, 1.1, len(x))
            y *= np.random.uniform(0.9, 1.1, len(y))
        if is_date(x.iloc[0]):
            dtype = x.iloc[0].__class__
            x = np.array([ _date_to_number(i) for i in x ])
            ax.scatter(x, y, **params)
            new_ticks = [ dtype(i) for i in ax.get_xticks() ]
            ax.set_xticklabels(new_ticks)
        else:
            ax.scatter(x, y, **params)