# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/michael/anaconda2/lib/python2.7/site-packages/superplot/plotlib/plots.py
# Compiled at: 2017-08-19 22:58:02
"""
=============
plotlib.plots
=============

Implementation of plot classes. These inherit from the classes in 
plotlib.base and must specify a figure() method which returns
a matplotlib figure object.

Plots should also have a "description" attribute with a one line
description of the type of plot.

A list of implemented plot classes :py:data:`plotlib.plots.plot_types`
is found at the bottom of this module. This is useful for the GUI,
which needs to enumerate the available plots. So if a new plot type
is implemented, it should be added to this list.

Also includes a function to save the current plot.
"""
from itertools import groupby
from base import *
from scipy.stats import chi2
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def save_plot(name):
    """ 
    Save a plot with a descriptive name.
    
    .. Warning::
        Figure properties specfied in by mplstyle, but could be
        overridden here.

    :param name: Prefix of filename, without extension
    :type name: string

    """
    plt.savefig(name)


class OneDimStandard(OneDimPlot):
    """ 
    Makes a one dimensional plot, showing profile likelihood,
    marginalised posterior, and statistics. 
    """
    description = 'One-dimensional plot.'

    def figure(self):
        fig, ax = self._new_plot(point_height=0.02 * self.pdf_data.pdf.max())
        opt = self.plot_options
        ax.autoscale(axis='y')
        if opt.show_posterior_pdf:
            pm.plot_data(self.pdf_data.bin_centers, self.pdf_data.pdf, schemes.posterior)
        if opt.show_prof_like:
            pm.plot_data(self.prof_data.bin_centers, self.prof_data.prof_like, schemes.prof_like)
        lower_credible_region = [ one_dim.credible_region(self.pdf_data.pdf, self.pdf_data.bin_centers, alpha=aa, region='lower') for aa in opt.alpha
                                ]
        upper_credible_region = [ one_dim.credible_region(self.pdf_data.pdf, self.pdf_data.bin_centers, alpha=aa, region='upper') for aa in opt.alpha
                                ]
        self.summary.append(('Lower credible region: {}').format(lower_credible_region))
        self.summary.append(('Upper credible region: {}').format(upper_credible_region))
        if opt.show_credible_regions:
            cr_height = 1.1 * self.pdf_data.pdf.max()
            for lower, upper, scheme in zip(lower_credible_region, upper_credible_region, schemes.credible_regions):
                pm.plot_data([lower, upper], [cr_height, cr_height], scheme)

        conf_intervals = [ one_dim.conf_interval(self.prof_data.prof_chi_sq, self.prof_data.bin_centers, alpha=aa) for aa in opt.alpha
                         ]
        for intervals, scheme in zip(conf_intervals, schemes.conf_intervals):
            if opt.show_conf_intervals:
                pm.plot_data(intervals, [self.pdf_data.pdf.max()] * int(opt.nbins), scheme)
            self.summary.append(('{}:').format(scheme.label))
            for interval in intervals:
                self.summary.append(str(interval))

        pm.legend(opt.leg_title, opt.leg_position)
        if opt.show_posterior_pdf and not opt.show_prof_like:
            plt.ylabel(schemes.posterior.label)
        elif opt.show_prof_like and not opt.show_posterior_pdf:
            plt.ylabel(schemes.prof_like.label)
        else:
            plt.ylabel('')
        return self.plot_data(figure=fig, summary=self.summary)


class OneDimChiSq(OneDimPlot):
    """ 
    Makes a one dimensional plot, showing delta-chisq only,
    and excluded regions. 
    """
    description = 'One-dimensional chi-squared plot.'

    def figure(self):
        fig, ax = self._new_plot()
        opt = self.plot_options
        pm.plot_data(self.prof_data.bin_centers, self.prof_data.prof_chi_sq, schemes.prof_chi_sq)
        opt.plot_limits[3] = 10.0
        pm.plot_limits(ax, opt.plot_limits)
        critical_chi_sq = [ chi2.ppf(1.0 - aa, 1) for aa in opt.alpha ]
        for chi_sq, facecolor, name in zip(critical_chi_sq, schemes.prof_chi_sq.colours, schemes.prof_chi_sq.level_names):
            fill_where = self.prof_data.prof_chi_sq >= chi_sq
            if opt.show_conf_intervals:
                ax.fill_between(self.prof_data.bin_centers, 0, 10, where=fill_where, facecolor=facecolor, interpolate=False, alpha=0.7)
            self.summary.append(name + ':')
            for filled, group in groupby(zip(self.prof_data.bin_centers, fill_where), key=lambda x: x[1]):
                if filled:
                    bins = [ g[0] for g in group ]
                    self.summary.append(('{},{}').format(min(bins), max(bins)))

            if opt.show_conf_intervals:
                plt.plot(-1, -1, 's', color=facecolor, label=name, alpha=0.7, ms=15)

        if opt.tau is not None:
            pm.plot_band(self.prof_data.bin_centers, self.prof_data.prof_chi_sq, opt.tau, ax, schemes.tau_band)
        pm.legend(opt.leg_title, opt.leg_position)
        plt.ylabel(schemes.prof_chi_sq.label)
        return self.plot_data(figure=fig, summary=self.summary)


