# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/geoms/geom_polygon.py
# Compiled at: 2016-07-31 12:14:34
from .geom import geom
import matplotlib.patches as patches

class geom_polygon(geom):
    """
    Polygon specified by (x, y) coordinates

    Parameters
    ----------
    x:
        x values for (x, y) coordinates
    y:
        y values for (x, y) coordinates
    color:
        color of outer line
    alpha:
        transparency of fill
    linetype:
        type of the line ('solid', 'dashed', 'dashdot', 'dotted')
    fill:
        color of the inside of the shape

    Examples
    --------
    """
    DEFAULT_AES = {'alpha': None, 'color': None, 'fill': '#333333', 'linetype': 'solid', 
       'size': 1.0}
    REQUIRED_AES = {'x', 'y'}
    DEFAULT_PARAMS = {}
    _aes_renames = {'linetype': 'linestyle', 'size': 'linewidth', 'fill': 'facecolor', 
       'color': 'edgecolor'}

    def plot(self, ax, data, _aes):
        data, _aes = self._update_data(data, _aes)
        params = self._get_plot_args(data, _aes)
        variables = _aes.data
        x = data[variables['x']]
        y = data[variables['y']]
        coordinates = zip(x, y)
        ax.add_patch(patches.Polygon(coordinates, closed=True, fill=True, **params))
        ax.autoscale_view()