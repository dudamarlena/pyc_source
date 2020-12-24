# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tareen/Desktop/Desktop_Tests/MPathic3/mpathic/src/info.py
# Compiled at: 2018-06-21 15:25:34
# Size of source mod 2**32: 8665 bytes
"""Module containing information theory esimtation routines."""
from __future__ import division
import numpy as np, scipy as sp, pandas as pd
from mpathic.src import _nsb
import pdb
from mpathic import SortSeqError

def mutualinfo(raw_pxy, tol=1e-10):
    """
    Simply computes mutual information given a 2d probability distribution 
    """
    with open('test_error', 'w') as (f):
        np.savetxt(f, raw_pxy)
    pxy = fix_probs_2d(raw_pxy)
    px = fix_probs(pxy.sum(axis=1))
    py = fix_probs(pxy.sum(axis=0))
    mi = entropy(px) + entropy(py) - entropy(pxy)
    if abs(mi) < tol:
        mi = 0.0
    elif not mi >= 0.0:
        raise AssertionError
    return mi


def entropy(raw_ps):
    """
    Simply computes entropy given a probability distribution
    """
    ps = fix_probs(raw_ps)
    indices = ps > 0.0
    ent = -np.sum(ps[indices] * np.log2(ps[indices]))
    assert ent >= 0.0
    return ent


def estimate_mutualinfo(raw_counts, pseudocount=1, err=False, method='naive'):
    """
    Naive mutual information esimator. raw_counts must be a 2d array
    """
    assert method in ('naive', 'tpm', 'nsb')
    if not pseudocount >= 0:
        raise SortSeqError('pseudocount is not nonnegative.')
    counts = fix_counts_2d(raw_counts)
    if method == 'naive':
        if err:
            mi, mi_err = _estimate_mutualinfo_naive(counts, pseudocount=pseudocount,
              err=True)
        else:
            mi = _estimate_mutualinfo_naive(counts, pseudocount=pseudocount,
              err=False)
    else:
        if method == 'tpm':
            if err:
                mi, mi_err = _estimate_mutualinfo_naive(counts, pseudocount=pseudocount,
                  err=True)
            else:
                mi = _estimate_mutualinfo_naive(counts, pseudocount=pseudocount,
                  err=False)
            n_rows = counts.shape[0]
            n_cols = counts.shape[1]
            N = counts.flatten().sum()
            mi -= (n_cols - 1.0) * (n_rows - 1.0) * np.log2(np.exp(1.0)) / (2.0 * N)
        else:
            if method == 'nsb':
                if err:
                    mi, mi_err = _estimate_mutualinfo_nsb(counts, err=True)
                else:
                    mi = _estimate_mutualinfo_nsb(counts, err=False)
            else:
                raise SortSeqError('Unknown method: %s.' % method)
        if err:
            return (mi, mi_err)
        else:
            return mi


def estimate_entropy(counts, method='naive', err=False):
    """
    Wrapper for all entropy estimators
    """
    if method == 'naive':
        if err:
            ent, ent_err = _estimate_entropy_naive(counts, err=True)
        else:
            ent = _estimate_entropy_naive(counts, err=False)
    else:
        if method == 'nsb':
            if err:
                ent, ent_err = _estimate_entropy_nsb(counts, err=True)
            else:
                ent = _estimate_entropy_nsb(counts, err=False)
        else:
            raise SortSeqError('Method %s unrecognized in estimate_entropy().')
    if err:
        return (ent, ent_err)
    else:
        return ent


def _estimate_entropy_naive(raw_counts, pseudocount=1, err=False, num_samples=25):
    """
    Naive entropy estimator
    """
    counts = fix_counts(raw_counts) + pseudocount
    ps = fix_probs(counts)
    ent = entropy(ps)
    assert ent >= 0
    if err:
        resampled_ents = np.zeros(num_samples)
        for n in range(num_samples):
            resampled_counts = sp.random.poisson(counts)
            if not all(resampled_counts.flatten() == 0.0):
                resampled_ps = fix_probs(resampled_counts)
                resampled_ents[n] = entropy(resampled_ps)

        ent_err = np.std(resampled_ents)
    if err:
        return (ent, ent_err)
    else:
        return ent


