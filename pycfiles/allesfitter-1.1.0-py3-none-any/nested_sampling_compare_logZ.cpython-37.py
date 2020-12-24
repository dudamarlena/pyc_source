# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/postprocessing/nested_sampling_compare_logZ.py
# Compiled at: 2020-03-09 17:19:13
# Size of source mod 2**32: 8245 bytes
"""
Created on Tue Oct 23 14:11:05 2018

@author:
Maximilian N. Günther
MIT Kavli Institute for Astrophysics and Space Research, 
Massachusetts Institute of Technology,
77 Massachusetts Avenue,
Cambridge, MA 02109, 
USA
Email: maxgue@mit.edu
Web: www.mnguenther.com
"""
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction':'in',  'ytick.direction':'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import numpy as np
import matplotlib.pyplot as plt
import os, sys, gzip
try:
    import cPickle as pickle
except:
    import pickle

from dynesty import utils as dyutils
from tqdm import tqdm

def ns_plot_bayes_factors(datadirs, labels=None, return_dlogZ=False, ax=None, explanation=False):
    """
    Inputs:
    -------
    datadirs : list of str (see Example 1) OR tuple of lists of str (see Example 2)
        all the directories from which 
        the first run_name must be the "null hypothesis"
        
    labels : list of str
        all the labels for the plot
        
    
    Outputs:
    --------
    fig : matplotlib.Figure object
    
    ax : matplotlib.Axes object
    
        
    Example 1:
    ---------
    #::: just do a single model comparison
    datadirs = ['circular_model', 'eccentric_model']
    labels = ['circular', 'eccentric']
    fig, ax = ns_compare_logZ(datadirs, labels)
    
    
    Example 2:
    ----------
    #::: do multiple model comparisons in one plot
    datadirs_1 = ['circular_model', 'eccentric_model']
    labels_1 = ['circular', 'eccentric']
    
    datadirs_2 = ['no_occultation_model', 'occultation_model']
    labels_2 = ['without occultation', 'with occulation']
    
    collection_of_datadirs = ( datadirs_1, datadirs_2 )
    collection_of_labels = ( labels_1, labels_2 )
    
    fig, ax = ns_compare_logZ(datadirs, labels)
    """
    if labels is None:
        labels = datadirs
    else:
        if isinstance(datadirs, list):
            delta_logZ, delta_logZ_err, delta_labels = get_delta_logZ_and_delta_labels(datadirs, labels)
        else:
            if isinstance(datadirs, tuple):
                delta_logZ, delta_logZ_err, delta_labels = get_collective_delta_logZ_and_delta_labels(datadirs, labels)
            else:
                raise ValueError('datadirs must be tuple or list.')
        index = np.arange(len(delta_logZ))
        if ax is None:
            fig, ax = plt.subplots(figsize=(3 * len(datadirs), 4))
        else:
            fig = plt.gcf()
    ax.bar(index, delta_logZ, edgecolor='b')
    ax.errorbar(index, delta_logZ, yerr=delta_logZ_err, color='k', linestyle='none', markersize=0, capsize=2, elinewidth=5, zorder=10)
    ax.set_xticks(index)
    ax.set_xticklabels(delta_labels)
    ymax = np.nanmax(list(1.1 * delta_logZ) + [7])
    ax.axhspan(3, 5, color='g', zorder=(-1), alpha=0.33)
    ax.axhspan(5, ymax, color='g', zorder=(-1), alpha=0.66)
    if explanation:
        ax.text((index[(-1)] + 1), 1.5, 'no strong\nevidence', va='center')
        ax.text((index[(-1)] + 1), 4, 'strong\nevidence', va='center')
        ax.text((index[(-1)] + 1), (np.max([(np.max(delta_logZ) + 5.0) / 2.0, 6.0])), 'very strong\nevidence', va='center')
    ax.set(ylim=[0, ymax], ylabel='$\\Delta \\ln{Z}$')
    if return_dlogZ:
        return (
         fig, ax, delta_logZ)
    return (fig, ax)


def get_delta_logZ_and_delta_labels(datadirs, labels):
    logZ, logZ_err = get_logZ(datadirs)
    delta_logZ = np.array(logZ) - logZ[0]
    delta_logZ_err = np.sqrt(np.array(logZ_err) ** 2 + np.array(logZ_err[0]) ** 2)
    delta_logZ = delta_logZ[1:]
    delta_logZ_err = delta_logZ_err[1:]
    delta_labels = [labels[(i + 1)] + '\nvs.\n' + labels[0] for i in range(len(delta_logZ))]
    return (
     delta_logZ, delta_logZ_err, delta_labels)


def get_logZ(datadirs, quiet=False):
    logZ = []
    logZ_err = []
    for rname in np.atleast_1d(datadirs):
        try:
            fname = os.path.join(rname, 'results', 'save_ns.pickle.gz')
            if not quiet:
                print('--------------------------')
                print(fname)
            f = gzip.GzipFile(fname, 'rb')
            results = pickle.load(f)
            f.close()
        except:
            fname = os.path.join(rname, 'results', 'save_ns.pickle')
            if not quiet:
                print('--------------------------')
                print(fname)
            with open(fname, 'rb') as (f):
                results = pickle.load(f)

        logZdynesty = results.logz[(-1)]
        logZerrdynesty = results.logzerr[(-1)]
        if not np.isnan(logZerrdynesty):
            if np.isinf(logZerrdynesty) or logZerrdynesty / logZdynesty > 1:
                if not quiet:
                    print('recalculating ln(Z) error...')
                sys.stdout.flush()
                lnzs = np.zeros((10, len(results.logvol)))
                for i in tqdm((range(10)), disable=quiet):
                    results_s = dyutils.simulate_run(results)
                    lnzs[i] = np.interp(-results.logvol, -results_s.logvol, results_s.logz)

                lnzerr = np.std(lnzs, axis=0)
                logZerrdynesty = lnzerr[(-1)]
            if not quiet:
                print('ln(Z) = {} +- {}'.format(logZdynesty, logZerrdynesty))
            logZ.append(logZdynesty)
            logZ_err.append(logZerrdynesty)

    return (
     logZ, logZ_err)


def get_collective_delta_logZ_and_delta_labels(collection_of_datadirs, collection_of_labels):
    """
    Example:
    --------
    datadirs_1 = ['circular_model', 'eccentric_model']
    labels_1 = ['circular', 'eccentric']
    
    datadirs_2 = ['no_occultation_model', 'occultation_model']
    labels_2 = ['without occultation', 'with occulation']
    
    collection_of_datadirs = ( datadirs_1, datadirs_2 )
    collection_of_labels = ( labels_1, labels_2 )
    
    delta_logZ, delta_logZ_err, delta_labels =         get_collective_delta_logZ_and_delta_labels(collection_of_datadirs, collection_of_labels)
    """
    delta_logZ, delta_logZ_err, delta_labels = [], [], []
    for datadirs, labels in zip(collection_of_datadirs, collection_of_labels):
        a, b, c = get_delta_logZ_and_delta_labels(datadirs, labels)
        delta_logZ += list(a)
        delta_logZ_err += list(b)
        delta_labels += list(c)

    return (
     delta_logZ, delta_logZ_err, delta_labels)