# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/geoms/geom_line.py
# Compiled at: 2016-07-31 12:14:34
from .geom import geom

class geom_line(geom):
    """
    Line chart

    Parameters
    ----------
    x:
        x values for (x, y) coordinates
    y:
        y values for (x, y) coordinates
    color:
        color of line
    alpha:
        transparency of color
    linetype:
        type of the line ('solid', 'dashed', 'dashdot', 'dotted')
    size:
        thickness of line

    Examples
    --------
    """
    is_path = False
    DEFAULT_AES = {'color': 'black', 'alpha': 1.0, 'linetype': 'solid', 'size': 1.0}
    REQUIRED_AES = {'x', 'y'}
    DEFAULT_PARAMS = {}
    _aes_renames = {'size': 'linewidth', 'linetype': 'linestyle'}

    def plot(self, ax, data, _aes):
        data, _aes = self._update_data(data, _aes)
        params = self._get_plot_args(data, _aes)
        variables = _aes.data
        x = data[variables['x']]
        y = data[variables['y']]
        nulls = x.isnull() | y.isnull()
        x = x[(nulls == False)]
        y = y[(nulls == False)]
        if self.is_path:
            pass
        else:
            order = x.argsort()
            x, y = x.iloc[order], y.iloc[order]
        ax.plot(x, y, **params)