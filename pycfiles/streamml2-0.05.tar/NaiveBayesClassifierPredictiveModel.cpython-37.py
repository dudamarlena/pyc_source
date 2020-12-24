# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\bmccs\Desktop\streamml2\streamml2\streamline\model_selection\models\classifiers\NaiveBayesClassifierPredictiveModel.py
# Compiled at: 2019-01-22 20:20:30
# Size of source mod 2**32: 799 bytes
import sys, os
from ..AbstractClassifierPredictiveModel import AbstractClassifierPredictiveModel
from sklearn.naive_bayes import GaussianNB

class NaiveBayesClassifierPredictiveModel(AbstractClassifierPredictiveModel):

    def __init__(self, X, y, nbc_params, nfolds=3, n_jobs=1, scoring=None, random_grid=False, n_iter=10, verbose=True):
        self._code = 'nbc'
        if verbose:
            print('Constructed NaiveBayesClassifierPredictiveModel: ' + self._code)
        AbstractClassifierPredictiveModel.__init__(self, 'classifier', X, y, nbc_params, nfolds, n_jobs, scoring, random_grid, n_iter, verbose)
        self._model = self.constructClassifier(GaussianNB(), self._random_grid)