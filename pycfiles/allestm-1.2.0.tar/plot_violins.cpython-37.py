# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/postprocessing/plot_violins.py
# Compiled at: 2018-11-15 14:40:51
# Size of source mod 2**32: 3027 bytes
__doc__ = '\nCreated on Tue Oct 30 12:14:51 2018\n\n@author:\nMaximilian N. Günther\nMIT Kavli Institute for Astrophysics and Space Research, \nMassachusetts Institute of Technology,\n77 Massachusetts Avenue,\nCambridge, MA 02109, \nUSA\nEmail: maxgue@mit.edu\nWeb: www.mnguenther.com\n'
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction':'in',  'ytick.direction':'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import numpy as np
import matplotlib.pyplot as plt
from .. import get_mcmc_posterior_samples, get_ns_posterior_samples, get_labels

def mcmc_plot_violins(datadirs, labels, key):
    """
    Inputs:
    -------
    
    Outputs:
    -------
    violin plots comparing the parameters of different runs
    
    
    Example:
    --------
    datadirs = ['allesfit_global/allesfit_wouttess_ns',
                'allesfit_global/allesfit_onlytess_ns',
                'allesfit_global/allesfit_withtess_ns',
                ]
    labels = ['w/o TESS',
              'only TESS',
              'w/ TESS',
              ]
    ns_plot_violins(datadirs, labels)
    """
    return plot_violins(datadirs, labels, key, 'mcmc')


def ns_plot_violins(datadirs, labels, key):
    """
    Inputs:
    -------
    
    Outputs:
    -------
    violin plots comparing the parameters of different runs
    
    
    Example:
    --------
    datadirs = ['allesfit_global/allesfit_wouttess_ns',
                'allesfit_global/allesfit_onlytess_ns',
                'allesfit_global/allesfit_withtess_ns',
                ]
    labels = ['w/o TESS',
              'only TESS',
              'w/ TESS',
              ]
    ns_plot_violins(datadirs, labels)
    """
    return plot_violins(datadirs, labels, key, 'ns')


def plot_violins(datadirs, labels, key, mode):
    all_params = {}
    all_paramslabels = {}
    for datadir, label in zip(datadirs, labels):
        if mode == 'mcmc':
            all_params[label] = get_mcmc_posterior_samples(datadir, as_type='dic')
        elif mode == 'ns':
            all_params[label] = get_ns_posterior_samples(datadir, as_type='dic')
        all_paramslabels[label] = get_labels(datadir, as_type='dic')

    xsize = max(6, 1.5 * len(labels))
    fig, ax = plt.subplots(figsize=(xsize, 4))
    violinlist = []
    for l in labels:
        if key in all_params[l]:
            violinlist.append(all_params[l][key])
        else:
            violinlist.append(np.ones(10) * np.nan)

    positionlist = range(len(labels))
    ax.violinplot(violinlist, positions=positionlist, showmedians=True, showextrema=False)
    ax.set_xticks(positionlist)
    ax.set_xticklabels(labels)
    ax.set_ylabel(all_paramslabels[labels[0]][key])
    plt.tight_layout()
    return (
     fig, ax)