# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/codes/flexible_clustering_tree/flexible_clustering_tree/string_matching.py
# Compiled at: 2019-10-28 15:40:24
# Size of source mod 2**32: 1650 bytes
from sklearn.base import BaseEstimator, ClusterMixin
from itertools import groupby
import numpy
from typing import List

class StringAggregation(BaseEstimator, ClusterMixin):
    __doc__ = 'Class to aggregate information by string'

    def __init__(self):
        pass

    def fit(self, X: List[str]):
        """run aggregation by string"""
        if not isinstance(X, list):
            raise Exception('StringAggregation has not list object. This class expects str of list object, but {} is given.'.format(type(X)))
        _StringAggregation__t_d_id2str = {d_id:_StringAggregation__str for d_id, _StringAggregation__str in enumerate(X)}
        labels_ = [None] * len(X)
        c_id = 0
        for _StringAggregation__str, g_obj in groupby(sorted((_StringAggregation__t_d_id2str.items()), key=(lambda t: t[1])), key=(lambda t: t[1])):
            for t in list(g_obj):
                labels_[t[0]] = c_id

            c_id += 1
        else:
            self.labels_ = labels_

        return self

    def fit_predict(self, X: List[str], y=None):
        self.fit(X)
        return self.labels_

    def get_params(self, deep=True):
        pass

    def set_params(self, **params):
        pass

    def __str__(self):
        return 'StringAggregation'


def test():
    matrix_obj_input = numpy.random.rand(100, 128)
    string_inputs = ['d'] * 10 + ['e'] * 10 + ['c'] * 10 + ['a'] * 10 + ['b'] * 10 + ['f'] * 50
    aggregation_obj = StringAggregation()
    aggregation_obj.fit(string_inputs)
    labels = aggregation_obj.fit_predict(string_inputs)
    assert len(labels) == len(string_inputs)


if __name__ == '__main__':
    test()