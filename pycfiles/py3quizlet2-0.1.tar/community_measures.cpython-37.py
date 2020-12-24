# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/community_detection/community_measures.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 1304 bytes
import numpy as np
from sklearn.metrics import silhouette_score
from itertools import product

def modularity(G, communities, weight='weight'):
    communities = list(communities.values())
    multigraph = G.is_multigraph()
    directed = G.is_directed()
    m = G.size(weight=weight)
    if directed:
        out_degree = dict(G.out_degree(weight=weight))
        in_degree = dict(G.in_degree(weight=weight))
        norm = 1 / m
    else:
        out_degree = dict(G.degree(weight=weight))
        in_degree = out_degree
        norm = 1 / (2 * m)

    def val(u, v):
        try:
            if multigraph:
                w = sum((d.get(weight, 1) for k, d in G[u][v].items()))
            else:
                w = G[u][v].get(weight, 1)
        except KeyError:
            w = 0

        if u == v:
            if not directed:
                w *= 2
        return w - in_degree[u] * out_degree[v] * norm

    Q = np.sum((val(u, v) for c in communities for u, v in product(c, repeat=2)))
    return Q * norm


def size_distribution(network_partition):
    return np.array([len(x) for x in network_partition.values()])


def number_of_communities(network_partition):
    return len(network_partition)