# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/reduction/base.py
# Compiled at: 2019-10-11 04:29:10
# Size of source mod 2**32: 1393 bytes
from abc import ABC, abstractmethod

class HubnessReduction(ABC):
    __doc__ = ' Base class for hubness reduction. '

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def fit(self, neigh_dist, neigh_ind, X, assume_sorted, *args, **kwargs):
        pass

    @abstractmethod
    def transform(self, neigh_dist, neigh_ind, X, assume_sorted, return_distance=True):
        pass

    def fit_transform(self, neigh_dist, neigh_ind, X, assume_sorted=True, return_distance=True, *args, **kwargs):
        """ Equivalent to call .fit().transform() """
        (self.fit)(neigh_dist, neigh_ind, X, assume_sorted, *args, **kwargs)
        return self.transform(neigh_dist, neigh_ind, X, assume_sorted, return_distance)


class NoHubnessReduction(HubnessReduction):
    __doc__ = ' Compatibility class for neighbor search without hubness reduction. '

    def __init__(self, **kwargs):
        (super().__init__)(**kwargs)

    def fit(self, *args, **kwargs):
        pass

    def transform(self, neigh_dist, neigh_ind, X, assume_sorted=True, return_distance=True, *args, **kwargs):
        """ Equivalent to call .fit().transform() """
        if return_distance:
            return (
             neigh_dist, neigh_ind)
        return neigh_ind