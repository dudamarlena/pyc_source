# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sovereign/utils/weighted_clusters.py
# Compiled at: 2020-04-16 21:27:51
# Size of source mod 2**32: 833 bytes
from __future__ import division

def _round_to_n(sequence, n=100):
    """ Resolves issue when dividing by N results in a set of numbers that don't add up to N again

        E.g. 100 / 3 = 33
             33 * 3 = 99

        For the above example, this function returns [33, 33, 34]
     """
    if sum(sequence) != n:
        sequence[-1] = n - sum(sequence[:-1])
    return sequence


def _normalize_weights(sequence, n=100):
    total = sum(sequence)
    for item in sequence:
        (yield int(item / total * n))


def fit_weights(clusters, total_weight=100):
    weights = list(_normalize_weights([cluster['weight'] for cluster in clusters], n=total_weight))
    for cluster, newly_assigned_weight in zip(clusters, _round_to_n(weights, n=total_weight)):
        cluster['weight'] = newly_assigned_weight
    else:
        return clusters