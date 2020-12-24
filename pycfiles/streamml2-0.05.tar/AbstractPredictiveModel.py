# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bmc/Desktop/streamml/streamline/model_selection/AbstractPredictiveModel.py
# Compiled at: 2018-06-22 08:44:01
import sys, os, numpy as np
from streamml.utils.validator.model_validation import ModelValidation

class AbstractPredictiveModel:
    _model = None
    _grid = None
    _pipe = None
    _params = None
    _modelType = None
    _validator = None
    _validation_results = None
    _X = None
    _y = None
    _code = None
    _n_jobs = None
    _verbose = None

    def __init__(self, X, params, nfolds, n_jobs, verbose):
        if self._verbose:
            print 'Constructed AbstractPredictiveModel: ' + self._code
        assert isinstance(params, dict), 'params must be dict'
        self._X = X
        self._params = params
        self._nfolds = nfolds
        self._n_jobs = n_jobs
        self._verbose = verbose
        self._validator = ModelValidation()

    def validate(self):
        pass

    def getCode(self):
        return self._code

    def getValidationResults(self):
        if self._verbose:
            print 'Returning ' + self._code + ' validation results'
        return self._validation_results

    def getBestEstimator(self):
        if self._verbose:
            print 'Returning ' + self._code + ' best estiminator'
        return self._model