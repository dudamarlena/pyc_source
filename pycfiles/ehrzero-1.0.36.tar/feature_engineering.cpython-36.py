# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ishanu/.local/lib/python3.6/site-packages/ehrzero/feature_engineering.py
# Compiled at: 2019-04-24 21:51:54
# Size of source mod 2**32: 2115 bytes
import numpy as np, pandas as pd, itertools
from sklearn.metrics import roc_auc_score, roc_curve, auc

def augment_agg(X):
    mean = np.array(X.mean(axis=1)).reshape(X.shape[0], 1)
    std = np.array(X.std(axis=1)).reshape(X.shape[0], 1)
    rang = np.array(X.max(axis=1) - X.min(axis=1)).reshape(X.shape[0], 1)
    X = np.append(X, mean, 1)
    X = np.append(X, std, 1)
    X = np.append(X, rang, 1)
    return X


def longest_one_streak(lst):
    return max(sum(1 for x in l if x == 1) for n, l in itertools.groupby(lst))


def optimal_cutoff(labels, preds):
    fpr, tpr, cutoff = roc_curve(labels, preds)
    roc_auc = auc(fpr, tpr)
    i = np.arange(len(tpr))
    roc = pd.DataFrame({'fpr':pd.Series(fpr, index=i),  'tpr':pd.Series(tpr, index=i),  '1-fpr':pd.Series(1 - fpr, index=i),  'tf':pd.Series(tpr - (1 - fpr), index=i),  'thresholds':pd.Series(cutoff, index=i)})
    return float(roc.ix[(roc.tf - 0).abs().argsort()[:1]]['thresholds'])


def get_dynamics(VALUES, TEST_SEQ_LENGTH):
    first_half = pd.Series([np.mean(i[:int(TEST_SEQ_LENGTH / 2)]) for i in VALUES])
    second_half = pd.Series([np.mean(i[int(TEST_SEQ_LENGTH / 2):TEST_SEQ_LENGTH]) for i in VALUES])
    dynamics = (second_half / first_half).fillna(0)
    dynamics[np.isinf(dynamics)] = 0
    return dynamics


def get_max_streak_length(arr, x):
    count = 0
    result = 0
    for i in arr:
        if i == x:
            count += 1
        else:
            count = 0
        result = max(result, count)

    return result