# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/geoms/geom_rect.py
# Compiled at: 2016-07-31 12:14:34
from .geom import geom
import matplotlib.patches as patches

class geom_rect(geom):
    """
    2-dimensional rectangle

    Parameters
    ----------
    xmin:
        min value for x
    xmax:
        max value for x
    ymin:
        min value for y
    ymax:
        max value for y
    color:
        color of outer line
    alpha:
        transparency of fill
    size:
        size of outer line
    linetype:
        type of the line ('solid', 'dashed', 'dashdot', 'dotted')
    fill:
        color of the interior shape

    Examples
    --------
    """
    DEFAULT_AES = {'alpha': None, 'color': None, 'fill': '#333333', 'linetype': 'solid', 
       'size': 1.0}
    REQUIRED_AES = {'xmin', 'xmax', 'ymin', 'ymax'}
    DEFAULT_PARAMS = {}
    _aes_renames = {'linetype': 'linestyle', 'size': 'linewidth', 'fill': 'facecolor', 
       'color': 'edgecolor'}

    def plot(self, ax, data, _aes):
        data, _aes = self._update_data(data, _aes)
        params = self._get_plot_args(data, _aes)
        variables = _aes.data
        xmin = data[variables['xmin']]
        xmax = data[variables['xmax']]
        ymin = data[variables['ymin']]
        ymax = data[variables['ymax']]
        for xmin_i, xmax_i, ymin_i, ymax_i in zip(xmin.values, xmax.values, ymin.values, ymax.values):
            ax.add_patch(patches.Rectangle((
             xmin_i, ymin_i), (xmax_i - xmin_i), (ymax_i - ymin_i), **params))

        ax.autoscale_view()