# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\bmccs\Desktop\streamml2\streamml2\streamline\model_selection\models\regressors\GradientBoostingRegressorPredictiveModel.py
# Compiled at: 2019-01-22 19:47:05
# Size of source mod 2**32: 962 bytes
import sys, os
from ..AbstractRegressorPredictiveModel import AbstractRegressorPredictiveModel
from sklearn.ensemble import GradientBoostingRegressor

class GradientBoostingRegressorPredictiveModel(AbstractRegressorPredictiveModel):

    def __init__(self, X, y, gbr_params, nfolds=3, n_jobs=1, scoring=None, random_grid=False, n_iter=10, verbose=True):
        self._code = 'gbr'
        if verbose:
            print('Constructed GradientBoostingRegressor: ' + self._code)
        AbstractRegressorPredictiveModel.__init__(self, 'regressor', X, y, gbr_params, nfolds, n_jobs, scoring, random_grid, n_iter, verbose)
        self._model = self.constructRegressor(GradientBoostingRegressor(), self._random_grid)

    def execute(self):
        pass