# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/michael/anaconda2/lib/python2.7/site-packages/superplot/plotlib/base.py
# Compiled at: 2016-09-09 23:03:24
"""
============
plotlib.base
============
This module contains abstract base classes, used to implement Plots.
"""
import os
from abc import ABCMeta, abstractmethod
import numpy as np, matplotlib.pyplot as plt, warnings
from collections import namedtuple
import plot_mod as pm, superplot.statslib.one_dim as one_dim, superplot.statslib.two_dim as two_dim, superplot.statslib.point as stats, superplot.schemes as schemes

class Plot(object):
    """
    Abstract base class for all plot types. Specifies interface for
    creating a plot object, and getting the figure associated
    with it. Does any common preprocessing / init (IE log scaling).

    :param data: Data dictionary loaded from chain file by :py:mod:`data_loader`
    :type data: dict
    :param plot_options: :py:data:`plot_options.plot_options` configuration tuple.
    :type plot_options: namedtuple
    """
    __metaclass__ = ABCMeta

    def __init__(self, data, plot_options):
        self.plot_options = plot_options
        self.posterior = np.array(data[0])
        self.chisq = np.array(data[1])
        self.xdata = np.array(data[plot_options.xindex])
        self.ydata = np.array(data[plot_options.yindex])
        self.zdata = np.array(data[plot_options.zindex])
        self.summary = []
        warnings.filterwarnings('error')
        if plot_options.logx:
            try:
                self.xdata = np.log10(self.xdata)
            except RuntimeWarning:
                print 'x-data not logged: probably logging a negative.'

        if plot_options.logy:
            try:
                self.ydata = np.log10(self.ydata)
            except RuntimeWarning:
                print 'y-data not logged: probably logging a negative.'

        if plot_options.logz:
            try:
                self.zdata = np.log10(self.zdata)
            except RuntimeWarning:
                print 'z-data not logged: probably logging a negative.'

        warnings.resetwarnings()

    def _new_plot(self):
        opt = self.plot_options
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        pm.plot_ticks(opt.xticks, opt.yticks, ax)
        pm.plot_labels(opt.xlabel, opt.ylabel, opt.plot_title, opt.title_position)
        pm.plot_limits(ax, opt.plot_limits)
        pm.appearance(self.__class__.__name__)
        return (
         fig, ax)

    plot_data = namedtuple('plot_data', ('figure', 'summary'))

    @abstractmethod
    def figure(self):
        """
        Abstract method - return the pyplot figure associated with this plot.

        :returns: Matplotlib figure, list of plot specific summary strings
        :rtype: named tuple (figure: matplotlib.figure.Figure, summary: list)
        """
        pass


class OneDimPlot(Plot):
    """
    Abstract base class for one dimensional plot types.     Handles initialization tasks common to one dimensional plots.
    """
    __metaclass__ = ABCMeta

    def __init__(self, data, plot_options):
        super(OneDimPlot, self).__init__(data, plot_options)
        opt = self.plot_options
        extent = np.zeros(4)
        extent[0] = min(self.xdata)
        extent[1] = max(self.xdata)
        extent[2] = 0
        extent[3] = 1.2
        if self.plot_options.bin_limits is None:
            self.plot_options = self.plot_options._replace(bin_limits=[
             extent[0], extent[1]])
        if self.plot_options.plot_limits is None:
            self.plot_options = self.plot_options._replace(plot_limits=extent)
        if opt.kde_pdf:
            self.pdf_data = one_dim.kde_posterior_pdf(self.xdata, self.posterior, bin_limits=opt.bin_limits, norm_area=not opt.show_prof_like, bw_method=opt.bw_method)
        else:
            self.pdf_data = one_dim.posterior_pdf(self.xdata, self.posterior, nbins=opt.nbins, bin_limits=opt.bin_limits, norm_area=not opt.show_prof_like)
        self.prof_data = one_dim.prof_data(self.xdata, self.chisq, nbins=opt.nbins, bin_limits=opt.bin_limits)
        self.best_fit = stats.best_fit(self.chisq, self.xdata)
        self.summary.append(('Best-fit point: {}').format(self.best_fit))
        self.posterior_mean = stats.posterior_mean(*self.pdf_data)
        self.summary.append(('Posterior mean: {}').format(self.posterior_mean))
        self.posterior_median = one_dim.posterior_median(*self.pdf_data)
        self.summary.append(('Posterior median: {}').format(self.posterior_median))
        self.posterior_modes = one_dim.posterior_mode(*self.pdf_data)
        self.summary.append(('Posterior mode/s: {}').format(self.posterior_modes))
        return

    def _new_plot(self, point_height=0.08):
        """
        Special new plot method for 1D plots.

        :param point_height: Height to plot point statistics (mean, median, mode)
        :type point_height: float
        """
        fig, ax = super(OneDimPlot, self)._new_plot()
        opt = self.plot_options
        if opt.show_best_fit:
            pm.plot_data(self.best_fit, point_height, schemes.best_fit, zorder=2)
        if opt.show_posterior_mean:
            pm.plot_data(self.posterior_mean, point_height, schemes.posterior_mean, zorder=2)
        if opt.show_posterior_median:
            pm.plot_data(self.posterior_median, point_height, schemes.posterior_median, zorder=2)
        if opt.show_posterior_mode:
            for mode in self.posterior_modes:
                pm.plot_data(mode, point_height, schemes.posterior_mode, zorder=2)

        return (
         fig, ax)


