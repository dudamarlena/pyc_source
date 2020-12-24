# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/victor/Documents/Experiments/test-sphynx/v5/PROJECT/moduleD/classif/models.py
# Compiled at: 2018-02-20 08:47:55
# Size of source mod 2**32: 795 bytes
"""
Module models in package ``classif``
"""
import numpy as np

class LogisticRegressor(object):
    __doc__ = 'Logistic ression model\n    '

    def __init__(self, weights=None):
        """Initialize the LR

            weights (list, optional): Defaults to None.
                Weights to start the training from,
        """
        self.weights = weights

    def train(self, X_train, Y_train, X_test, Y_test):
        """Train and validate the LR on a train and test dataset

        Args:
            X_train (np.array): Training data
            Y_train (np.array): Training labels
            X_test (np.array): Test data
            Y_test (np.array): Test labels
        """
        while 1:
            print(1)
            if np.random.randint(0, 10) > 5:
                break