class TwoDimPlotFilledPDF(TwoDimPlot):
    """ Makes a two dimensional plot with filled credible regions only, showing
    best-fit and posterior mean. """
    description = 'Two-dimensional posterior pdf, filled contours only.'

    def figure(self):
        fig, ax = self._new_plot()
        opt = self.plot_options
        levels = [ two_dim.critical_density(self.pdf_data.pdf, aa) for aa in opt.alpha ]
        pdf = self.pdf_data.pdf
        pdf = pdf / pdf.sum()
        if opt.show_credible_regions:
            pm.plot_filled_contour(pdf, levels, schemes.posterior, bin_limits=opt.bin_limits)
        pm.legend(opt.leg_title, opt.leg_position)
        return self.plot_data(figure=fig, summary=self.summary)


class TwoDimPlotFilledPL(TwoDimPlot):
    """ Makes a two dimensional plot with filled confidence intervals only, showing
    best-fit and posterior mean. """
    description = 'Two-dimensional profile likelihood, filled contours only.'

    def figure(self):
        fig, ax = self._new_plot()
        opt = self.plot_options
        levels = [ two_dim.critical_prof_like(aa) for aa in opt.alpha ]
        if opt.show_conf_intervals:
            pm.plot_filled_contour(self.prof_data.prof_like, levels, schemes.prof_like, bin_limits=opt.bin_limits)
        pm.legend(opt.leg_title, opt.leg_position)
        return self.plot_data(figure=fig, summary=self.summary)


class TwoDimPlotPDF(TwoDimPlot):
    """ Makes a two dimensional marginalised posterior plot, showing
    best-fit and posterior mean and credible regions. """
    description = 'Two-dimensional posterior pdf.'

    def figure(self):
        fig, ax = self._new_plot()
        opt = self.plot_options
        if opt.show_posterior_pdf:
            pm.plot_image(self.pdf_data.pdf, opt.bin_limits, opt.plot_limits, schemes.posterior)
        levels = [ two_dim.critical_density(self.pdf_data.pdf, aa) for aa in opt.alpha ]
        pdf = self.pdf_data.pdf
        pdf = pdf / pdf.sum()
        if opt.show_credible_regions:
            pm.plot_contour(pdf, levels, schemes.posterior, bin_limits=opt.bin_limits)
        pm.legend(opt.leg_title, opt.leg_position)
        return self.plot_data(figure=fig, summary=self.summary)


class TwoDimPlotPL(TwoDimPlot):
    """ Makes a two dimensional profile likelihood plot, showing
    best-fit and posterior mean and confidence intervals. """
    description = 'Two-dimensional profile likelihood.'

    def figure(self):
        fig, ax = self._new_plot()
        opt = self.plot_options
        if opt.show_prof_like:
            pm.plot_image(self.prof_data.prof_like, opt.bin_limits, opt.plot_limits, schemes.prof_like)
        levels = [ two_dim.critical_prof_like(aa) for aa in opt.alpha ]
        if opt.show_conf_intervals:
            pm.plot_contour(self.prof_data.prof_like, levels, schemes.prof_like, bin_limits=opt.bin_limits)
        pm.legend(opt.leg_title, opt.leg_position)
        return self.plot_data(figure=fig, summary=self.summary)


class Scatter(TwoDimPlot):
    """ Makes a three dimensional scatter plot, showing
    best-fit and posterior mean and credible regions and confidence intervals.
    The scattered points are coloured by the zdata. """
    description = 'Three-dimensional scatter plot.'

    def figure(self):
        fig, ax = self._new_plot()
        opt = self.plot_options
        min_ = np.percentile(self.zdata, 5.0)
        max_ = np.percentile(self.zdata, 95.0)
        sc = plt.scatter(self.xdata, self.ydata, s=schemes.scatter.size, c=self.zdata, marker=schemes.scatter.symbol, cmap=schemes.scatter.colour_map, norm=None, vmin=min_, vmax=max_, linewidth=0.0, verts=None, rasterized=True)
        cb = plt.colorbar(sc, orientation='vertical', fraction=0.046, pad=0.04)
        cb.ax.set_ylabel(opt.zlabel)
        cb.locator = MaxNLocator(8)
        cb.update_ticks()
        levels = [ two_dim.critical_density(self.pdf_data.pdf, aa) for aa in opt.alpha ]
        pdf = self.pdf_data.pdf
        pdf = pdf / pdf.sum()
        if opt.show_credible_regions:
            pm.plot_contour(pdf, levels, schemes.posterior, bin_limits=opt.bin_limits)
        levels = [ two_dim.critical_prof_like(aa) for aa in opt.alpha ]
        if opt.show_conf_intervals:
            pm.plot_contour(self.prof_data.prof_like, levels, schemes.prof_like, bin_limits=opt.bin_limits)
        pm.legend(opt.leg_title, opt.leg_position)
        return self.plot_data(figure=fig, summary=self.summary)


plot_types = [
 OneDimStandard,
 OneDimChiSq,
 TwoDimPlotFilledPDF,
 TwoDimPlotFilledPL,
 TwoDimPlotPDF,
 TwoDimPlotPL,
 Scatter]