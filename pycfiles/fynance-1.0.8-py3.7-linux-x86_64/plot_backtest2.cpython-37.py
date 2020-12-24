# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fynance/dev/plot_backtest2.py
# Compiled at: 2019-05-24 08:59:25
# Size of source mod 2**32: 4972 bytes
""" Module with some object and functions to plot backtest. """
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
plt.style.use('seaborn')
__all__ = [
 'PlotPerf', 'PlotLoss']

class _PlotBase(object):
    __doc__ = ' Base class for plot backtest.\n\n    Attributes\n    ----------\n    fig : matplotlib.figure.Figure\n        Figure to display backtest.\n    ax : matplotlib.axes\n        Axe(s) to display a part of backtest.\n\n    Methods\n    -------\n    plot : Plot performance.\n\n    '

    def __init__(self, fig=None, ax=None, size=(9, 6), dynam=False, **kwargs):
        """ Inititalize method.

        Set size of training and predicting period, inital
        value to backtest, a target filter and training parameters.

        Parameters
        ----------
        fig : matplotlib.figure.Figure, optional
            Figure to display backtest.
        ax : matplotlib.axes, optional
            Axe(s) to display a part of backtest.
        size : tuple, optional
            Size of figure, default is (9, 6)
        dynam : bool, optional
            If True set on interactive plot.
        kwargs : dict, optional
            Axes configuration, cf matplotlib documentation [1]_. Default is
            {'yscale': 'linear', 'xscale': 'linear', 'ylabel': '',
            'xlabel': '', 'title': '', 'tick_params': {}}

        References
        ----------
        .. [1] https://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes

        """
        self._set_figure(fig, ax, size, dynam=dynam)
        (self._set_axes)(**kwargs)

    def _set_figure(self, fig, ax, size, dynam=False):
        """ Set figure, axes and parameters for dynamic plot. """
        if fig is None and ax is None:
            self.fig, self.ax = plt.subplots(1, 1, size)
        else:
            self.fig, self.ax = fig, ax
        if dynam:
            plt.ion()
        return self

    def _plot(self, y, x=None, names=None, col='Blues', lw=1.0, **kwargs):
        """ Plot performances.

        Parameters
        ----------
        y : np.ndarray[np.float64, ndim=2], with shape (`T`, `N`)
            Returns or indexes.
        x : np.ndarray[ndim=2], with shape (`T`, 1), optional
            x-axis, can be series of int or dates or string.
        names : str, optional
            Names y lines for legend.
        col : str, optional
            Color of palette, cf seaborn documentation [1]_.
            Default is 'Blues'.
        lw : float, optional
            Line width of lines.
        kwargs : dict, optional
            Parameters for `ax.legend` method cf matplotlib documentation [2]_.

        Returns
        -------
        pbt : PlotBackTest
            Self object.

        References
        ----------
        .. [1] https://seaborn.pydata.org/api.html
        .. [2] https://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes

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
        l = self.ax.plot(x, y, LineWidth=lw)
        for i in range(N):
            l[i].set_color(col[i])
            l[i].set_label(self._set_name((names[i]), (y[:, i]), unit=unit))

        (self.ax.legend)(**kwargs)
        return self

    def _set_axes(self, yscale='linear', xscale='linear', ylabel='', xlabel='', title='', tick_params={}):
        """ Set axes parameters. """
        self.ax.clear()
        self.ax.set_yscale(yscale)
        self.ax.set_xscale(xscale)
        self.ax.set_ylabel(ylabel)
        self.ax.set_xlabel(xlabel, x=0.9)
        self.ax.set_title(title)
        (self.ax.tick_params)(**tick_params)
        return self


class PlotPerf(_PlotBase):
    __doc__ = ' TODO : docstring. '

    def _set_name(self, name, y):
        """ Set name of perf plot. """
        return 'Perf {}: {:.0%}'.format(name, y[(-1)] / y[0] - 1)

    def plot(self):
        """ TODO : docstring. """
        y_label = 'Perf'


class PlotLoss(_PlotBase):
    __doc__ = ' TODO : docstring. '

    def _set_name(self, name, y):
        """ Set name of loss plot. """
        return 'Loss {}: {:.2f}'.format(name, y[(-1)])

    def plot(self, y_loss):
        """ TODO : docstring. """
        y_label = 'Loss'
        self._plot(y_loss,
          names='Estim NN', col='BuGn', lw=2.0)