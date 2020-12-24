# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zichen/Documents/Yan/MSEA_python_package/venv37/lib/python3.7/site-packages/msea/utils.py
# Compiled at: 2020-03-28 13:15:57
# Size of source mod 2**32: 6446 bytes
"""Utils for performing microbe-set enrichment analysis.
"""
from __future__ import print_function
import os
from urllib.request import urlopen
import numpy as np, pandas as pd
from scipy import stats
from tqdm import trange

def read_gmt(file_or_url):
    """
    Read a gmt file into a dictionary of sets.

    :param file_or_url: a GMT file or URL of a GMT file
    :return: a dictionary of sets
    """
    d_gmt = {}
    if os.path.isfile(file_or_url):
        fh = open(file_or_url, 'r')
    else:
        fh = urlopen(file_or_url)
    for line in fh:
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        sl = line.strip().split('\t')
        term, items = sl[0], set(sl[2:])
        d_gmt[term] = items

    fh.close()
    return d_gmt


def write_gmt(d_gmt, filename):
    """
    Write a dictionary of sets to a gmt file.

    :param d_gmt: a dictionary of sets
    :param filename: filename for the GMT file
    :return: returns nothing
    """
    with open(filename, 'w') as (out):
        for term, items in d_gmt.items():
            out.write(term + '\t' + '\t'.join(list(items)) + '\n')


def fisher_test(s1, s2, universe):
    """
    Perform Fisher's exact test for two sets.

    :param s1: a set of items
    :param s2: a set of items
    :param universe: int, universe size
    :return: returns the odds ratio and p-value

    """
    a = len(s1 & s2)
    b, c = len(s1), len(s2)
    oddsratio, pval = stats.fisher_exact([
     [
      a, b], [c, universe]])
    return (oddsratio, pval)


def get_empirical_ranks(d_gmt, n=1000, universe=1200, fix_size=None):
    """
    Generate random microbe sets to get empirical ranks for each term.

    :param n: number of permutations
    :param universe: number of microbes used as the universe size for Fisher's exact test
    :param fix_size: if None, uses variable sizes when generating random sets; if int,
        uses fixed size random sets to evaluate the null distribution of the ranks
    :return: returns the means and standard deviations of the null ranks

    """
    all_microbes = set()
    set_sizes = []
    for microbes in d_gmt.values():
        all_microbes = all_microbes | microbes
        set_sizes.append(len(microbes))

    print('Number of unique microbes:', len(all_microbes))
    all_microbes = list(all_microbes)
    n_terms = len(d_gmt)
    rank_mat = np.zeros((n_terms, n))
    for i in trange(n):
        if fix_size:
            size = fix_size
        else:
            size = np.random.choice(set_sizes, 1)[0]
        random_set = np.random.choice(all_microbes, size, replace=False)
        random_set = set(random_set)
        pvals = np.ones(n_terms)
        j = 0
        for term, genes_ref in d_gmt.items():
            oddsratio, pval = fisher_test(random_set, genes_ref, universe)
            pvals[j] = pval
            j += 1

        ranks = np.argsort(pvals)
        rank_mat[:, i] = ranks

    return (
     rank_mat.mean(axis=1), rank_mat.std(axis=1))


def _ecdf(x):
    """no frills empirical cdf used in fdrcorrection
    """
    nobs = len(x)
    return np.arange(1, nobs + 1) / float(nobs)


def multipletests_fdr_bh(pvals, is_sorted=False):
    """
    FDR Benjamini-Hochberg correction for p-values adapted from statsmodels.

    :param pvals: an array of nominal p-values
    :param is_sorted: bool, whether the p-values are sorted
    :return: returns an array of corrected p-values aka FDRs/q-values
    """
    pvals = np.asarray(pvals)
    if not is_sorted:
        pvals_sortind = np.argsort(pvals)
        pvals_sorted = np.take(pvals, pvals_sortind)
    else:
        pvals_sorted = pvals
    ecdffactor = _ecdf(pvals_sorted)
    pvals_corrected_raw = pvals_sorted / ecdffactor
    pvals_corrected = np.minimum.accumulate(pvals_corrected_raw[::-1])[::-1]
    del pvals_corrected_raw
    pvals_corrected[pvals_corrected > 1] = 1
    if not is_sorted:
        pvals_corrected_ = np.empty_like(pvals_corrected)
        pvals_corrected_[pvals_sortind] = pvals_corrected
        del pvals_corrected
        return pvals_corrected_
    return pvals_corrected


def enrich(microbes, d_gmt, rank_means=None, rank_stds=None, universe=1000):
    """
    Perform enrichment analysis for a set of microbes against a
    microbe-set library using Fisher's exact test and z-score.

    :param microbes: a set of microbes as the input for MSEA analysis against this reference set
    :param d_gmt: a dictionary of microbe-sets representing the reference microbe-set library
    :param rank_means: (optional) the array of mean ranks from null distribution
    :param rank_stds: (optional) the array of standard deviations of ranks from null distribution
    :param universe: number of microbes used as the universe size for Fisher's exact test
    :return: returns a pandas.DataFrame object for the MSEA result table
    """
    microbes = set(microbes)
    n_terms = len(d_gmt)
    oddsratios = np.zeros(n_terms)
    pvals = np.ones(n_terms)
    shared = []
    i = 0
    for term, microbes_ref in d_gmt.items():
        oddsratio, pval = fisher_test(microbes, microbes_ref, universe)
        oddsratios[i] = oddsratio
        pvals[i] = pval
        shared.append(list(microbes & microbes_ref))
        i += 1

    qvals = multipletests_fdr_bh(pvals)
    if rank_means is not None and rank_stds is not None:
        p_ranks = np.argsort(pvals)
        z_scores = (p_ranks - rank_means) / rank_stds
        combined_scores = np.log(pvals) * z_scores
        res = pd.DataFrame({'term':list(d_gmt.keys()), 
         'oddsratio':oddsratios, 
         'pvalue':pvals, 
         'qvalue':qvals, 
         'zscore':z_scores, 
         'combined_score':combined_scores, 
         'shared':shared}).set_index('term').sort_values('combined_score', ascending=False)
    else:
        res = pd.DataFrame({'term':list(d_gmt.keys()), 
         'oddsratio':oddsratios, 
         'pvalue':pvals, 
         'qvalue':qvals, 
         'shared':shared}).set_index('term').sort_values('qvalue')
    res['n_shared'] = res['shared'].map(len)
    return res.loc[(res['n_shared'] > 0)]