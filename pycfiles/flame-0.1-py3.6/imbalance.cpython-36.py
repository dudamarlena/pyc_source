# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/stats/imbalance.py
# Compiled at: 2018-06-21 06:48:46
# Size of source mod 2**32: 1747 bytes
import pandas as pd, numpy as np

def simple_subsampling(X, Y, random_seed):
    """
    Simple subsampling, adjusts the number of negative samples to the positive one
    """
    frame = pd.DataFrame(X)
    frame['act'] = Y
    positives = frame[(frame['act'] == 1)]
    negatives = frame[(frame['act'] == 0)]
    neg_sub = negatives.sample(frac=(float(len(positives)) / len(negatives)),
      random_state=46)
    new = pd.concat([positives, neg_sub], axis=0)
    Y_s = new['act'].values
    new = new.drop(['act'], axis=1)
    X_s = new.values
    if Y_s.size == 0 or X_s.size == 0:
        raise ValueError('Error creating subsampled matrices')
    return (
     X_s, Y_s)


def run_imbalance(method, X, Y, random_seed=46):
    X_s = []
    Y_s = []
    if method == 'simple_subsampling':
        X_s, Y_s = simple_subsampling(X, Y, random_seed)
    else:
        raise ValueError('Imbalance data method not recognized')
    return (
     X_s, Y_s)