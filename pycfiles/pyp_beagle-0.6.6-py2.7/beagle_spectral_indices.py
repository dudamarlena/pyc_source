# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyp_beagle/beagle_spectral_indices.py
# Compiled at: 2019-07-16 04:25:49
import os, logging, ConfigParser
from collections import OrderedDict
from scipy.interpolate import interp1d
from bisect import bisect_left
import numpy as np
from itertools import tee, izip
import json, matplotlib.pyplot as plt, matplotlib.ticker as plticker, matplotlib.gridspec as gridspec
from matplotlib import rcParams
from matplotlib.axes import Axes
from astropy.io import ascii
from astropy.io import fits
import dependencies.set_shared_labels as shLab, sys, dependencies.WeightedKDE as WeightedKDE, dependencies.autoscale as autoscale
from dependencies.walker_random_sampling import WalkerRandomSampling
from dependencies import FillBetweenStep
from significant_digits import to_precision
from beagle_utils import BeagleDirectories, prepare_plot_saving, set_plot_ticks, plot_exists, prepare_violin_plot, extract_row
from beagle_observed_catalogue import ObservedCatalogue
from pkg_resources import resource_stream
TOKEN_SEP = ':'
microJy = np.float32(1e-29)
nanoJy = np.float32(1e-32)
p_value_lim = 0.05

def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


_TOKENS = [
 'lum', 'lumErr', 'ew', 'ewErr']
_COL_NAME = 'colName'
_LABEL = 'label'
_SEP = ':'

class SpectralIndicesCatalogue(ObservedCatalogue):

    def configure(self, file_name):
        self.line_config = OrderedDict()
        for line in open(file_name):
            if line.strip() and not line.startswith('#'):
                _line = line
                _key = _LABEL + _SEP
                if _key in line:
                    _label = line.split(_key)[1].split()[0]
                    self.line_config[_label] = OrderedDict()
                    for t in _TOKENS:
                        _key = t + _SEP + _COL_NAME + _SEP
                        if _key in line:
                            _value = line.split(_key)[1].split()[0]
                            self.line_config[_label][t] = _value


