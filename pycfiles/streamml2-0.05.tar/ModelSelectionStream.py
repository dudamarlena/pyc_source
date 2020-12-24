# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bmc/Desktop/streamml/streamline/model_selection/flow/ModelSelectionStream.py
# Compiled at: 2018-06-22 11:37:48
import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RepeatedStratifiedKFold
import matplotlib.pyplot as plt, sys, os
from collections import defaultdict
from streamml.streamline.model_selection.models.regressors.LinearRegressorPredictiveModel import LinearRegressorPredictiveModel
from streamml.streamline.model_selection.models.regressors.SupportVectorRegressorPredictiveModel import SupportVectorRegressorPredictiveModel
from streamml.streamline.model_selection.models.regressors.RidgeRegressorPredictiveModel import RidgeRegressorPredictiveModel
from streamml.streamline.model_selection.models.regressors.LassoRegressorPredictiveModel import LassoRegressorPredictiveModel
from streamml.streamline.model_selection.models.regressors.ElasticNetRegressorPredictiveModel import ElasticNetRegressorPredictiveModel
from streamml.streamline.model_selection.models.regressors.KNNRegressorPredictiveModel import KNNRegressorPredictiveModel
from streamml.streamline.model_selection.models.regressors.RandomForestRegressorPredictiveModel import RandomForestRegressorPredictiveModel
from streamml.streamline.model_selection.models.regressors.AdaptiveBoostingRegressorPredictiveModel import AdaptiveBoostingRegressorPredictiveModel
from streamml.streamline.model_selection.models.regressors.MultilayerPerceptronRegressorPredictiveModel import MultilayerPerceptronRegressorPredictiveModel

