# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gleipnir/utilities/knn_entropy.py
# Compiled at: 2019-04-26 20:35:17
# Size of source mod 2**32: 5595 bytes
"""Functions to compute entropy and mutual information using k-nearest neighbor estimators.
Adapted from: https://github.com/blakeaw/Python-knn-entropy/blob/master/knn_entropy.py
"""
import numpy as np
from scipy.special import gamma, psi
from scipy.spatial.distance import cdist

def k_nearest_neighbors(X, k=1):
    """Determine the k-nearest neighbors of each point within a random variate sample.
    This function uses Euclidean distance as the distance metric for
    determining the nearest neighbors.
    Args:
        X (numpy.array): A random variate sample.
        k (int): The number of nearest neighbors to find. Defaults to 1.

    Returns:
        dict: A dictionary keyed to the sample indices of points from the input
            random variate sample. Each element is a sorted list of the
            k-nearest neighbors of the form
            [[index, distance], [index, distance]...]

    """
    nX = len(X)
    knn = {key:[] for key in range(nX)}
    X = np.reshape(X, (nX, -1))
    dists_arr = cdist(X, X)
    distances = [[i, j, dists_arr[(i, j)]] for i in range(nX - 1) for j in range(i + 1, nX)]
    distances.sort(key=(lambda x: x[2]))
    for d in distances:
        i = d[0]
        j = d[1]
        dist = d[2]
        if len(knn[i]) < k:
            knn[i].append([j, dist])
        if len(knn[j]) < k:
            knn[j].append([i, dist])

    return knn


def kth_nearest_neighbor_distances(X, k=1):
    nX = len(X)
    X = np.reshape(X, (nX, -1))
    dists_arr = cdist(X, X)
    dists_arr.sort()
    return [dists_arr[i][k] for i in range(nX)]


def shannon_entropy(X, k=1, kth_dists=None):
    r_k = kth_dists
    if kth_dists is None:
        r_k = kth_nearest_neighbor_distances(X, k=k)
    n = len(X)
    d = 1
    if len(X.shape) == 2:
        d = X.shape[1]
    v_unit_ball = np.pi ** (0.5 * d) / gamma(0.5 * d + 1.0)
    lr_k = np.log(r_k)
    H = psi(n) - psi(k) + np.log(v_unit_ball) + np.float(d) / np.float(n) * lr_k.sum()
    return H


def shannon_entropy_pc(X, k=1, kth_dists=None):
    r_k = kth_dists
    if kth_dists is None:
        r_k = np.array(kth_nearest_neighbor_distances(X, k=k))
    n = len(X)
    d = 1
    if len(X.shape) == 2:
        d = X.shape[1]
    v_unit_ball = np.pi ** (0.5 * d) / gamma(0.5 * d + 1.0)
    p_k_hat = k / (n - 1.0) * (1.0 / v_unit_ball) * (1.0 / r_k ** d)
    log_p_k_hat = np.log(p_k_hat)
    h_k_hat = log_p_k_hat.sum() / (-1.0 * n)
    return h_k_hat


def mutual_information(var_tuple, k=2):
    nvar = len(var_tuple)
    var_tuple = tuple(var_tuple[i].reshape(len(var_tuple[i]), -1) for i in range(nvar))
    Hx = [shannon_entropy((var_tuple[i]), k=k) for i in range(nvar)]
    Hx = np.array(Hx)
    Hxtot = Hx.sum()
    joint = np.hstack(var_tuple)
    Hjoint = shannon_entropy(joint, k=k)
    MI = Hxtot - Hjoint
    if MI < 0.0:
        MI = 0.0
    return MI


def conditional_mutual_information(var_tuple, cond_tuple, k=2):
    nvar = len(var_tuple)
    ncon = len(cond_tuple)
    var_tuple = tuple(var_tuple[i].reshape(len(var_tuple[i]), -1) for i in range(nvar))
    cond_tuple = tuple(cond_tuple[i].reshape(len(cond_tuple[i]), -1) for i in range(ncon))
    Hxz = [shannon_entropy((np.hstack(var_tuple[i] + cond_tuple)), k=k) for i in range(nvar)]
    Hxz = np.array(Hxz)
    jtup = var_tuple + cond_tuple
    joint = np.hstack(jtup)
    Hj = shannon_entropy(joint, k=k)
    Hz = 0.0
    if len(cond_tuple) > 1:
        joint = np.hstack(cond_tuple)
        Hz = shannon_entropy(joint, k=k)
    else:
        Hz = shannon_entropy((cond_tuple[0]), k=k)
    Hxzsum = Hxz.sum()
    MIc = Hxzsum - Hj - Hz
    if MIc < 0.0:
        MIc = 0.0
    return MIc