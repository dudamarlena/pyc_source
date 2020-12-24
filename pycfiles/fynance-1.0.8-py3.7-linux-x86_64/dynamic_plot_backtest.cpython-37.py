# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fynance/backtest/dynamic_plot_backtest.py
# Compiled at: 2019-09-21 13:56:53
# Size of source mod 2**32: 3213 bytes
""" Module with some function plot backtest. """
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from fynance.backtest.plot_backtest import PlotBackTest
plt.style.use('seaborn')
__all__ = [
 'DynaPlotBackTest']

class DynaPlotBackTest(PlotBackTest):
    __doc__ = " Dynamic plot backtest object.\n\n    Attributes\n    ----------\n    fig : matplotlib.figure.Figure\n        Figure to display backtest.\n    ax : matplotlib.axes\n        Axe(s) to display a part of backtest.\n\n    Methods\n    -------\n    plot(y, x=None, names=None, col='Blues', lw=1., **kwargs)\n        Plot performances.\n\n    See Also\n    --------\n    PlotBackTest, display_perf, set_text_stats\n\n    "
    plt.ion()

    def plot(self, y, x=None, names=None, col='Blues', lw=1.0, unit='raw', **kwargs):
        """ Dynamic plot performances.

        Parameters
        ----------
        y : np.ndarray[np.float64, ndim=2], with shape (`T`, `N`)
            Returns or indexes.
        x : np.ndarray[ndim=2], with shape (`T`, 1), optional
            x-axis, can be series of int or dates or string.
        names : str, optional
            Names y lines for legend.
        col : str, optional
            Color of palette, cf seaborn documentation [2]_.
            Default is 'Blues'.
        lw : float, optional
            Line width of lines.
        kwargs : dict, optional
            Parameters for `ax.legend` method, cf matplotlib
            documentation [3]_.

        Returns
        -------
        pbt : PlotBackTest
            Self object.

        References
        ----------
        .. [2] https://seaborn.pydata.org/api.html
        .. [3] https://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes

        """
        T, N = y.shape
        if x is None:
            x = np.arange(T)
        elif names is None:
            names = ['$Model_{}$'.format(i) for i in range(N)]
        else:
            if isinstance(names, str):
                names = ['${}_{}$'.format(names, i) for i in range(N)]
        col = sns.color_palette(col, N)
        h = self.ax.plot(x, y, LineWidth=lw)
        for i in range(N):
            h[i].set_color(col[i])
            h[i].set_label(self._set_name((names[i]), (y[:, i]), unit=unit))

        (self.ax.legend)(**kwargs)
        return self

    def _set_name(self, name, y, unit='raw', **kwargs):
        if unit.lower() == 'raw':
            return '{}: {:.2f}'.format(name, y[(-1)])
        if unit.lower() == 'perf':
            return '{}: {:.0%}'.format(name, y[(-1)] / y[0] - 1)
        raise ValueError