class ModelSelectionStream:
    _X = None
    _y = None
    _test_size = None
    _nfolds = None
    _n_jobs = None
    _verbose = None
    _scoring = None
    _metrics = None
    _test_size = None
    _wrapper_models = None
    _bestEstimators = {}
    _bestEstimator = None
    _regressors_results = None
    _classifiers_results = None

    def __init__(self, X, y):
        assert isinstance(X, pd.DataFrame), 'X was not a pandas DataFrame'
        assert any([isinstance(y, pd.DataFrame), isinstance(y, pd.Series)]), 'y was not a pandas DataFrame or Series'
        self._X = X
        self._y = y

    def getBestEstimators(self):
        return self._bestEstimators

    def getBestEstimator(self):
        return self._bestEstiminator

    def determineBestEstimators(self, models):
        if self._verbose:
            print '**************************************************'
            print 'Determining Best Estimators.'
            print '**************************************************'
        for model in models:
            self._bestEstimators[model.getCode()] = model.getBestEstimator()
            if self._verbose:
                print (
                 model.getCode(), model.getBestEstimator().get_params())

        return self._bestEstimators

    def handleRegressors(self, Xtest, ytest, metrics, wrapper_models, cut):
        self._regressors_results = defaultdict(list)
        rskf = RepeatedStratifiedKFold(n_splits=10, n_repeats=10, random_state=36851234)
        butch = self._y.copy()
        butch[butch < cut] = 1
        butch[butch >= cut] = 0
        averages = defaultdict(list)
        for train_index, test_index in rskf.split(self._X, butch):
            if self._verbose:
                print (
                 'TRAIN:', train_index, 'TEST:', test_index)
            self._X_train, self._X_test = self._X.iloc[train_index, :], self._X.iloc[test_index, :]
            self._y_train, self._y_test = self._y.iloc[train_index], self._y.iloc[test_index]
            for model in wrapper_models:
                self._regressors_results[model.getCode()].append(model.validate(self._X_test, self._y_test, metrics))

        for k, v in self._regressors_results.items():
            example_df = pd.DataFrame(self._regressors_results[k])
            mean = example_df.mean()
            self._regressors_results[k] = mean

        if self._verbose:
            print '**************************************************'
            print 'Regressor Performance Sheet'
            print '**************************************************'
            df_results = pd.DataFrame(self._regressors_results)
            print df_results
            df_results.plot(title='Errors by Model')
            plt.show()
        return self._regressors_results

    def handleClassifiers(self, Xtest, ytest, metrics, wrapper_models):
        if self._verbose:
            print '**************************************************'
            print 'Classifier Performance Sheet'
            print '**************************************************'

    def handleModelSelection(self, regressors, metrics, Xtest, ytest, wrapper_models, cut=None):
        if regressors:
            assert cut != None, 'you must select a cut point for your stratified folds to equally distribute your critical points'
            self._bestEstimator = self.handleRegressors(Xtest, ytest, metrics, wrapper_models, cut)
        else:
            assert 1 == 2, 'Handling Classification is not yet supported.'
            self._bestEstimator = self.handleClassifiers(Xtest, ytest, metrics, wrapper_models)
        return self._bestEstimator

    def flow(self, models_to_flow=[], params=None, test_size=0.2, nfolds=3, nrepeats=3, pos_split=1, n_jobs=1, metrics=[], verbose=False, regressors=True, cut=None):
        assert isinstance(nfolds, int), 'nfolds must be integer'
        assert isinstance(nrepeats, int), 'nrepeats must be integer'
        assert isinstance(n_jobs, int), 'n_jobs must be integer'
        assert isinstance(verbose, bool), 'verbosem ust be bool'
        assert isinstance(pos_split, int), 'pos_split must be integer'
        assert isinstance(params, dict), 'params must be a dict'
        assert isinstance(test_size, float), 'test_size must be a float'
        assert isinstance(metrics, list), 'model scoring must be a list'
        assert isinstance(regressors, bool), 'regressor must be bool'
        self._nfolds = nfolds
        self._nrepeats = nrepeats
        self._n_jobs = n_jobs
        self._verbose = verbose
        self._pos_split = pos_split
        self._allParams = params
        self._metrics = metrics
        self._test_size = test_size
        self._regressors = regressors
        self._cut = cut
        stringbuilder = ''
        for thing in models_to_flow:
            stringbuilder += thing
            stringbuilder += ' --> '

        if self._verbose:
            print '**************************************************'
            print 'Model Selection Streamline: ' + stringbuilder[:-5]
            print '**************************************************'

        def linearRegression():
            self._lr_params = {}
            for k, v in self._allParams.items():
                if 'lr' in k:
                    self._lr_params[k] = v

            model = LinearRegressorPredictiveModel(self._X_train, self._y_train, self._lr_params, self._nfolds, self._n_jobs, self._verbose)
            return model

        def supportVectorRegression():
            self._svr_params = {}
            for k, v in self._allParams.items():
                if 'svr' in k:
                    self._svr_params[k] = v

            model = SupportVectorRegressorPredictiveModel(self._X_train, self._y_train, self._svr_params, self._nfolds, self._n_jobs, self._verbose)
            return model

        def randomForestRegression():
            self._rfr_params = {}
            for k, v in self._allParams.items():
                if 'rfr' in k:
                    self._rfr_params[k] = v

            model = RandomForestRegressorPredictiveModel(self._X_train, self._y_train, self._rfr_params, self._nfolds, self._n_jobs, self._verbose)
            return model

        def adaptiveBoostingRegression():
            self._abr_params = {}
            for k, v in self._allParams.items():
                if 'abr' in k:
                    self._abr_params[k] = v

            model = AdaptiveBoostingRegressorPredictiveModel(self._X_train, self._y_train, self._abr_params, self._nfolds, self._n_jobs, self._verbose)
            return model

        def knnRegression():
            self._knnr_params = {}
            for k, v in self._allParams.items():
                if 'knnr' in k:
                    self._knnr_params[k] = v

            model = KNNRegressorPredictiveModel(self._X_train, self._y_train, self._knnr_params, self._nfolds, self._n_jobs, self._verbose)
            return model

        def ridgeRegression():
            self._ridge_params = {}
            for k, v in self._allParams.items():
                if 'ridge' in k:
                    self._ridge_params[k] = v

            model = RidgeRegressorPredictiveModel(self._X_train, self._y_train, self._ridge_params, self._nfolds, self._n_jobs, self._verbose)
            return model

        def lassoRegression():
            self._lasso_params = {}
            for k, v in self._allParams.items():
                if 'lasso' in k:
                    self._lasso_params[k] = v

            model = LassoRegressorPredictiveModel(self._X_train, self._y_train, self._lasso_params, self._nfolds, self._n_jobs, self._verbose)
            return model

        def elasticNetRegression():
            self._enet_params = {}
            for k, v in self._allParams.items():
                if 'enet' in k:
                    self._enet_params[k] = v

            model = ElasticNetRegressorPredictiveModel(self._X_train, self._y_train, self._enet_params, self._nfolds, self._n_jobs, self._verbose)
            return model

        def multilayerPerceptronRegression():
            self._mlpr_params = {}
            for k, v in self._allParams.items():
                if 'mlpr' in k:
                    self._mlpr_params[k] = v

            model = MultilayerPerceptronRegressorPredictiveModel(self._X_train, self._y_train, self._mlpr_params, self._nfolds, self._n_jobs, self._verbose)
            return model

        options = {'lr': linearRegression, 'svr': supportVectorRegression, 
           'rfr': randomForestRegression, 
           'abr': adaptiveBoostingRegression, 
           'knnr': knnRegression, 
           'ridge': ridgeRegression, 
           'lasso': lassoRegression, 
           'enet': elasticNetRegression, 
           'mlpr': multilayerPerceptronRegression}
        self._X_train, self._X_test, self._y_train, self._y_test = train_test_split(self._X, self._y, test_size=self._test_size)
        self._wrapper_models = []
        for key in models_to_flow:
            self._wrapper_models.append(options[key]())

        if self._verbose:
            print
        self._bestEstimators = self.determineBestEstimators(self._wrapper_models)
        if len(self._metrics) > 0:
            self._bestEstiminator = self.handleModelSelection(self._regressors, self._metrics, self._X_test, self._y_test, self._wrapper_models, self._cut)
        return self._bestEstimators