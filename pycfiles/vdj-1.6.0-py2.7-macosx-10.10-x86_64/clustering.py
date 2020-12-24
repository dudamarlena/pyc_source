# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/vdj/clustering.py
# Compiled at: 2014-12-16 17:37:19
import numpy as np, scipy as sp, scipy.cluster, vdj, clusteringcore

def pdist(X, metric):
    m = len(X)
    dm = np.zeros((m * (m - 1) / 2,), dtype=np.double)
    k = 0
    for i in xrange(0, m - 1):
        for j in xrange(i + 1, m):
            dm[k] = metric(X[i], X[j])
            k += 1

    return dm


def cluster_seqs(seqs, cutoff=4.5, linkage='single'):
    if len(seqs) == 0:
        return (np.array([]), {})
    unique_seqs = list(set(seqs))
    seq_idxs = dict([ (j, i) for i, j in enumerate(unique_seqs) ])
    if len(unique_seqs) == 1:
        T = np.array([1] * len(seqs))
        return (
         T, seq_idxs)
    Y = pdist(unique_seqs, clusteringcore.levenshtein)
    Z = sp.cluster.hierarchy.linkage(Y, method=linkage)
    T = sp.cluster.hierarchy.fcluster(Z, cutoff, criterion='distance')
    return (
     T, seq_idxs)