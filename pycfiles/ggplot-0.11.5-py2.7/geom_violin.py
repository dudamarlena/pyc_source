# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/geoms/geom_violin.py
# Compiled at: 2016-08-12 16:37:32
from .geom import geom

class geom_violin(geom):
    """
    Violin plots

    Parameters
    ----------
    x:
        x values for (x, y) coordinates
    y:
        y values to be violin'd
    color:
        color of line

    Examples
    --------
    """
    DEFAULT_AES = {'y': None, 'color': 'black'}
    REQUIRED_AES = {
     'x', 'y'}
    DEFAULT_PARAMS = {}

    def plot(self, ax, data, _aes, x_levels):
        data, _aes = self._update_data(data, _aes)
        params = self._get_plot_args(data, _aes)
        variables = _aes.data
        xticks = []
        for i, xvalue in enumerate(x_levels):
            subset = data[(data[variables['x']] == xvalue)]
            yi = subset[variables['y']].values
            plot_parts = ax.violinplot(yi, positions=[i], showextrema=False)
            for pc in plot_parts['bodies']:
                pc.set_facecolor('white')
                pc.set_edgecolor('black')
                pc.set_alpha(1.0)
                pc.set_linewidth(1.0)

            xticks.append(i)

        ax.set_xticks(xticks)
        ax.set_xticklabels(x_levels)