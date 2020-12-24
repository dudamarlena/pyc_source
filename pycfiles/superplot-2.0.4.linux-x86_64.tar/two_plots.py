# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/michael/anaconda2/lib/python2.7/site-packages/superplot/example/two_plots.py
# Compiled at: 2017-08-19 22:58:02
"""
=================================================
Example with 2 or more plots on top of each other
=================================================
"""
import matplotlib.pyplot as plt, numpy as np, superplot.data_loader as data_loader, superplot.plotlib.plot_mod as pm, superplot.statslib.two_dim as two_dim, superplot.statslib.one_dim as one_dim, superplot.statslib.point as stats
from superplot.schemes import scheme_from_yaml
BIN_LIMITS = [
 [
  -10000, 10000], [-10000, 10000]]
ALPHA = [0.045500263896, 0.31731050786]
XINDEX = 2
YINDEX = 3
XLABEL = '$x$'
YLABEL = '$y$'
TEXTS = ['gaussian_.txt', 'SB_MO_log_allpost.txt']
YAMLS = ['config.yml', 'alt_config.yml']
LEG_LOCS = ['upper right', 'lower right']
LEG_TITLES = ['Gaussian', 'CMSSM']

def add_data(data, scheme, leg_loc, leg_title):
    """
    Add dataset to current plot.

    :param data: Chain from e.g. MultiNest
    :type data: np.array
    :param scheme: A scheme of styles for plot
    :type scheme: Scheme
    :param leg_loc: Location of legend
    :type leg_loc: str
    :param leg_title: Title of legend
    :type leg_title: str
    """
    posterior = data[0]
    chisq = data[1]
    xdata = data[XINDEX]
    ydata = data[YINDEX]
    pdf_data = two_dim.kde_posterior_pdf(xdata, ydata, posterior, bin_limits=BIN_LIMITS)
    pdf = pdf_data.pdf / pdf_data.pdf.sum()
    levels = [ two_dim.critical_density(pdf, aa) for aa in ALPHA ]
    pm.plot_contour(pdf, levels, scheme.posterior, BIN_LIMITS)
    best_fit_x = stats.best_fit(chisq, xdata)
    best_fit_y = stats.best_fit(chisq, ydata)
    pm.plot_data(best_fit_x, best_fit_y, scheme.best_fit, zorder=2)
    posterior_mean_x = stats.posterior_mean(np.sum(pdf_data.pdf, axis=1), pdf_data.bin_centers_x)
    posterior_mean_y = stats.posterior_mean(np.sum(pdf_data.pdf, axis=0), pdf_data.bin_centers_y)
    pm.plot_data(posterior_mean_x, posterior_mean_y, scheme.posterior_mean, zorder=2)
    posterior_modes = two_dim.posterior_mode(*pdf_data)
    for bin_center_x, bin_center_y in posterior_modes:
        pm.plot_data(bin_center_x, bin_center_y, scheme.posterior_mode, zorder=2)

    posterior_median_x = one_dim.posterior_median(np.sum(pdf_data.pdf, axis=1), pdf_data.bin_centers_x)
    posterior_median_y = one_dim.posterior_median(np.sum(pdf_data.pdf, axis=0), pdf_data.bin_centers_y)
    pm.plot_data(posterior_median_x, posterior_median_y, scheme.posterior_median, zorder=2)
    handles, labels = plt.gca().get_legend_handles_labels()
    leg = plt.legend(prop={'size': 10}, handles=handles[-6:], labels=labels[-6:], loc=leg_loc, title=leg_title)
    leg.get_title().set_fontsize('10')
    plt.gca().add_artist(leg)


schemes = map(scheme_from_yaml, YAMLS)
datas = map(data_loader._read_data_file, TEXTS)
fig = plt.figure()
pm.appearance('TwoDimPlotPDF')
plt.xlim(BIN_LIMITS[0])
plt.ylim(BIN_LIMITS[1])
plt.xlabel(XLABEL)
plt.ylabel(YLABEL)
for data, scheme, leg_loc, leg_title in zip(datas, schemes, LEG_LOCS, LEG_TITLES):
    add_data(data, scheme, leg_loc, leg_title)

plt.savefig('combined.pdf')