# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/deeplearn/plot.py
# Compiled at: 2020-05-11 01:33:34
# Size of source mod 2**32: 4725 bytes
"""Graphcal plotting convenience utilities.

"""
__author__ = 'Paul Landes'
import logging, pylab
from scipy.stats import gaussian_kde
import numpy as np
import matplotlib.pyplot as plt
logger = logging.getLogger(__name__)

class PlotManager(object):
    __doc__ = 'A Convenience class to give window geomtry placement and blocking.\n\n    '

    def __init__(self, geometry=(50, 0), size=(5, 5), block=False):
        self.geometry = ('+{}+{}'.format)(*geometry)
        logger.debug('using geometry: {} -> {}'.format(geometry, self.geometry))
        self.size = size
        self.block = block

    @staticmethod
    def clear():
        if '_plot_mng_fig' in globals():
            del globals()['_plot_mng_fig']

    @property
    def fig(self):
        return self.get_fig()

    def get_fig(self, *args, **kwargs):
        global _plot_mng_fig
        if not hasattr(self, '_fig'):
            if '_plot_mng_fig' in globals():
                plt.close(_plot_mng_fig)
            _plot_mng_fig = self._fig = (plt.figure)(args, figsize=self.size, **kwargs)
        return self._fig

    @property
    def ax(self):
        return self.subplots()

    def subplots(self, *args, **kwargs):
        return (self.fig.subplots)(*args, **kwargs)

    def subplot(self, *args, **kwargs):
        return (self.fig.add_subplot)(*args, **kwargs)

    def show(self):
        mng = pylab.get_current_fig_manager()
        mng.window.wm_geometry(self.geometry)
        self.fig.tight_layout()
        plt.show(block=(self.block))

    def save(self, fig_path=None, *args, **kwargs):
        if fig_path is None:
            fig_path = 'fig.png'
        logger.info(f"saving output figure to {fig_path}")
        (plt.savefig)(fig_path, *args, **kwargs)


class DensityPlotManager(PlotManager):
    __doc__ = 'Create density plots.\n\n    '

    def __init__(self, data, covariance_factor=0.5, interval=None, margin=None, *args, **kwargs):
        """
        :param covariance_factor: smooth factor for visualization only
        """
        (super(DensityPlotManager, self).__init__)(*args, **kwargs)
        self.interval = interval
        self.margin = margin
        self.covariance_factor = covariance_factor
        self.data = data

    def plot(self):
        data = self.data
        ax = self.ax
        density = gaussian_kde(data)
        if ax is None:
            ax = self.ax
        if self.interval is None:
            self.interval = (
             min(data), max(data))
        if self.margin is None:
            self.margin = 0.2 * abs(self.interval[0] - self.interval[1])
        xs = np.linspace(self.interval[0] - self.margin, self.interval[1] + self.margin)
        logger.debug(f"data size: {len(data)}, X graph points: {len(xs)}")
        density.covariance_factor = lambda : self.covariance_factor
        density._compute_covariance()
        logger.debug(f"plotting with ax: {ax}")
        ax.plot(xs, density(xs))


class GraphPlotManager(PlotManager):

    def __init__(self, graph, style='spring', pos=None, *args, **kwargs):
        (super(GraphPlotManager, self).__init__)(*args, **kwargs)
        self.graph = graph
        self.style = style
        self.pos = pos
        self.set_draw_arguments()

    def set_draw_arguments(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def _get_layout_function(self):
        import networkx as nx
        style = self.style
        if style == 'spectral':
            layoutfn = nx.spectral_layout
        else:
            if style == 'circular':
                layoutfn = nx.circular_layout
            else:
                if style == 'spring':
                    layoutfn = nx.spring_layout
                else:
                    if style == 'shell':
                        layoutfn = nx.shell_layout
                    else:
                        if style == 'kamada':
                            layoutfn = nx.kamada_kawai_layout
                        else:
                            if style == 'planar':
                                layoutfn = nx.layout.planar_layout
                            else:
                                if style == 'random':
                                    layoutfn = nx.layout.random_layout
                                else:
                                    raise ValueError(f"no such layout: {style}")
        return layoutfn

    def _get_pos(self):
        if self.pos is None:
            layoutfn = self._get_layout_function()
            pos = layoutfn(self.graph)
        else:
            pos = self.pos
        return pos

    def show(self):
        import networkx as nx
        nxg = self.graph
        ax = self.ax
        pos = self._get_pos()
        (nx.draw_networkx)(nxg, *(self.args), pos=pos, ax=ax, **self.kwargs)
        super(GraphPlotManager, self).show()