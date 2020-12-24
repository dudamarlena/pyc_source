# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bmc/Desktop/streamml/streamline/model_selection/models/regressors/RandomForestRegressorPredictiveModel.py
# Compiled at: 2018-06-22 08:44:01
import sys, os
from streamline.model_selection.models.AbstractRegressorPredictiveModel import AbstractRegressorPredictiveModel
from sklearn.ensemble import RandomForestRegressor

class RandomForestRegressorPredictiveModel(AbstractRegressorPredictiveModel):

    def __init__(self, X, y, rfr_params, nfolds=3, n_jobs=1, scoring=None, verbose=True):
        self._code = 'rfr'
        if verbose:
            print 'Constructed RandomForestRegressorPredictiveModel: ' + self._code
        AbstractRegressorPredictiveModel.__init__(self, 'regressor', X, y, rfr_params, nfolds, n_jobs, scoring, verbose)
        self._model = self.constructRegressor(RandomForestRegressor())

    def execute(self):
        pass