# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\bmccs\Desktop\streamml2\streamml2\streamline\model_selection\models\regressors\LassoLeastAngleRegressorPredictiveModel.py
# Compiled at: 2019-01-22 20:18:16
# Size of source mod 2**32: 933 bytes
import sys, os
from ..AbstractRegressorPredictiveModel import AbstractRegressorPredictiveModel
from sklearn.linear_model import LassoLars

class LassoLeastAngleRegressorPredictiveModel(AbstractRegressorPredictiveModel):

    def __init__(self, X, y, lasso_lar_params, nfolds=3, n_jobs=1, scoring=None, random_grid=False, n_iter=10, verbose=True):
        self._code = 'lasso_lar'
        if verbose:
            print('Constructed LassoLars: ' + self._code)
        AbstractRegressorPredictiveModel.__init__(self, 'regressor', X, y, lasso_lar_params, nfolds, n_jobs, scoring, random_grid, n_iter, verbose)
        self._model = self.constructRegressor(LassoLars(), self._random_grid)

    def execute(self):
        pass