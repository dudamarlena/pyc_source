# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/reduction/shared_neighbors.py
# Compiled at: 2019-08-29 04:04:58
# Size of source mod 2**32: 1072 bytes
from __future__ import annotations
from sklearn.utils.validation import check_is_fitted
from .base import HubnessReduction

class SharedNearestNeighbors(HubnessReduction):
    __doc__ = ' Hubness reduction with Shared Nearest Neighbors (snn). '

    def __init__(self):
        super().__init__()

    def fit(self, neigh_dist, neigh_ind, X=None, *args, **kwargs) -> 'SharedNearestNeighbors':
        raise NotImplementedError('SNN is not yet implemented.')

    def transform(self, neigh_dist, neigh_ind, X=None, *args, **kwargs):
        check_is_fitted(self, 'neigh_dist_train_')


class SimhubIn(HubnessReduction):
    __doc__ = ' Hubness reduction with unsupervised Simhub (simhubin). '

    def __init__(self):
        super().__init__()

    def fit(self, neigh_dist, neigh_ind, X=None, *args, **kwargs) -> 'SimhubIn':
        raise NotImplementedError('Simhub is not yet implemented.')

    def transform(self, neigh_dist, neigh_ind, X=None, *args, **kwargs):
        check_is_fitted(self, 'neigh_dist_train_')