def _estimate_mutualinfo_naive(raw_counts, pseudocount=1, err=False, num_samples=25):
    """
    Naive mutual information estimator
    """
    counts = fix_counts_2d(raw_counts) + pseudocount
    ps = fix_probs_2d(counts)
    mi = mutualinfo(ps)
    assert mi >= 0
    if err:
        resampled_mis = np.zeros(num_samples)
        for n in range(num_samples):
            resampled_counts = sp.random.poisson(counts)
            if not all(resampled_counts.flatten() == 0.0):
                resampled_ps = fix_probs_2d(resampled_counts)
                resampled_mi = mutualinfo(resampled_ps)
                resampled_mis[n] = resampled_mi

        mi_err = np.std(resampled_mis)
    if err:
        return (mi, mi_err)
    else:
        return mi


def _estimate_entropy_nsb(raw_counts, maxlen=1000, err=False):
    """
    NSB entropy estimator
    """
    counts = fix_counts(raw_counts)
    if not len(counts) <= maxlen:
        raise SortSeqError('len(counts)==%d is too big for NSB.' % len(counts))
    N = counts.sum()
    K = len(counts)
    ent = float(_nsb.S(counts, N, K))
    if err:
        ent_err = float(_nsb.dS(counts, N, K))
    if err:
        return (ent, ent_err)
    else:
        return ent


def _estimate_mutualinfo_nsb(raw_counts, err=False):
    """
    NSB mutual information estimator
    """
    counts = fix_counts_2d(raw_counts)
    counts_xy = counts.flatten()
    counts_x = counts.sum(axis=1)
    counts_y = counts.sum(axis=0)
    mi_xy, mi_err_xy = _estimate_entropy_nsb(counts_xy, err=True)
    mi_x, mi_err_x = _estimate_entropy_nsb(counts_x, err=True)
    mi_y, mi_err_y = _estimate_entropy_nsb(counts_y, err=True)
    mi = mi_x + mi_y - mi_xy
    mi_err = np.sqrt(mi_err_xy ** 2 + mi_err_x ** 2 + mi_err_y ** 2)
    if err:
        return (mi, mi_err)
    else:
        return mi


def fix_counts_2d(raw_counts):
    """
    Converts to numpy array of floats.
    Checks that array is 2d, elements are nonnegative and not all zero. 
    """
    try:
        counts = np.array(raw_counts).astype(float)
    except:
        raise SortSeqError('could not covernt counts to array of flots')

    if len(counts.shape) != 2:
        raise SortSeqError('counts array is not 2d.')
    if not all(np.isfinite(counts.flatten())):
        raise SortSeqError('counts are all finite.')
    if not all(counts.flatten() >= 0.0):
        raise SortSeqError('counts are not nonnegative.')
    if all(counts.flatten() == 0.0):
        raise SortSeqError('counts are all equal to zero.')
    return counts


def fix_counts(raw_counts):
    """
    Flattens and converts to floats.
    Also checks that elements are present, are nonnegative, and not all zero. 
    """
    try:
        counts = np.array(raw_counts).astype(float).flatten()
    except:
        raise SortSeqError('could not covernt counts to array of flots')

    if len(counts.shape) == 0.0:
        raise SortSeqError('counts is empty or not array.')
    if not all(np.isfinite(counts)):
        raise SortSeqError('counts are not all finite.')
    if not all(counts >= 0.0):
        raise SortSeqError('counts are not nonnegative.')
    if all(counts == 0.0):
        raise SortSeqError('counts are all equal to zero.')
    return counts


def fix_probs_2d(raw_ps):
    """
    Make sure probability distribution is 2d and valid
    """
    ps = fix_counts_2d(raw_ps)
    ps /= ps.flatten().sum()
    return ps


def fix_probs(raw_ps):
    """
    Make sure probability distribution is 1d and valid
    """
    ps = fix_counts(raw_ps)
    ps /= ps.sum()
    return ps