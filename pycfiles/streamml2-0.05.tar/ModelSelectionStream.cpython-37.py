# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\bmccs\Desktop\streamml2\streamml2\streamline\model_selection\flow\ModelSelectionStream.py
# Compiled at: 2019-01-26 09:26:58
# Size of source mod 2**32: 54962 bytes
import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt
import seaborn as sns, sys, os
from collections import defaultdict
from scipy.stats import ttest_ind
import models.regressors.LinearRegressorPredictiveModel as LinearRegressorPredictiveModel
import models.regressors.SupportVectorRegressorPredictiveModel as SupportVectorRegressorPredictiveModel
import models.regressors.RidgeRegressorPredictiveModel as RidgeRegressorPredictiveModel
import models.regressors.LassoRegressorPredictiveModel as LassoRegressorPredictiveModel
import models.regressors.ElasticNetRegressorPredictiveModel as ElasticNetRegressorPredictiveModel
import models.regressors.KNNRegressorPredictiveModel as KNNRegressorPredictiveModel
import models.regressors.RandomForestRegressorPredictiveModel as RandomForestRegressorPredictiveModel
import models.regressors.AdaptiveBoostingRegressorPredictiveModel as AdaptiveBoostingRegressorPredictiveModel
import models.regressors.MultilayerPerceptronRegressorPredictiveModel as MultilayerPerceptronRegressorPredictiveModel
import models.regressors.LassoLeastAngleRegressorPredictiveModel as LassoLeastAngleRegressorPredictiveModel
import models.regressors.LeastAngleRegressorPredictiveModel as LeastAngleRegressorPredictiveModel
import models.regressors.BayesianRidgeRegressorPredictiveModel as BayesianRidgeRegressorPredictiveModel
import models.regressors.ARDRegressorPredictiveModel as ARDRegressorPredictiveModel
import models.regressors.PassiveAggressiveRegressorPredictiveModel as PassiveAggressiveRegressorPredictiveModel
import models.regressors.TheilSenRegressorPredictiveModel as TheilSenRegressorPredictiveModel
import models.regressors.HuberRegressorPredictiveModel as HuberRegressorPredictiveModel
import models.regressors.GaussianProcessRegressorPredictiveModel as GaussianProcessRegressorPredictiveModel
import models.regressors.GradientBoostingRegressorPredictiveModel as GradientBoostingRegressorPredictiveModel
import models.regressors.BaggingRegressorPredictiveModel as BaggingRegressorPredictiveModel
import models.regressors.DecisionTreeRegressorPredictiveModel as DecisionTreeRegressorPredictiveModel
import models.classifiers.AdaptiveBoostingClassifierPredictiveModel as AdaptiveBoostingClassifierPredictiveModel
import models.classifiers.DecisionTreeClassifierPredictiveModel as DecisionTreeClassifierPredictiveModel
import models.classifiers.GradientBoostingClassifierPredictiveModel as GradientBoostingClassifierPredictiveModel
import models.classifiers.GuassianProcessClassifierPredictiveModel as GuassianProcessClassifierPredictiveModel
import models.classifiers.KNNClassifierPredictiveModel as KNNClassifierPredictiveModel
import models.classifiers.LogisticRegressionClassifierPredictiveModel as LogisticRegressionClassifierPredictiveModel
import models.classifiers.MultilayerPerceptronClassifierPredictiveModel as MultilayerPerceptronClassifierPredictiveModel
import models.classifiers.NaiveBayesClassifierPredictiveModel as NaiveBayesClassifierPredictiveModel
import models.classifiers.RandomForestClassifierPredictiveModel as RandomForestClassifierPredictiveModel
import models.classifiers.StochasticGradientDescentClassifierPredictiveModel as StochasticGradientDescentClassifierPredictiveModel
import models.classifiers.SupportVectorClassifierPredictiveModel as SupportVectorClassifierPredictiveModel
from utils.helpers import listofdict2dictoflist
import warnings
warnings.filterwarnings('ignore')

