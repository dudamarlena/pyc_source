# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/aidanrocke/anaconda/envs/py3k/lib/python3.6/site-packages/deep_rectifiers/validation.py
# Compiled at: 2017-05-18 12:27:10
# Size of source mod 2**32: 2161 bytes
"""
Created on Thu May 18 17:25:19 2017

@author: aidanrocke
"""
from sklearn.metrics import log_loss
import numpy as np, xgboost as xgb

def accuracy(model, X, Y):
    yhat = model.predict(X)
    return (
     np.mean(np.round(yhat) == Y), log_loss(Y, yhat))


def cross_validate(model, train_X, train_Y, K, epochs):
    """This function performs K-fold cross-validation"""
    permutation = np.random.permutation(range(len(train_X)))
    train_X = train_X[permutation]
    train_Y = train_Y[permutation]
    cols = round(float(len(train_X)) / float(K))
    sample_indices = np.reshape(permutation[:K * cols], (K, cols))
    CV_results = np.zeros((K, 2))
    row_index = np.array(range(K))
    for i in range(K):
        I = row_index[(np.arange(K) != i)]
        rows = np.concatenate((sample_indices[I]), axis=0)
        model.fit((train_X[rows]), (train_Y[rows]), epochs=epochs, verbose=1)
        evaluation = model.evaluate((train_X[sample_indices[i]]), (train_Y[sample_indices[i]]), verbose=1)
        CV_results[i] = (
         evaluation[0], evaluation[1])

    return CV_results


def adversarial_validation(train_X, test_X):
    train_Y = np.zeros(len(train_X))
    test_Y = np.ones(len(test_X))
    X = np.concatenate((train_X, test_X))
    Y = np.concatenate((train_Y, test_Y))
    model = xgb.XGBClassifier()
    model.fit(X, Y.flatten())
    probs = model.predict(train_X)
    indices = [i[0] for i in sorted((enumerate(probs)), key=(lambda x: x[1]))]
    X, Y = train_X[indices], train_Y[indices]
    train_X, validate_X = X[1:int(len(indices) * 0.7)], X[int(len(indices) * 0.7):len(indices)]
    train_Y, validate_Y = Y[1:int(len(indices) * 0.7)], Y[int(len(indices) * 0.7):len(indices)]
    return (
     train_X, validate_X, train_Y, validate_Y)