class TwoDimPlot(Plot):
    """
    Abstract base class for two dimensional plot types     (plus the 3D scatter plot which is an honorary two     dimensional plot for now). Handles initialization tasks     common to these plot types.
    """
    __metaclass__ = ABCMeta

    def __init__(self, data, plot_options):
        super(TwoDimPlot, self).__init__(data, plot_options)
        opt = self.plot_options
        extent = np.zeros(4)
        extent[0] = min(self.xdata)
        extent[1] = max(self.xdata)
        extent[2] = min(self.ydata)
        extent[3] = max(self.ydata)
        if self.plot_options.bin_limits is None:
            self.plot_options = self.plot_options._replace(bin_limits=[
             [
              extent[0], extent[1]], [extent[2], extent[3]]])
        if self.plot_options.plot_limits is None:
            self.plot_options = self.plot_options._replace(plot_limits=extent)
        if opt.kde_pdf:
            self.pdf_data = two_dim.kde_posterior_pdf(self.xdata, self.ydata, self.posterior, bw_method=opt.bw_method, bin_limits=opt.bin_limits)
        else:
            self.pdf_data = two_dim.posterior_pdf(self.xdata, self.ydata, self.posterior, nbins=opt.nbins, bin_limits=opt.bin_limits)
        self.prof_data = two_dim.profile_like(self.xdata, self.ydata, self.chisq, nbins=opt.nbins, bin_limits=opt.bin_limits)
        self.best_fit_x = stats.best_fit(self.chisq, self.xdata)
        self.best_fit_y = stats.best_fit(self.chisq, self.ydata)
        self.summary.append(('Best-fit point (x,y): {}, {}').format(self.best_fit_x, self.best_fit_y))
        self.posterior_mean_x = stats.posterior_mean(np.sum(self.pdf_data.pdf, axis=1), self.pdf_data.bin_centers_x)
        self.posterior_mean_y = stats.posterior_mean(np.sum(self.pdf_data.pdf, axis=0), self.pdf_data.bin_centers_y)
        self.summary.append(('Posterior mean (x,y): {}, {}').format(self.posterior_mean_x, self.posterior_mean_y))
        self.posterior_modes = two_dim.posterior_mode(*self.pdf_data)
        self.summary.append(('Posterior modes/s (x,y): {}').format(self.posterior_modes))
        self.posterior_median_x = one_dim.posterior_median(np.sum(self.pdf_data.pdf, axis=1), self.pdf_data.bin_centers_x)
        self.posterior_median_y = one_dim.posterior_median(np.sum(self.pdf_data.pdf, axis=0), self.pdf_data.bin_centers_y)
        self.summary.append(('Posterior median (x,y): {}, {}').format(self.posterior_median_x, self.posterior_median_y))
        return

    def _new_plot(self):
        fig, ax = super(TwoDimPlot, self)._new_plot()
        opt = self.plot_options
        if opt.show_best_fit:
            pm.plot_data(self.best_fit_x, self.best_fit_y, schemes.best_fit, zorder=2)
        if opt.show_posterior_mean:
            pm.plot_data(self.posterior_mean_x, self.posterior_mean_y, schemes.posterior_mean, zorder=2)
        if opt.show_posterior_mode:
            for bin_center_x, bin_center_y in self.posterior_modes:
                pm.plot_data(bin_center_x, bin_center_y, schemes.posterior_mode, zorder=2)

        if opt.show_posterior_median:
            pm.plot_data(self.posterior_median_x, self.posterior_median_y, schemes.posterior_median, zorder=2)
        return (fig, ax)