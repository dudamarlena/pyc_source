# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sisua/analysis/imputation_benchmarks.py
# Compiled at: 2019-08-27 05:49:40
# Size of source mod 2**32: 7802 bytes
from __future__ import absolute_import, division, print_function
from collections import OrderedDict, defaultdict
import numpy as np, pandas as pd, seaborn
from matplotlib import pyplot as plt
from scipy.stats import kde
from six import string_types
from sklearn.neighbors import KernelDensity
from odin import backend as K
from odin import visual
from odin.utils import as_tuple, cache_memory, catch_warnings_ignore
from odin.visual import plot_figure, to_axis
from sisua.data import get_dataset
from sisua.data.const import MARKER_GENES
from sisua.data.utils import standardize_protein_name

def get_imputed_indices(x_org, x_imp):
    """ Return the indices of the cells which are imputed"""
    ids = []
    for i, (xo, xi) in enumerate(zip(x_org, x_imp)):
        if np.sum(xo) != np.sum(xi):
            ids.append(i)

    return np.array(ids)


def correlation_scores(X, y, gene_name, protein_name, return_series=False):
    """ Spearman and Pearson correlation scores

  return_series : bool
      if True, return the gene and protein series, instead of
      calculating spearman, or pearson correlation scores

  Return
  ------
  `correlation_scores` or `correlation_series`

  of which,

  correlation_scores : dict(protein_name/gene_name=(spearman, pearson))
  correlation_series : dict(protein_name/gene_name=(gene_series, prot_series))

  """
    from scipy.stats import pearsonr, spearmanr
    gene_name = np.asarray(gene_name).ravel().tolist()
    protein_name = np.asarray(protein_name).ravel().tolist()
    if not X.shape[1] == len(gene_name):
        raise AssertionError('Number of genes mismatch')
    else:
        assert y.shape[1] == len(protein_name), 'Number of protein mismatch'
        assert X.shape[0] == y.shape[0], 'Number of sample mismatch'
    protein_name = [standardize_protein_name(i) for i in protein_name]
    prot2gene = {}
    for prot, gene in MARKER_GENES.items():
        if prot in protein_name:
            index = [i for i, name in enumerate(gene_name) if gene == name]
            if len(index) == 0:
                index = [i for i, name in enumerate(gene_name) if gene == name.split('_')[(-1)]]
        if len(index) == 1:
            prot2gene[protein_name.index(prot)] = index[0]
        else:
            if len(index) >= 2:
                raise RuntimeError('Found multiple gene index with the same name')

    scores = {}
    series = {}
    if len(prot2gene) > 0:
        for prot, gene in prot2gene.items():
            x_ = X[:, gene]
            y_ = y[:, prot]
            name = protein_name[prot] + '/' + gene_name[gene]
            series[name] = (x_, y_)
            if not return_series:
                scores[name] = (
                 spearmanr(x_, y_).correlation, pearsonr(x_, y_)[0])

    if return_series:
        series = OrderedDict(sorted((series.items()), key=(lambda x: x[0].split('/')[0])))
        return series
    else:
        scores = OrderedDict(sorted((scores.items()), key=(lambda x: x[0].split('/')[0])))
        return scores


def imputation_score(original, imputed):
    """ Median of medians for all distances """
    assert original.shape == imputed.shape
    nonzeros = np.nonzero(original)
    d = np.abs(original - imputed)
    return float(np.median(d))


def imputation_mean_score(original, corrupted, imputed):
    """ Mean of medians for each cell imputation score """
    assert original.shape == corrupted.shape == imputed.shape
    imputation_cells = []
    for cell_org, cell_crt, cell_imp in zip(original, corrupted, imputed):
        if np.sum(cell_org) != np.sum(cell_crt):
            imputation_cells.append(np.median(np.abs(cell_org - cell_imp)))

    if len(imputation_cells) > 0:
        return np.mean(imputation_cells)
    else:
        return 0


def imputation_std_score(original, corrupted, imputed):
    assert original.shape == corrupted.shape == imputed.shape
    imputation_cells = []
    for cell_org, cell_crt, cell_imp in zip(original, corrupted, imputed):
        if np.sum(cell_org) != np.sum(cell_crt):
            imputation_cells.append(np.median(np.abs(cell_org - cell_imp)))

    if len(imputation_cells) > 0:
        return np.std(imputation_cells)
    else:
        return 0


def plot_imputation_series(original, imputed, title='Imputation'):
    original = K.log_norm(original, axis=0)
    imputed = K.log_norm(imputed, axis=0)
    max_val = max(np.max(original), np.max(imputed))
    with catch_warnings_ignore(FutureWarning):
        grid = seaborn.pairplot(data=(pd.DataFrame({'Original Value':original, 
         'Imputed Value':imputed})),
          height=4,
          aspect=1,
          kind='reg',
          diag_kws={'bins': 180},
          plot_kws={'scatter_kws':dict(s=2, alpha=0.6), 
         'line_kws':dict(color='red', alpha=0.8), 
         'color':'g'})
        ids = np.linspace(0, max_val)
        grid.axes[(0, 1)].set_xlim((0, max_val))
        grid.axes[(0, 1)].set_ylim((0, max_val))
        grid.axes[(0, 1)].plot(ids, ids, linestyle='--', linewidth=1, color='black')
        grid.axes[(1, 0)].set_xlim((0, max_val))
        grid.axes[(1, 0)].set_ylim((0, max_val))
        grid.axes[(1, 0)].plot(ids, ids, linestyle='--', linewidth=1, color='black')


def plot_imputation(original, imputed, corrupted=None, kde_kernel='gaussian', ax=None, title='Imputation'):
    """ Original code: scVI
      Modified by: SISUA

  kde_kernel : string (default: 'linear')
    'gaussian', 'tophat', 'epanechnikov', 'exponential', 'linear',
    'cosine'

  """
    y = imputed
    x = original
    assert imputed.shape == original.shape
    if corrupted is not None:
        if not original.shape == corrupted.shape:
            raise AssertionError
    if corrupted is not None:
        mask = np.where(original != corrupted, True, False)
        x = x[mask]
        y = y[mask]
    ymax = 25
    mask = x < ymax
    x = x[mask]
    y = y[mask]
    mask = y < ymax
    x = x[mask]
    y = y[mask]
    l_minimum = np.minimum(x.shape[0], y.shape[0])
    x = x[:l_minimum]
    y = y[:l_minimum]
    data = np.vstack([x, y])
    axes = visual.to_axis(ax)
    axes.set_xlim([0, ymax])
    axes.set_ylim([0, ymax])
    nbins = 80
    xi, yi = np.mgrid[0:ymax:nbins * complex(0.0, 1.0), 0:ymax:nbins * complex(0.0, 1.0)]
    k_ = kde.gaussian_kde(data)
    zi = k_(np.vstack([xi.flatten(), yi.flatten()]))
    plt.title(title, fontsize=12)
    plt.ylabel('Imputed counts')
    plt.xlabel('Original counts')
    plt.pcolormesh(yi, xi, (zi.reshape(xi.shape)), cmap='Reds')
    a, _, _, _ = np.linalg.lstsq((y[:, np.newaxis]), x, rcond=(-1))
    linspace = np.linspace(0, ymax)
    plt.plot(linspace, (a * linspace), color='black')
    plt.plot(linspace, linspace, color='black', linestyle=':')