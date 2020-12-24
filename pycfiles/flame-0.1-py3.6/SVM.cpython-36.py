# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/stats/SVM.py
# Compiled at: 2018-06-21 06:48:46
# Size of source mod 2**32: 5384 bytes
from flame.stats.base_model import BaseEstimator
from flame.stats.base_model import getCrossVal
from flame.stats.scale import scale, center
from flame.stats.model_validation import CF_QuanVal
from sklearn import svm
from nonconformist.base import ClassifierAdapter, RegressorAdapter
from nonconformist.acp import AggregatedCp
from nonconformist.acp import BootstrapSampler
from nonconformist.icp import IcpClassifier, IcpRegressor
from nonconformist.nc import ClassifierNc, MarginErrFunc, RegressorNc
from sklearn.neighbors import KNeighborsRegressor
from nonconformist.nc import AbsErrorErrFunc, RegressorNormalizer

class SVM(BaseEstimator):

    def __init__(self, X, Y, parameters):
        super(SVM, self).__init__(X, Y, parameters)
        self.estimator_parameters = parameters['SVM_parameters']
        self.tune = parameters['tune']
        self.tune_parameters = parameters['SVM_optimize']
        if self.quantitative:
            self.name = 'SVM-R'
            self.estimator_parameters.pop('class_weight', None)
            self.estimator_parameters.pop('probability', None)
            self.estimator_parameters.pop('decision_function_shape', None)
            self.estimator_parameters.pop('random_state', None)
            self.tune_parameters.pop('class_weight', None)
            self.tune_parameters.pop('random_state', None)
        else:
            self.estimator_parameters.pop('epsilon', None)
            self.name = 'SVM-C'

    def build(self):
        """Build a new SVM model with the X and Y numpy matrices"""
        if self.failed:
            return False
        else:
            X = self.X.copy()
            Y = self.Y.copy()
            if self.autoscale:
                X, self.mux = center(X)
                X, self.wgx = scale(X, self.autoscale)
            results = []
            results.append(('nobj', 'number of objects', self.nobj))
            results.append(('nvarx', 'number of predictor variables', self.nvarx))
            if self.cv:
                self.cv = getCrossVal(self.cv, 46, self.n, self.p)
            if self.tune:
                if self.quantitative:
                    self.optimize(X, Y, svm.SVR(), self.tune_parameters)
                    results.append(('model', 'model type', 'SVM quantitative (optimized)'))
                else:
                    self.optimize(X, Y, svm.SVC(probability=True), self.tune_parameters)
                    results.append(('model', 'model type', 'SVM qualitative (optimized)'))
            else:
                if self.quantitative:
                    print('Building Quantitative SVM-R model')
                    self.estimator = (svm.SVR)(**self.estimator_parameters)
                    results.append(('model', 'model type', 'SVM quantitative'))
                else:
                    print('Building Qualitative SVM-C')
                    self.estimator = (svm.SVC)(**self.estimator_parameters)
                    results.append(('model', 'model type', 'SVM qualitative'))
                if self.conformal:
                    if self.quantitative:
                        underlying_model = RegressorAdapter(self.estimator)
                        normalizing_model = RegressorAdapter(KNeighborsRegressor(n_neighbors=1))
                        normalizing_model = RegressorAdapter(self.estimator)
                        normalizer = RegressorNormalizer(underlying_model, normalizing_model, AbsErrorErrFunc())
                        nc = RegressorNc(underlying_model, AbsErrorErrFunc(), normalizer)
                        self.conformal_pred = AggregatedCp(IcpRegressor(nc), BootstrapSampler())
                        self.conformal_pred.fit(X, Y)
                        results.append(('model', 'model type', 'conformal SVM quantitative'))
                    else:
                        self.conformal_pred = AggregatedCp(IcpClassifier(ClassifierNc(ClassifierAdapter(self.estimator), MarginErrFunc())), BootstrapSampler())
                        self.conformal_pred.fit(X, Y)
                        results.append(('model', 'model type', 'conformal SVM qualitative'))
                self.estimator.fit(X, Y)
            return (
             True, results)