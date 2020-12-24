# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/utils.py
# Compiled at: 2018-03-18 23:36:04
import numpy as np
from itertools import combinations_with_replacement

def polynomial_features(X, degree):
    n_samples, n_features = np.shape(X)

    def index_combinations():
        combs = [ combinations_with_replacement(range(n_features), i) for i in range(0, degree + 1) ]
        flat_combs = [ item for sublist in combs for item in sublist ]
        return flat_combs

    combinations = index_combinations()
    n_output_features = len(combinations)
    X_new = np.empty((n_samples, n_output_features))
    for i, index_combs in enumerate(combinations):
        X_new[:, i] = np.prod(X[:, index_combs], axis=1)

    return X_new


def normalize(X, axis=-1, order=2):
    """ Normalize the dataset X """
    l2 = np.atleast_1d(np.linalg.norm(X, order, axis))
    l2[l2 == 0] = 1
    return X / np.expand_dims(l2, axis)