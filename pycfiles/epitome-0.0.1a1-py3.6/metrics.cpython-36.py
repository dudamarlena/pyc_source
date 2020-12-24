# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/epitome/metrics.py
# Compiled at: 2020-01-09 18:50:33
# Size of source mod 2**32: 2619 bytes
import sklearn.metrics, numpy as np, tensorflow as tf

def gini(actual, pred, sample_weight):
    df = tf.stack([actual, pred], axis=0)
    df = tf.gather(df, tf.argsort(pred, direction='DESCENDING'), axis=1)
    linsp = tf.divide(tf.range(1, df.shape[1] + 1), df.shape[1])
    linsp = tf.cast(linsp, tf.float32)
    totalPos = tf.math.reduce_sum(actual)
    cumPosFound = tf.math.cumsum(df[0])
    Lorentz = tf.divide(cumPosFound, totalPos)
    Gini = Lorentz - linsp
    return tf.reduce_sum(tf.boolean_mask(Gini, sample_weight)).numpy()


def gini_normalized(actual, pred, sample_weight=None):
    normalized_gini = gini(actual, pred, sample_weight) / gini(actual, actual, sample_weight)
    return normalized_gini


def get_performance(assaymap, preds, truth, sample_weight):
    if not preds.shape == truth.shape:
        raise AssertionError
    elif not preds.shape == sample_weight.shape:
        raise AssertionError
    inv_assaymap = {v:k for k, v in assaymap.items()}
    evaluated_assays = {}
    for j in range(preds.shape[1]):
        try:
            roc_score = sklearn.metrics.roc_auc_score((truth[:, j]), (preds[:, j]),
              sample_weight=(sample_weight[:, j]),
              average='macro')
        except ValueError:
            roc_score = np.NaN

        try:
            pr_score = sklearn.metrics.average_precision_score((truth[:, j]), (preds[:, j]),
              sample_weight=(sample_weight[:, j]))
        except ValueError:
            pr_score = np.NaN

        try:
            gini_score = gini_normalized((truth[:, j]), (preds[:, j]),
              sample_weight=(sample_weight[:, j]))
        except ValueError:
            gini_score = np.NaN

        evaluated_assays[inv_assaymap[(j + 1)]] = {'AUC':roc_score, 
         'auPRC':pr_score,  'GINI':gini_score}

    return evaluated_assays