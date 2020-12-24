# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/postprocessing/nested_sampling_compare_logZ.py
# Compiled at: 2018-12-11 11:18:10
__doc__ = '\nCreated on Tue Oct 23 14:11:05 2018\n\n@author:\nMaximilian N. Günther\nMIT Kavli Institute for Astrophysics and Space Research, \nMassachusetts Institute of Technology,\n77 Massachusetts Avenue,\nCambridge, MA 02109, \nUSA\nEmail: maxgue@mit.edu\nWeb: www.mnguenther.com\n'
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction': 'in', 'ytick.direction': 'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import numpy as np, matplotlib.pyplot as plt, os, sys, gzip
try:
    import cPickle as pickle
except:
    import pickle

from dynesty import utils as dyutils
from tqdm import tqdm

def ns_plot_bayes_factors(run_names, labels):
    """
    Inputs:
    -------
    run_names : list of str (see Example 1) OR tuple of lists of str (see Example 2)
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
    run_names = ['circular_model', 'eccentric_model']
    labels = ['circular', 'eccentric']
    fig, ax = ns_compare_logZ(run_names, labels)
    
    
    Example 2:
    ----------
    #::: do multiple model comparisons in one plot
    run_names_1 = ['circular_model', 'eccentric_model']
    labels_1 = ['circular', 'eccentric']
    
    run_names_2 = ['no_occultation_model', 'occultation_model']
    labels_2 = ['without occultation', 'with occulation']
    
    collection_of_run_names = ( run_names_1, run_names_2 )
    collection_of_labels = ( labels_1, labels_2 )
    
    fig, ax = ns_compare_logZ(run_names, labels)
    """
    if isinstance(run_names, list):
        delta_logZ, delta_logZ_err, delta_labels = get_delta_logZ_and_delta_labels(run_names, labels)
    elif isinstance(run_names, tuple):
        delta_logZ, delta_logZ_err, delta_labels = get_collective_delta_logZ_and_delta_labels(run_names, labels)
    else:
        raise ValueError('run_names must be tuple or list.')
    index = np.arange(len(delta_logZ))
    fig, ax = plt.subplots(figsize=(3 * len(run_names), 4))
    ax.bar(index, delta_logZ, edgecolor='b')
    ax.errorbar(index, delta_logZ, yerr=delta_logZ_err, color='k', linestyle='none', markersize=0, capsize=2, elinewidth=5, zorder=10)
    ax.set_xticks(index)
    ax.set_xticklabels(delta_labels)
    ymax = np.nanmax(list(delta_logZ) + [7])
    ax.axhspan(3, 5, color='g', zorder=-1, alpha=0.33)
    ax.axhspan(5, ymax, color='g', zorder=-1, alpha=0.66)
    ax.text(index[(-1)] + 0.55, 1.5, 'no strong\nevidence', va='center')
    ax.text(index[(-1)] + 0.55, 4, 'strong\nevidence', va='center')
    ax.text(index[(-1)] + 0.55, 6, 'very strong\nevidence', va='center')
    ax.set(ylim=[0, ymax], ylabel='$\\Delta \\log{Z}$')
    return (
     fig, ax)


def get_delta_logZ_and_delta_labels(run_names, labels):
    logZ, logZ_err = get_logZ(run_names)
    delta_logZ = np.array(logZ) - logZ[0]
    delta_logZ_err = np.sqrt(np.array(logZ_err) ** 2 + np.array(logZ_err[0]) ** 2)
    delta_logZ = delta_logZ[1:]
    delta_logZ_err = delta_logZ_err[1:]
    delta_labels = [ labels[(i + 1)] + '\nvs.\n' + labels[0] for i in range(len(delta_logZ)) ]
    return (
     delta_logZ, delta_logZ_err, delta_labels)


def get_logZ(run_names):
    logZ = []
    logZ_err = []
    for rname in run_names:
        try:
            fname = os.path.join(rname, 'results', 'save_ns.pickle.gz')
            print('--------------------------')
            print(fname)
            f = gzip.GzipFile(fname, 'rb')
            results = pickle.load(f)
            f.close()
        except:
            fname = os.path.join(rname, 'results', 'save_ns.pickle')
            print('--------------------------')
            print(fname)
            with open(fname, 'rb') as (f):
                results = pickle.load(f)

        logZdynesty = results.logz[(-1)]
        logZerrdynesty = results.logzerr[(-1)]
        if np.isnan(logZerrdynesty) or np.isinf(logZerrdynesty) or logZerrdynesty / logZdynesty > 1:
            print('recalculating logZ error...')
            sys.stdout.flush()
            lnzs = np.zeros((10, len(results.logvol)))
            for i in tqdm(range(10)):
                results_s = dyutils.simulate_run(results)
                lnzs[i] = np.interp(-results.logvol, -results_s.logvol, results_s.logz)

            lnzerr = np.std(lnzs, axis=0)
            logZerrdynesty = lnzerr[(-1)]
        print(('log(Z) = {} +- {}').format(logZdynesty, logZerrdynesty))
        logZ.append(logZdynesty)
        logZ_err.append(logZerrdynesty)

    return (
     logZ, logZ_err)


def get_collective_delta_logZ_and_delta_labels(collection_of_run_names, collection_of_labels):
    """
    Example:
    --------
    run_names_1 = ['circular_model', 'eccentric_model']
    labels_1 = ['circular', 'eccentric']
    
    run_names_2 = ['no_occultation_model', 'occultation_model']
    labels_2 = ['without occultation', 'with occulation']
    
    collection_of_run_names = ( run_names_1, run_names_2 )
    collection_of_labels = ( labels_1, labels_2 )
    
    delta_logZ, delta_logZ_err, delta_labels =         get_collective_delta_logZ_and_delta_labels(collection_of_run_names, collection_of_labels)
    """
    delta_logZ, delta_logZ_err, delta_labels = [], [], []
    for run_names, labels in zip(collection_of_run_names, collection_of_labels):
        a, b, c = get_delta_logZ_and_delta_labels(run_names, labels)
        delta_logZ += list(a)
        delta_logZ_err += list(b)
        delta_labels += list(c)

    return (delta_logZ, delta_logZ_err, delta_labels)