class ModelSelectionStream:
    _X = None
    _y = None
    _test_size = None
    _nfolds = None
    _nrepeats = None
    _n_jobs = None
    _verbose = None
    _metrics = None
    _wrapper_models = None
    _bestEstimators = None
    _scoring_results = None
    _final_results = None
    _regressors_results_list = None
    _regressors_results = None
    _classifier_results_list = None
    _classifiers_results = None
    _model_selection = None
    _stratified = None
    _metrics_significance_dict = None
    _random_grid = None
    _n_iter = None

    def __init__(self, X, y):
        assert isinstance(X, pd.DataFrame), 'X was not a pandas DataFrame'
        assert any([isinstance(y, pd.DataFrame), isinstance(y, pd.Series)]), 'y was not a pandas DataFrame or Series'
        self._X = X
        self._y = y

    def getActualErrorOnTest(self, metrics, wrapper_models):
        self._final_results = {}
        for model in wrapper_models:
            model._model.fit(self._X_train, self._y_train)
            results = model.validate(self._X_test, self._y_test, metrics)
            self._final_results[model.getCode()] = results

        if self._verbose:
            print('*************************************************************')
            print('=> (Final Results) => True Error Between Xtrain Xtest')
            print('*************************************************************')
        df_results = pd.DataFrame(self._final_results)
        if self._verbose:
            print(df_results)
        df_results.plot(title=('Error(s) - Train Size:' + str(1 - self._test_size) + ' Test Size: ' + str(self._test_size)))
        plt.xticks(range(len(df_results.index.tolist())), df_results.index.tolist())
        locs, labels = plt.xticks()
        plt.setp(labels, rotation=45)
        plt.show()
        return self._final_results

    def getBestEstimators(self):
        return self._bestEstimators

    def determineBestEstimators(self, models):
        self._bestEstimators = {}
        if self._verbose:
            print('**************************************************')
            print('Determining Best Estimators.')
            print('**************************************************')
        for model in models:
            self._bestEstimators[model.getCode()] = model.getBestEstimator()

        return self._bestEstimators

    def handleRegressors(self, Xtrain, ytrain, metrics, wrapper_models, cut, stratified):
        return_dict = {}
        self._regressors_results_list = defaultdict(list)
        self._regressors_results = dict()
        if stratified:
            if self._verbose:
                print('Executing Standard ' + str(self._nfolds) + '-Fold Cross Validation Repeated ' + str(self._nrepeats) + ' Times.')
            assert self._cut != None, 'you must select a cut point for your stratified folds to equally distribute your critical points'
            rskf = RepeatedStratifiedKFold(n_splits=(self._nfolds), n_repeats=(self._nrepeats), random_state=36851234)
            ycut = ytrain.copy()
            ycut[ycut < cut] = 1
            ycut[ycut >= cut] = 0
            for train_index, test_index in rskf.split(Xtrain, ycut):
                fold_X_train, fold_X_test = Xtrain.iloc[train_index, :], Xtrain.iloc[test_index, :]
                fold_y_train, fold_y_test = ytrain.iloc[train_index], ytrain.iloc[test_index]
                for model in wrapper_models:
                    model._model.fit(fold_X_train, fold_y_train)
                    results = model.validate(fold_X_test, fold_y_test, metrics)
                    self._regressors_results_list[model.getCode()].append(results)

            for k, v in self._regressors_results_list.items():
                example_df = pd.DataFrame(self._regressors_results_list[k])
                mean = example_df.mean()
                self._regressors_results[k] = mean

        else:
            if self._verbose:
                print('Executing Standard ' + str(self._nfolds) + '-Fold Cross Validation Repeated ' + str(self._nrepeats) + ' Times.')
            kf = KFold(n_splits=(self._nfolds))
            for train_index, test_index in kf.split(Xtrain):
                fold_X_train, fold_X_test = Xtrain.iloc[train_index, :], Xtrain.iloc[test_index, :]
                fold_y_train, fold_y_test = ytrain.iloc[train_index], ytrain.iloc[test_index]
                for model in wrapper_models:
                    model._model.fit(fold_X_train, fold_y_train)
                    results = model.validate(fold_X_test, fold_y_test, metrics)
                    self._regressors_results_list[model.getCode()].append(results)

            for k, v in self._regressors_results_list.items():
                example_df = pd.DataFrame(self._regressors_results_list[k])
                mean = example_df.mean()
                self._regressors_results[k] = mean

        return_dict['avg_kfold'] = self._regressors_results
        if self._verbose:
            print('*****************************************')
            print('=> (Regressor) => Performance Sheet')
            print('*****************************************')
        df_results = pd.DataFrame(self._regressors_results)
        if self._verbose:
            print(df_results)
            df_results.plot(title=('Error(s) - Regressor(s) - Average ' + str(self._nfolds) + '-Fold CV'))
            plt.xticks(range(len(df_results.index.tolist())), df_results.index.tolist())
            locs, labels = plt.xticks()
            plt.setp(labels, rotation=45)
            plt.show()
        if self._stats:
            if self._verbose:
                print('*****************************************************************************************')
                print('=> (Regressor) => (Two Tailed T-test) =>(Calculating Statistical Differences In Means)')
                print('*****************************************************************************************')
            self._metrics_significance_dict = {}
            for m in metrics:
                ttest_sig_mat = np.zeros((len(wrapper_models), len(wrapper_models)))
                for i, k in enumerate(self._regressors_results.keys()):
                    for j, k2 in enumerate(self._regressors_results.keys()):
                        nd = listofdict2dictoflist(self._regressors_results_list[k])
                        nd2 = listofdict2dictoflist(self._regressors_results_list[k2])
                        p_int = ttest_ind((nd[m]), (nd2[m]),
                          equal_var=False)
                        if p_int[1] <= 0.05:
                            ttest_sig_mat[(i, j)] = 1

                df = pd.DataFrame(ttest_sig_mat)
                df.index = list(self._regressors_results.keys())
                df.columns = list(self._regressors_results.keys())
                self._metrics_significance_dict[m] = df
                if self._verbose:
                    print(self._metrics_significance_dict[m])

            return_dict['significance'] = self._metrics_significance_dict
        return return_dict

    def handleClassifiers(self, Xtrain, ytrain, metrics, wrapper_models, stratified):
        return_dict = {}
        self._classifier_results_list = defaultdict(list)
        self._classifier_results = dict()
        if stratified:
            if self._verbose:
                print('Executing Stratified ' + str(self._nfolds) + 'Fold Cross Validation Repeated ' + str(self._nrepeats) + ' Times.')
            rskf = RepeatedStratifiedKFold(n_splits=(self._nfolds), n_repeats=(self._nrepeats), random_state=36851234)
            for train_index, test_index in rskf.split(Xtrain, ytrain):
                fold_X_train, fold_X_test = Xtrain.iloc[train_index, :], Xtrain.iloc[test_index, :]
                fold_y_train, fold_y_test = ytrain.iloc[train_index], ytrain.iloc[test_index]
                for model in wrapper_models:
                    model._model.fit(fold_X_train, fold_y_train)
                    results = model.validate(fold_X_test, fold_y_test, metrics)
                    self._classifier_results_list[model.getCode()].append(results)

            for k, v in self._classifier_results_list.items():
                example_df = pd.DataFrame(self._classifier_results_list[k])
                mean = example_df.mean()
                self._classifier_results[k] = mean

        else:
            if self._verbose:
                print('Executing Standard ' + str(self._nfolds) + '-Fold Cross Validation Repeated ' + str(self._nrepeats) + ' Times.')
            kf = KFold(n_splits=(self._nfolds))
            for train_index, test_index in kf.split(Xtrain):
                fold_X_train, fold_X_test = Xtrain.iloc[train_index, :], Xtrain.iloc[test_index, :]
                fold_y_train, fold_y_test = ytrain.iloc[train_index], ytrain.iloc[test_index]
                for model in wrapper_models:
                    model._model.fit(fold_X_train, fold_y_train)
                    results = model.validate(fold_X_test, fold_y_test, metrics)
                    self._classifier_results_list[model.getCode()].append(results)

            for k, v in self._classifier_results_list.items():
                example_df = pd.DataFrame(self._classifier_results_list[k])
                mean = example_df.mean()
                self._classifier_results[k] = mean

        return_dict['avg_kfold'] = self._classifier_results
        if self._verbose:
            print('*****************************************')
            print('=> (Classifier) => Performance Sheet')
            print('*****************************************')
        df_results = pd.DataFrame(self._classifier_results)
        if self._verbose:
            print(df_results)
            df_results.plot(title=('Error(s) - Classifiers(s) - Average ' + str(self._nfolds) + '-Fold CV'))
            plt.xticks(range(len(df_results.index.tolist())), df_results.index.tolist())
            locs, labels = plt.xticks()
            plt.setp(labels, rotation=45)
            plt.show()
        if self._stats:
            if self._verbose:
                print('*****************************************************************************************')
                print('=> (Classifier) => (Two Tailed T-test) =>(Calculating Statistical Differences In Means)')
                print('*****************************************************************************************')
            self._metrics_significance_dict = {}
            for m in metrics:
                ttest_sig_mat = np.zeros((len(wrapper_models), len(wrapper_models)))
                for i, k in enumerate(self._classifier_results.keys()):
                    for j, k2 in enumerate(self._classifier_results.keys()):
                        nd = listofdict2dictoflist(self._classifier_results_list[k])
                        nd2 = listofdict2dictoflist(self._classifier_results_list[k2])
                        p_int = ttest_ind((nd[m]), (nd2[m]),
                          equal_var=False)
                        if p_int[1] <= 0.1:
                            ttest_sig_mat[(i, j)] = 1
                        else:
                            ttest_sig_mat[(i, j)] = 0

                df = pd.DataFrame(ttest_sig_mat)
                df.index = list(self._classifier_results.keys())
                df.columns = list(self._classifier_results.keys())
                self._metrics_significance_dict[m] = df
                if self._verbose:
                    print(self._metrics_significance_dict[m])

            return_dict['significance'] = self._metrics_significance_dict
        return return_dict

    def flow(self, models_to_flow, params={}, test_size=0.3, nfolds=3, nrepeats=10, stats=True, stratified=False, n_jobs=1, metrics=[], verbose=True, regressors=True, model_selection=True, cut=None, random_grid=False, n_iter=10):
        if not isinstance(models_to_flow, list):
            if not isinstance(models_to_flow, tuple):
                raise AssertionError('Your models to flow must be a list or tuple.')
            elif not len(models_to_flow) > 0:
                raise AssertionError('You mus thave at least one model to flow, calculated len(models_to_flow)=' + str(len(models_to_flow)))
            else:
                assert isinstance(nfolds, int), 'nfolds must be integer'
                assert isinstance(nrepeats, int), 'nrepeats must be integer'
                assert isinstance(n_jobs, int), 'n_jobs must be integer'
                assert isinstance(verbose, bool), 'verbosem ust be bool'
                assert isinstance(params, dict), 'params must be a dict'
                assert isinstance(test_size, float), 'test_size must be a float'
                assert isinstance(metrics, list), 'model scoring must be a list'
                assert isinstance(regressors, bool), 'regressor must be bool'
                assert isinstance(model_selection, bool), 'modelSelection must be bool'
                assert isinstance(stratified, bool), 'modelSelection must be bool'
                assert isinstance(stats, bool), 'stats must be bool'
                assert isinstance(random_grid, bool), 'random_grid must be bool'
                assert isinstance(n_iter, int), 'random_grid must be int'
                self._nfolds = nfolds
                self._nrepeats = nrepeats
                self._n_jobs = n_jobs
                self._verbose = verbose
                self._allParams = params
                self._metrics = metrics
                self._test_size = test_size
                self._regressors = regressors
                self._model_selection = model_selection
                self._cut = cut
                self._stratified = stratified
                self._stats = stats
                self._random_grid = random_grid
                self._n_iter = n_iter
                stringbuilder = ''
                for thing in models_to_flow:
                    stringbuilder += thing
                    stringbuilder += ' --> '

                if self._verbose:
                    if self._regressors:
                        print('*************************')
                        print('=> (Regressor) => Model Selection Streamline: ' + stringbuilder[:-5])
                        print('*************************')
                    else:
                        if self._regressors == False:
                            print('*************************')
                            print('=> (Classifier) => Model Selection Streamline: ' + stringbuilder[:-5])
                            print('*************************')
                        else:
                            print('Invalid model selected. Please set regressors=True or regressors=False.')
                            print

            def linearRegression():
                self._lr_params = {}
                for k, v in self._allParams.items():
                    if 'lr' == k.split('__')[0]:
                        self._lr_params[k] = v

                model = LinearRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._lr_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def supportVectorRegression():
                self._svr_params = {}
                for k, v in self._allParams.items():
                    if 'svr' == k.split('__')[0]:
                        self._svr_params[k] = v

                model = SupportVectorRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._svr_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def randomForestRegression():
                self._rfr_params = {}
                for k, v in self._allParams.items():
                    if 'rfr' == k.split('__')[0]:
                        self._rfr_params[k] = v

                model = RandomForestRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._rfr_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def adaptiveBoostingRegression():
                self._abr_params = {}
                for k, v in self._allParams.items():
                    if 'abr' == k.split('__')[0]:
                        self._abr_params[k] = v

                model = AdaptiveBoostingRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._abr_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def knnRegression():
                self._knnr_params = {}
                for k, v in self._allParams.items():
                    if 'knnr' == k.split('__')[0]:
                        self._knnr_params[k] = v

                model = KNNRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._knnr_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def ridgeRegression():
                self._ridge_params = {}
                for k, v in self._allParams.items():
                    if 'ridge' == k.split('__')[0]:
                        self._ridge_params[k] = v

                model = RidgeRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._ridge_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def lassoRegression():
                self._lasso_params = {}
                for k, v in self._allParams.items():
                    if 'lasso' == k.split('__')[0]:
                        self._lasso_params[k] = v

                model = LassoRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._lasso_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def elasticNetRegression():
                self._enet_params = {}
                for k, v in self._allParams.items():
                    if 'enet' == k.split('__')[0]:
                        self._enet_params[k] = v

                model = ElasticNetRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._enet_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def multilayerPerceptronRegression():
                self._mlpr_params = {}
                for k, v in self._allParams.items():
                    if 'mlpr' == k.split('__')[0]:
                        self._mlpr_params[k] = v

                model = MultilayerPerceptronRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._mlpr_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def leastAngleRegression():
                self._lar_params = {}
                for k, v in self._allParams.items():
                    if 'lar' == k.split('__')[0]:
                        self._lar_params[k] = v

                model = LeastAngleRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._lar_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def lassoLeastAngleRegression():
                self._lasso_lar_params = {}
                for k, v in self._allParams.items():
                    if 'lasso_lar' == k.split('__')[0]:
                        self._lasso_lar_params[k] = v

                model = LassoLeastAngleRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._lasso_lar_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def bayesianRidgeRegression():
                self._bays_ridge = {}
                for k, v in self._allParams.items():
                    if 'bays_ridge' == k.split('__')[0]:
                        self._bays_ridge[k] = v

                model = BayesianRidgeRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._bays_ridge),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def ardRegression():
                self._ardr_params = {}
                for k, v in self._allParams.items():
                    if 'ardr' == k.split('__')[0]:
                        self._ardr_params[k] = v

                model = ARDRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._ardr_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def passiveAggressiveRegression():
                self._par_params = {}
                for k, v in self._allParams.items():
                    if 'par' == k.split('__')[0]:
                        self._par_params[k] = v

                model = PassiveAggressiveRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._par_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def theilSenRegression():
                self._tsr_params = {}
                for k, v in self._allParams.items():
                    if 'tsr' == k.split('__')[0]:
                        self._tsr_params[k] = v

                model = TheilSenRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._tsr_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def huberRegression():
                self._hr_params = {}
                for k, v in self._allParams.items():
                    if 'hr' == k.split('__')[0]:
                        self._hr_params[k] = v

                model = HuberRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._hr_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def gaussianProcessRegression():
                self._gpr_params = {}
                for k, v in self._allParams.items():
                    if 'gpr' == k.split('__')[0]:
                        self._gpr_params[k] = v

                model = GaussianProcessRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._gpr_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def gradientBoostingRegression():
                self._gbr_params = {}
                for k, v in self._allParams.items():
                    if 'gbr' == k.split('__')[0]:
                        self._gbr_params[k] = v

                model = GradientBoostingRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._gbr_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def baggingRegression():
                self._br_params = {}
                for k, v in self._allParams.items():
                    if 'br' == k.split('__')[0]:
                        self._br_params[k] = v

                model = BaggingRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._br_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def decisionTreeRegression():
                self._dtr_params = {}
                for k, v in self._allParams.items():
                    if 'dtr' == k.split('__')[0]:
                        self._dtr_params[k] = v

                model = DecisionTreeRegressorPredictiveModel((self._X_train), (self._y_train),
                  (self._dtr_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def adaptiveBoostingClassifier():
                self._abc_params = {}
                for k, v in self._allParams.items():
                    if 'abc' == k.split('__')[0]:
                        self._abc_params[k] = v

                model = AdaptiveBoostingClassifierPredictiveModel((self._X_train), (self._y_train),
                  (self._abc_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def decisionTreeClassifier():
                self._dtc_params = {}
                for k, v in self._allParams.items():
                    if 'dtc' == k.split('__')[0]:
                        self._dtc_params[k] = v

                model = DecisionTreeClassifierPredictiveModel((self._X_train), (self._y_train),
                  (self._dtc_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def gradientBoostingClassifier():
                self._gbc_params = {}
                for k, v in self._allParams.items():
                    if 'gbc' == k.split('__')[0]:
                        self._gbc_params[k] = v

                model = GradientBoostingClassifierPredictiveModel((self._X_train), (self._y_train),
                  (self._gbc_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def guassianProcessClassifier():
                self._gpc_params = {}
                for k, v in self._allParams.items():
                    if 'gpc' == k.split('__')[0]:
                        self._gpc_params[k] = v

                model = GuassianProcessClassifierPredictiveModel((self._X_train), (self._y_train),
                  (self._gpc_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def knnClassifier():
                self._knnc_params = {}
                for k, v in self._allParams.items():
                    if 'knnc' == k.split('__')[0]:
                        self._knnc_params[k] = v

                model = KNNClassifierPredictiveModel((self._X_train), (self._y_train),
                  (self._knnc_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def logisticRegressionClassifier():
                self._logr_params = {}
                for k, v in self._allParams.items():
                    if 'logr' == k.split('__')[0]:
                        self._logr_params[k] = v

                model = LogisticRegressionClassifierPredictiveModel((self._X_train), (self._y_train),
                  (self._logr_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def multilayerPerceptronClassifier():
                self._mlpc_params = {}
                for k, v in self._allParams.items():
                    if 'mlpc' == k.split('__')[0]:
                        self._mlpc_params[k] = v

                model = MultilayerPerceptronClassifierPredictiveModel((self._X_train), (self._y_train),
                  (self._mlpc_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def naiveBayesClassifier():
                self._nbc_params = {}
                for k, v in self._allParams.items():
                    if 'nbc' == k.split('__')[0]:
                        self._nbc_params[k] = v

                model = NaiveBayesClassifierPredictiveModel((self._X_train), (self._y_train),
                  (self._nbc_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def randomForestClassifier():
                self._rfc_params = {}
                for k, v in self._allParams.items():
                    if 'rfc' == k.split('__')[0]:
                        self._rfc_params[k] = v

                model = RandomForestClassifierPredictiveModel((self._X_train), (self._y_train),
                  (self._rfc_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def stochasticGradientDescentClassifier():
                self._sgdc_params = {}
                for k, v in self._allParams.items():
                    if 'sgdc' == k.split('__')[0]:
                        self._sgdc_params[k] = v

                model = StochasticGradientDescentClassifierPredictiveModel((self._X_train), (self._y_train),
                  (self._sgdc_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            def supportVectorClassifier():
                self._svc_params = {}
                for k, v in self._allParams.items():
                    if 'svc' == k.split('__')[0]:
                        self._svc_params[k] = v

                model = SupportVectorClassifierPredictiveModel((self._X_train), (self._y_train),
                  (self._svc_params),
                  nfolds=(self._nfolds),
                  n_jobs=(self._n_jobs),
                  random_grid=(self._random_grid),
                  n_iter=(self._n_iter),
                  verbose=(self._verbose))
                return model

            regression_options = {'lr':linearRegression, 
             'svr':supportVectorRegression, 
             'rfr':randomForestRegression, 
             'abr':adaptiveBoostingRegression, 
             'knnr':knnRegression, 
             'ridge':ridgeRegression, 
             'lasso':lassoRegression, 
             'enet':elasticNetRegression, 
             'mlpr':multilayerPerceptronRegression, 
             'br':baggingRegression, 
             'dtr':decisionTreeRegression, 
             'gbr':gradientBoostingRegression, 
             'gpr':gaussianProcessRegression, 
             'hr':huberRegression, 
             'tsr':theilSenRegression, 
             'par':passiveAggressiveRegression, 
             'ard':ardRegression, 
             'bays_ridge':bayesianRidgeRegression, 
             'lasso_lar':lassoLeastAngleRegression, 
             'lar':leastAngleRegression}
            classification_options = {'abc':adaptiveBoostingClassifier, 
             'dtc':decisionTreeClassifier, 
             'gbc':gradientBoostingClassifier, 
             'gpc':guassianProcessClassifier, 
             'knnc':knnClassifier, 
             'logr':logisticRegressionClassifier, 
             'mlpc':multilayerPerceptronClassifier, 
             'nbc':naiveBayesClassifier, 
             'rfc':randomForestClassifier, 
             'sgd':stochasticGradientDescentClassifier, 
             'svc':supportVectorClassifier}
            self._X_train, self._X_test, self._y_train, self._y_test = train_test_split((self._X), (self._y),
              test_size=(self._test_size))
            self._wrapper_models = []
            if self._regressors:
                for key in models_to_flow:
                    self._wrapper_models.append(regression_options[key]())

        elif self._regressors == False:
            for key in models_to_flow:
                self._wrapper_models.append(classification_options[key]())

        else:
            print('Invalid model type. Please set regressors=True or regressors=False.')
            print
        return_dict = {}
        self._bestEstimators = self.determineBestEstimators(self._wrapper_models)
        if self._model_selection:
            if not (
             len(self._wrapper_models) > 1, 'In order to compare models, you must have more than one. Add some in the first argument of `flow(...)` and retry.'):
                raise AssertionError
            else:
                if not len(self._metrics) > 0:
                    if self._regressors:
                        self._metrics = [
                         'rmse',
                         'mse',
                         'r2',
                         'explained_variance',
                         'mean_absolute_error',
                         'median_absolute_error']
                    else:
                        self._metrics = ['precision',
                         'recall',
                         'f1',
                         'accuracy',
                         'kappa']
                if self._regressors:
                    return_dict = self.handleRegressors(self._X_train, self._y_train, self._metrics, self._wrapper_models, self._cut, self._stratified)
                else:
                    if self._regressors == False:
                        return_dict = self.handleClassifiers(self._X_train, self._y_train, self._metrics, self._wrapper_models, self._stratified)
                    else:
                        print('You selected an invalid type of model.')
                        print
            self._final_results = self.getActualErrorOnTest(self._metrics, self._wrapper_models)
            return_dict['final_errors'] = self._final_results
        return_dict['models'] = self._bestEstimators
        return return_dict