class SpectralIndices(object):

    def __init__(self, **kwargs):
        with open(kwargs.get('line_labels_json')) as (f):
            self.line_list = json.load(f, object_pairs_hook=OrderedDict)
        self.inset_fontsize = BeagleDirectories.inset_fontsize_fraction * BeagleDirectories.fontsize
        self.observed_catalogue = SpectralIndicesCatalogue()
        self.key = kwargs.get('ID_key')
        self.plot_log_flux = kwargs.get('plot_log_flux')
        self.print_values = kwargs.get('print_line_values')
        self.max_interval = kwargs.get('max_interval')

    def plot_line_fluxes(self, ID, replot=False, title=False, letter=None, signif_digits=1):
        suffix = ''
        plot_name = str(ID) + '_BEAGLE_spectral_indices' + suffix + '.pdf'
        if plot_exists(plot_name) and not replot:
            logging.warning('The plot "' + plot_name + '" already exists. \n Exiting the function.')
            return
        else:
            observation = extract_row(self.observed_catalogue.data, ID, key=self.key)
            fig = plt.figure(figsize=(12, 3))
            ax = fig.add_subplot(1, 1, 1)
            fits_file = os.path.join(BeagleDirectories.results_dir, str(ID) + '_' + BeagleDirectories.suffix + '.fits.gz')
            hdulist = fits.open(fits_file)
            model_fluxes = hdulist['spectral indices'].data
            n_lines = len(self.line_list)
            probability = hdulist['posterior pdf'].data['probability']
            width = 0.5
            minY_values = np.zeros(n_lines)
            maxY_values = np.zeros(n_lines)
            _observed_fluxes = np.zeros(n_lines)
            _observed_flux_errors = np.zeros(n_lines)
            _model_fluxes = np.zeros(n_lines)
            for i, (key, value) in enumerate(self.line_list.iteritems()):
                X = i + 1
                _line_conf = self.observed_catalogue.line_config[key]
                if 'lum' in _line_conf:
                    _col_name = _line_conf['lum']
                    _err_col_name = _line_conf['lumErr']
                elif 'ew' in _line_conf:
                    _col_name = _line_conf['ew']
                    _err_col_name = _line_conf['ewErr']
                _observed_flux = observation[_col_name]
                _observed_fluxes[i] = _observed_flux
                _observed_flux_err = observation[_err_col_name]
                _observed_flux_errors[i] = _observed_flux_err
                _label = value['label']
                _model_flux = model_fluxes[key]
                kde_pdf, pdf_norm, median_flux, x_plot, y_plot = prepare_violin_plot(_model_flux, weights=probability)
                _model_fluxes[i] = median_flux
                _max_y = np.max(y_plot)
                w = width / _max_y
                y_grid = np.full(len(x_plot), X)
                _lim_y = kde_pdf(median_flux) / pdf_norm * w
                kwargs = {'alpha': 0.8}
                ax.errorbar(X, _observed_flux, yerr=_observed_flux_err, color='dodgerblue', ls=' ', marker=' ', zorder=5, **kwargs)
                ax.plot(X, _observed_flux, color='dodgerblue', ls=' ', marker='D', markeredgewidth=0.0, markersize=8, zorder=3, **kwargs)
                kwargs = {'color': 'tomato', 'alpha': 0.7, 'edgecolor': 'black', 'linewidth': 0.2}
                ax.fill_betweenx(x_plot, (y_grid - y_plot * w), (y_grid + y_plot * w), zorder=2, **kwargs)
                ax.plot([X - _lim_y, X + _lim_y], [
                 median_flux, median_flux], color='black', zorder=2, linewidth=0.2)
                ax.plot(X, median_flux, color='black', marker='o', markersize=5, zorder=4, alpha=0.7)
                _all = np.concatenate((_observed_flux - _observed_flux_err, x_plot))
                _min = np.amin(_all[(_all > 0.0)])
                minY_values[i] = _min
                _all = np.concatenate((_observed_flux + _observed_flux_err, x_plot))
                _max = np.amax(_all[(_all > 0.0)])
                maxY_values[i] = _max

            minY = np.amin(minY_values)
            maxY = np.max(maxY_values)
            if self.print_values:
                _factor = 0.15
            else:
                _factor = 0.1
            if self.plot_log_flux:
                dY = np.log10(maxY) - np.log10(minY)
                minY = 10.0 ** (np.log10(minY) - _factor * dY)
                maxY = 10.0 ** (np.log10(maxY) + _factor * dY)
            else:
                dY = maxY - minY
                minY -= _factor * dY
                maxY += _factor * dY
            ax.set_ylim(minY, maxY)
            set_plot_ticks(ax, n_x=5)
            if self.plot_log_flux:
                ax.set_ylabel('$\\log(\\textnormal{F}/\\textnormal{erg} \\;                 \\textnormal{s}^{-1} \\, \\textnormal{cm}^{-2})$')
            else:
                ax.set_ylabel('$\\textnormal{F}/\\textnormal{erg} \\;                 \\textnormal{s}^{-1} \\, \\textnormal{cm}^{-2}$')
            plt.tick_params(axis='x', which='both', top='off', bottom='off')
            xticks = range(1, len(self.line_list) + 1)
            ax.set_xticks(xticks)
            ticklabels = list()
            alpha = 0.6
            minY, maxY = ax.get_ylim()
            dY = maxY - minY
            _factor = 0.03
            _init_fact = 0.04
            j = 1
            _fontsize = min(self.inset_fontsize, self.inset_fontsize / (0.075 * n_lines))
            for i, (line_key, line_value) in enumerate(self.line_list.iteritems()):
                X = i + 1
                ticklabels.append(line_value['label'])
                _variab_fact = _init_fact * j
                if self.plot_log_flux:
                    dY = np.log10(maxY) - np.log10(minY)
                    Y = 10.0 ** (np.log10(minY_values[i]) - _factor * dY)
                    Y_t0 = 10.0 ** (np.log10(maxY) - _variab_fact * dY)
                    Y_t1 = 10.0 ** (np.log10(maxY) - _variab_fact * dY - 1.4 * _init_fact * dY)
                else:
                    Y = minY_values[i] - _factor * dY
                    Y_t0 = maxY - _variab_fact * dY
                    Y_t1 = maxY - _variab_fact * dY - 1.4 * _init_fact * dY
                ax.plot([X, X], [minY, Y], color='black', ls=':', zorder=2, alpha=alpha)
                if self.print_values:
                    _val = _observed_fluxes[i]
                    if not _val > 0.0:
                        continue
                    _val_err = _observed_flux_errors[i]
                    _n = int(np.floor(np.log10(_val)))
                    _norm = 10.0 ** _n
                    _text = '$' + to_precision(_val / _norm, signif_digits + 2) + '\\pm' + to_precision(_val_err / _norm, signif_digits) + '$'
                    ax.text(X, Y_t0, _text, horizontalalignment='center', verticalalignment='center', color='black', fontsize=_fontsize)
                    _val = _model_fluxes[i]
                    _text = '$' + to_precision(_val / _norm, signif_digits + 2) + '$'
                    ax.text(X, Y_t1, _text, horizontalalignment='center', verticalalignment='center', color='black', fontsize=_fontsize)
                j += 1
                if j % 4 == 0:
                    j = 1

            ax.set_xticklabels(ticklabels, rotation=45, rotation_mode='anchor', ha='right')
            if self.plot_log_flux:
                ax.set_yscale('log')
            if title:
                plt.title(title)
            if letter is not None:
                ax.text(0.01, 0.94, '(' + letter + ')', horizontalalignment='left', verticalalignment='center', color='black', transform=ax.transAxes)
            name = prepare_plot_saving(plot_name)
            fig.savefig(name, dpi=None, facecolor='w', edgecolor='w', orientation='portrait', papertype='a4', format='pdf', transparent=False, bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)
            hdulist.close()
            return