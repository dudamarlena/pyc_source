# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/stats/GNB.py
# Compiled at: 2018-06-21 06:48:46
# Size of source mod 2**32: 3120 bytes
from sklearn.naive_bayes import GaussianNB
from flame.stats.base_model import BaseEstimator
from flame.stats.base_model import getCrossVal
from flame.stats.scale import scale, center
from flame.stats.model_validation import CF_QuanVal
from nonconformist.base import ClassifierAdapter, RegressorAdapter
from nonconformist.acp import AggregatedCp
from nonconformist.acp import BootstrapSampler
from nonconformist.icp import IcpClassifier, IcpRegressor
from nonconformist.nc import ClassifierNc, MarginErrFunc, RegressorNc

class GNB(BaseEstimator):

    def __init__(self, X, Y, parameters):
        super(GNB, self).__init__(X, Y, parameters)
        self.estimator_parameters = parameters['GNB_parameters']
        if self.quantitative:
            return
        self.name = 'GNB-Classifier'

    def build(self):
        """Build a new qualitative GNB model with the X and Y numpy matrices"""
        if self.failed:
            return (False, 'Error initiating model')
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
            if self.quantitative:
                print('GNB only applies to qualitative data')
                return (False, 'GNB only applies to qualitative data')
            print('Building GaussianNB model')
            print(self.estimator_parameters)
            self.estimator = GaussianNB(**self.estimator_parameters)
            results.append(('model', 'model type', 'GNB qualitative'))
            if self.conformal:
                self.conformal_pred = AggregatedCp(IcpClassifier(ClassifierNc(ClassifierAdapter(self.estimator), MarginErrFunc())), BootstrapSampler())
                self.conformal_pred.fit(X, Y)
                results.append(('model', 'model type', 'conformal GNB qualitative'))
            self.estimator.fit(X, Y)
            return (True, results)