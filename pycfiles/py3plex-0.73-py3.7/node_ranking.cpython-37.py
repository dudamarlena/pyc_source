# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/node_ranking/node_ranking.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 5317 bytes
import numpy as np, networkx as nx
import scipy.sparse as sp
from itertools import product

def stochastic_normalization(matrix):
    matrix = matrix.tolil()
    try:
        matrix.setdiag(0)
    except TypeError:
        matrix.setdiag(np.zeros(matrix.shape[0]))

    matrix = matrix.tocsr()
    d = matrix.sum(axis=1).getA1()
    nzs = np.where(d > 0)
    k = 1 / d[nzs]
    matrix = sp.diags(k, 0).tocsc().dot(matrix).transpose()
    return matrix


def stochastic_normalization_hin(matrix):
    matrix = matrix.tolil()
    try:
        matrix.setdiag(0)
    except TypeError:
        matrix.setdiag(np.zeros(matrix.shape[0]))

    matrix = matrix.tocsr()
    d = matrix.sum(axis=1).getA1()
    nzs = np.where(d > 0)
    d[nzs] = 1 / d[nzs]
    matrix = sp.diags(d, 0).tocsc().dot(matrix).transpose()
    return matrix


def modularity(G, communities, weight='weight'):
    return 1


def page_rank_kernel(index_row):
    pr = sparse_page_rank(G, [index_row], epsilon=1e-06,
      max_steps=100000,
      damping=damping_hyper,
      spread_step=spread_step_hyper,
      spread_percent=spread_percent_hyper,
      try_shrink=True)
    norm = np.linalg.norm(pr, 2)
    if norm > 0:
        pr = pr / np.linalg.norm(pr, 2)
        return (index_row, pr)
    return (index_row, np.zeros(graph.shape[1]))


def sparse_page_rank(matrix, start_nodes, epsilon=1e-06, max_steps=100000, damping=0.5, spread_step=10, spread_percent=0.3, try_shrink=False):
    if not len(start_nodes) > 0:
        raise AssertionError
    else:
        size = matrix.shape[0]
        if start_nodes is None:
            start_nodes = range(size)
            nz = size
        else:
            nz = len(start_nodes)
        start_vec = np.zeros((size, 1))
        start_vec[start_nodes] = 1
        start_rank = start_vec / len(start_nodes)
        rank_vec = start_vec / len(start_nodes)
        shrink = False
        which = np.zeros(0)
        if try_shrink:
            v = start_vec / len(start_nodes)
            steps = 0
            while nz < size * spread_percent and steps < spread_step:
                steps += 1
                v += matrix.dot(v)
                nz_new = np.count_nonzero(v)
                if nz_new == nz:
                    shrink = True
                    break
                nz = nz_new

            rr = np.arange(matrix.shape[0])
            which = (v[rr] > 0).reshape(size)
            if shrink:
                start_rank = start_rank[which]
                rank_vec = rank_vec[which]
                matrix = matrix[:, which][which, :]
        diff = np.Inf
        steps = 0
        while diff > epsilon and steps < max_steps:
            steps += 1
            new_rank = matrix.dot(rank_vec)
            rank_sum = np.sum(new_rank)
            if rank_sum < 0.999999999:
                new_rank += start_rank * (1 - rank_sum)
            new_rank = damping * new_rank + (1 - damping) * start_rank
            new_diff = np.linalg.norm(rank_vec - new_rank, 1)
            diff = new_diff
            rank_vec = new_rank

        if try_shrink and shrink:
            ret = np.zeros(size)
            rank_vec = rank_vec.T[0]
            ret[which] = rank_vec
            ret[start_nodes] = 0
            return ret.flatten()
    rank_vec[start_nodes] = 0
    return rank_vec.flatten()


def hubs_and_authorities(graph):
    return nx.hits_scipy(graph)


def hub_matrix(graph):
    return nx.hub_matrix(graph)


def authority_matrix(graph):
    return nx.authority_matrix(graph)