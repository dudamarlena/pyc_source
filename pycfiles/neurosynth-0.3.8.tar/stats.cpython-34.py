# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tal/Dropbox/Code/neurosynth/neurosynth/analysis/stats.py
# Compiled at: 2015-08-10 12:19:20
# Size of source mod 2**32: 2517 bytes
"""Various statistical helper functions"""
import warnings, numpy as np
from scipy import special
from scipy.stats import ss

def pearson(x, y):
    """ Correlates row vector x with each row vector in 2D array y. """
    data = np.vstack((x, y))
    ms = data.mean(axis=1)[(slice(None, None, None), None)]
    datam = data - ms
    datass = np.sqrt(ss(datam, axis=1))
    temp = np.dot(datam[1:], datam[0].T)
    rs = temp / (datass[1:] * datass[0])
    return rs


def two_way(cells):
    """ Two-way chi-square test of independence.
    Takes a 3D array as input: N(voxels) x 2 x 2, where the last two dimensions
    are the contingency table for each of N voxels. Returns an array of
    p-values.
    """
    warnings.simplefilter('ignore', RuntimeWarning)
    cells = cells.astype('float64')
    total = np.apply_over_axes(np.sum, cells, [1, 2]).ravel()
    chi_sq = np.zeros(cells.shape, dtype='float64')
    for i in range(2):
        for j in range(2):
            exp = np.sum(cells[:, i, :], 1).ravel() * np.sum(cells[:, :, j], 1).ravel() / total
            bad_vox = np.where(exp == 0)[0]
            chi_sq[:, i, j] = (cells[:, i, j] - exp) ** 2 / exp
            chi_sq[(bad_vox, i, j)] = 1.0

    chi_sq = np.apply_over_axes(np.sum, chi_sq, [1, 2]).ravel()
    return special.chdtrc(1, chi_sq)


def one_way(data, n):
    """ One-way chi-square test of independence.
    Takes a 1D array as input and compares activation at each voxel to
    proportion expected under a uniform distribution throughout the array. Note
    that if you're testing activation with this, make sure that only valid
    voxels (e.g., in-mask gray matter voxels) are included in the array, or
    results won't make any sense!
    """
    term = data.astype('float64')
    no_term = n - term
    t_exp = np.mean(term, 0)
    t_exp = np.array([t_exp] * data.shape[0])
    nt_exp = n - t_exp
    t_mss = (term - t_exp) ** 2 / t_exp
    nt_mss = (no_term - nt_exp) ** 2 / nt_exp
    chi2 = t_mss + nt_mss
    return special.chdtrc(1, chi2)


def fdr(p, q=0.05):
    """ Determine FDR threshold given a p value array and desired false
    discovery rate q. """
    s = np.sort(p)
    nvox = p.shape[0]
    null = np.array(range(1, nvox + 1), dtype='float') * q / nvox
    below = np.where(s <= null)[0]
    if any(below):
        return s[max(below)]
    return -1