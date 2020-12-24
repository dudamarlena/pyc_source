# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bmc/Desktop/streamml/streamline/model_selection/models/regressors/MultilayerPerceptronRegressorPredictiveModel.py
# Compiled at: 2018-06-22 11:37:25
import sys, os
from streamline.model_selection.models.AbstractRegressorPredictiveModel import AbstractRegressorPredictiveModel
from sklearn.neural_network import MLPRegressor

class MultilayerPerceptronRegressorPredictiveModel(AbstractRegressorPredictiveModel):

    def __init__(self, X, y, mlpr_params, nfolds=3, n_jobs=1, scoring=None, verbose=True):
        self._code = 'mlpr'
        if verbose:
            print 'Constructed MultilayerPerceptronRegressor: ' + self._code
        AbstractRegressorPredictiveModel.__init__(self, 'regressor', X, y, mlpr_params, nfolds, n_jobs, scoring, verbose)
        self._model = self.constructRegressor(MLPRegressor())

    def execute(self):
        pass