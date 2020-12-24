# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/prepare_ttv_fit.py
# Compiled at: 2020-02-01 10:37:24
# Size of source mod 2**32: 4203 bytes
__doc__ = '\nCreated on Fri Jan 31 15:50:31 2020\n\n@author: \nDr. Maximilian N. Günther\nMIT Kavli Institute for Astrophysics and Space Research, \nMassachusetts Institute of Technology,\n77 Massachusetts Avenue,\nCambridge, MA 02109, \nUSA\nEmail: maxgue@mit.edu\nGitHub: https://github.com/MNGuenther\nWeb: www.mnguenther.com\n'
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction':'in',  'ytick.direction':'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import numpy as np
import matplotlib.pyplot as plt
import os, allesfitter
from allesfitter.exoworlds_rdx.lightcurves.index_transits import get_tmid_observed_transits

def prepare_ttv_fit(datadir, ax=None):
    """
    this must be run *after* reduce_phot_data()
    """
    ax0 = ax
    alles = allesfitter.allesclass(datadir)

    def plot_all_transits_color_coded():
        width = alles.settings['fast_fit_width']
        for inst in alles.settings['inst_phot']:
            time = alles.data[inst]['time']
            for companion in alles.settings['companions_phot']:
                ind = []
                for i, t in enumerate(alles.data[(companion + '_tmid_observed_transits')]):
                    ind += list(np.where((time >= t - width / 2.0) & (time <= t + width / 2.0))[0])

                ax.plot((alles.data[inst]['time'][ind]), (alles.data[inst]['flux'][ind]), ls='none', marker='.', label=companion)

    for companion in alles.settings['companions_phot']:
        print('#TTV companion ' + companion)
        all_times = []
        all_flux = []
        for inst in alles.settings['inst_phot']:
            all_times += list(alles.data[inst]['time'])
            all_flux += list(alles.data[inst]['flux'])

        alles.data[companion + '_tmid_observed_transits'] = get_tmid_observed_transits(all_times, alles.initial_guess_params_median[(companion + '_epoch')], alles.initial_guess_params_median[(companion + '_period')], alles.settings['fast_fit_width'])
        for i, t in enumerate(alles.data[(companion + '_tmid_observed_transits')]):
            print(companion + '_ttv_transit_' + str(i + 1) + ',0,1,uniform -0.05 0.05,TTV$_\\mathrm{' + companion + ';' + str(i + 1) + '}$,d')

        flux_min = np.nanmin(all_flux)
        flux_max = np.nanmax(all_flux)
        if ax0 is None:
            days = np.max(all_times) - np.min(all_times)
            figsizex = np.max([5, 5 * (days / 10.0)])
            fig, ax = plt.subplots(figsize=(figsizex, 4))
        for inst in alles.settings['inst_phot']:
            ax.plot((alles.fulldata[inst]['time']), (alles.fulldata[inst]['flux']), ls='none', marker='.', color='silver')

        plot_all_transits_color_coded()
        ax.plot((alles.data[(companion + '_tmid_observed_transits')]), (np.ones_like(alles.data[(companion + '_tmid_observed_transits')]) * 0.997 * flux_min), 'k^', zorder=12)
        for i, tmid in enumerate(alles.data[(companion + '_tmid_observed_transits')]):
            ax.text(tmid, (0.992 * flux_min), (str(i + 1)), ha='center', zorder=12)
            ax.axvline(tmid, color='grey', zorder=11)

        ax.set(ylim=[0.99 * flux_min, 1.002 * flux_max], xlabel='Time (BJD)', ylabel='Realtive Flux', title=('Companion ' + companion))
        ax.legend(loc='best')
        if not os.path.exists(os.path.join(datadir, 'results')):
            os.makedirs(os.path.join(datadir, 'results'))
        fname = os.path.join(datadir, 'results', 'preparation_for_TTV_fit_' + companion + '.jpg')
        fig = plt.gcf()
        fig.savefig(fname, bbox_inches='tight')
        plt.close(fig)