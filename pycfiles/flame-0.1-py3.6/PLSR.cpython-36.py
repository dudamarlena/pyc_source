# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/stats/PLSR.py
# Compiled at: 2018-06-21 06:50:39
# Size of source mod 2**32: 5562 bytes
from flame.stats.base_model import BaseEstimator
from flame.stats.base_model import getCrossVal
from flame.stats.scale import scale, center
from flame.stats.model_validation import CF_QuanVal
import copy
from sklearn.cross_decomposition import PLSCanonical, PLSRegression, CCA
from nonconformist.base import ClassifierAdapter, RegressorAdapter
from nonconformist.acp import AggregatedCp
from nonconformist.acp import BootstrapSampler
from nonconformist.icp import IcpClassifier, IcpRegressor
from nonconformist.nc import ClassifierNc, MarginErrFunc, RegressorNc
import numpy as np
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from nonconformist.nc import AbsErrorErrFunc, RegressorNormalizer

class PLS_r(PLSRegression):

    def predict(self, X, copy=True):
        results = super(PLS_r, self).predict(X, copy=True).ravel()
        return results


class PLSR(BaseEstimator):

    def __init__(self, X, Y, parameters):
        super(PLSR, self).__init__(X, Y, parameters)
        self.estimator_parameters = parameters['PLSR_parameters']
        self.tune = parameters['tune']
        self.tune_parameters = parameters['PLSR_optimize']
        self.name = 'PLSR'
        self.optimiz = self.estimator_parameters['optimize']
        self.estimator_parameters.pop('optimize')

    def build(self):
        if not self.quantitative:
            print('PLSR only applies to quantitative data')
            return (False, 'PLSR only applies to quantitative data')
        else:
            if self.failed:
                return (False, 'Error initiating model')
            else:
                X = self.X.copy()
                Y = self.Y.copy()
                if self.autoscale:
                    X, self.mux = center(X)
                    X, self.wgx = scale(X, self.autoscale)
                    print('autoscaling')
                results = []
                results.append(('nobj', 'number of objects', self.nobj))
                results.append(('nvarx', 'number of predictor variables', self.nvarx))
                if self.cv:
                    self.cv = getCrossVal(self.cv, 46, self.n, self.p)
                if self.tune:
                    if self.optimiz == 'auto':
                        super(PLSR, self).optimize(X, Y, PLS_r(**self.estimator_parameters), self.tune_parameters)
                    else:
                        if self.optimiz == 'manual':
                            self.optimize(X, Y, PLS_r(**self.estimator_parameters), self.tune_parameters)
                    results.append(('model', 'model type', 'PLSR quantitative (optimized)'))
                else:
                    print('Building  Quantitative PLSR')
                    self.estimator = PLS_r(**self.estimator_parameters)
                    results.append(('model', 'model type', 'PLSR quantitative'))
                if self.conformal:
                    underlying_model = RegressorAdapter(self.estimator)
                    normalizing_model = RegressorAdapter(KNeighborsRegressor(n_neighbors=1))
                    normalizing_model = RegressorAdapter(self.estimator)
                    normalizer = RegressorNormalizer(underlying_model, normalizing_model, AbsErrorErrFunc())
                    nc = RegressorNc(underlying_model, AbsErrorErrFunc(), normalizer)
                    self.conformal_pred = AggregatedCp(IcpRegressor(nc), BootstrapSampler())
                    self.conformal_pred.fit(X, Y)
                    results.append(('model', 'model type', 'conformal PLSR quantitative'))
            self.estimator.fit(X, Y)
            return (
             True, results)

    def optimize(self, X, Y, estimator, tune_parameters):
        """ optimizes a model using a grid search over a range of values for diverse parameters"""
        print('Optimizing PLSR algorithm')
        latent_variables = tune_parameters['n_components']
        r2 = 0
        estimator0 = ''
        list_latent = []
        for n_comp in latent_variables:
            r2_0 = 0
            (estimator.set_params)(**{'n_components': n_comp})
            y_pred = cross_val_predict(estimator, X, Y, cv=(self.cv), n_jobs=1)
            r2_0 = r2_score(Y, y_pred)
            if r2_0 >= r2:
                r2 = r2_0
                estimator0 = copy.copy(estimator)
            list_latent.append([n_comp, r2_0])

        print('r2 per latent variable')
        for el in list_latent:
            print('Number of latent variables: %s \nr2: %s\n' % (
             el[0], el[1]))

        self.estimator = estimator0
        self.estimator.fit(X, Y)
        print(self.estimator.get_params())