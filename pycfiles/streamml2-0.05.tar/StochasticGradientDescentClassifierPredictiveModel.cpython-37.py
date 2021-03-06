# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\bmccs\Desktop\streamml2\streamml2\streamline\model_selection\models\classifiers\StochasticGradientDescentClassifierPredictiveModel.py
# Compiled at: 2019-01-22 20:20:24
# Size of source mod 2**32: 838 bytes
import sys, os
from ..AbstractClassifierPredictiveModel import AbstractClassifierPredictiveModel
from sklearn.linear_model import SGDClassifier

class StochasticGradientDescentClassifierPredictiveModel(AbstractClassifierPredictiveModel):

    def __init__(self, X, y, sgdc_params, nfolds=3, n_jobs=1, scoring=None, random_grid=False, n_iter=10, verbose=True):
        self._code = 'sgdc'
        if verbose:
            print('Constructed StochasticGradientDescentClassifierPredictiveModel: ' + self._code)
        AbstractClassifierPredictiveModel.__init__(self, 'classifier', X, y, sgdc_params, nfolds, n_jobs, scoring, random_grid, n_iter, verbose)
        self._model = self.constructClassifier(SGDClassifier(), self._random_grid)