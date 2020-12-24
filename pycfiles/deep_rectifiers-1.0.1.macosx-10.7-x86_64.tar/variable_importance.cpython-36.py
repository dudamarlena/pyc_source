# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/aidanrocke/anaconda/envs/py3k/lib/python3.6/site-packages/deep_rectifiers/variable_importance.py
# Compiled at: 2017-06-21 11:07:48
# Size of source mod 2**32: 921 bytes
"""
Created on Fri May 19 23:26:05 2017

@author: aidanrocke
"""
import numpy as np

def variable_importance(trained_model, validate_X, validate_Y):
    """
        A method for calculating variable importance by introducing Gaussian noise. 

        trained_model

    """
    yhat = np.round(trained_model.predict(validate_X))
    boolean = np.array(yhat == validate_Y)
    X = validate_X[boolean[:, 0]]
    Y = validate_Y[boolean[:, 0]]
    N, M = np.shape(validate_X)
    importance = np.zeros(M)
    for i in range(M):
        mu = np.mean(X[:, i])
        sigma = np.std(X[:, i])
        Xhat = X
        Xhat[:, i] = np.random.normal(mu, sigma)
        importance[i] = 1 - np.mean(np.round(trained_model.predict(Xhat)) == Y)

    return importance