# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/general/benchmark_classification.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 1011 bytes
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import scipy.sparse as sp

def evaluate_oracle_F1(probs, Y_real):
    all_labels = []
    y_test = [[] for _ in range(Y_real.shape[0])]
    cy = sp.csr_matrix(Y_real).tocoo()
    for i, b in zip(cy.row, cy.col):
        y_test[i].append(b)

    top_k_list = [len(l) for l in y_test]
    assert Y_real.shape[0] == len(top_k_list)
    predictions = []
    for i, k in enumerate(top_k_list):
        probs_ = probs[i, :]
        a = np.zeros(probs.shape[1])
        labels_tmp = probs_.argsort()[-k:]
        a[labels_tmp] = 1
        predictions.append(a)

    predictions = np.matrix(predictions)
    micro = f1_score(Y_real, predictions, average='micro')
    macro = f1_score(Y_real, predictions, average='macro')
    return (
     micro, macro)