# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mlbox/model/classification/classifier.py
# Compiled at: 2020-04-13 16:34:29
# Size of source mod 2**32: 13332 bytes
import warnings
from copy import copy
import numpy as np, pandas as pd
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier, ExtraTreesClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from lightgbm import LGBMClassifier

class Classifier:
    __doc__ = 'Wraps scikitlearn classifiers.\n\n    Parameters\n    ----------\n    strategy : str, default = "LightGBM"\n        The choice for the classifier.\n        Available strategies = {"LightGBM", "RandomForest", "ExtraTrees",\n        "Tree", "Bagging", "AdaBoost" or "Linear"}.\n\n    **params : default = None\n        Parameters of the corresponding classifier.\n        Examples : n_estimators, max_depth...\n\n    '

    def __init__(self, **params):
        """Init Classifier object.

        User can define strategy parameters.

        Parameters
        ----------
        strategy : str, default = "LightGBM"
            The choice of the classifier.
            Available strategies = {"LightGBM", "RandomForest", "ExtraTrees",
            "Tree", "Bagging", "AdaBoost" or "Linear"}.

        """
        if 'strategy' in params:
            self._Classifier__strategy = params['strategy']
        else:
            self._Classifier__strategy = 'LightGBM'
        self._Classifier__classif_params = {}
        self._Classifier__classifier = None
        self._Classifier__set_classifier(self._Classifier__strategy)
        self._Classifier__col = None
        self.set_params(**params)
        self._Classifier__fitOK = False

    def get_params(self, deep=True):
        """Get strategy parameters of Classifier object."""
        params = {}
        params['strategy'] = self._Classifier__strategy
        params.update(self._Classifier__classif_params)
        return params

    def set_params(self, **params):
        """Set strategy parameters of Classifier object."""
        self._Classifier__fitOK = False
        if 'strategy' in params.keys():
            self._Classifier__set_classifier(params['strategy'])
            for k, v in self._Classifier__classif_params.items():
                if k not in self.get_params().keys():
                    warnings.warn('Invalid parameter for classifier ' + str(self._Classifier__strategy) + '. Parameter IGNORED. Check the list of available parameters with `classifier.get_params().keys()`')
                else:
                    setattr(self._Classifier__classifier, k, v)

        for k, v in params.items():
            if k == 'strategy':
                continue
            if k not in self._Classifier__classifier.get_params().keys():
                warnings.warn('Invalid parameter for classifier ' + str(self._Classifier__strategy) + '. Parameter IGNORED. Check the list of available parameters with `classifier.get_params().keys()`')
            else:
                setattr(self._Classifier__classifier, k, v)
                self._Classifier__classif_params[k] = v

    def __set_classifier(self, strategy):
        """Set the classifier using scikitlearn Classifier."""
        self._Classifier__strategy = strategy
        if strategy == 'RandomForest':
            self._Classifier__classifier = RandomForestClassifier(n_estimators=400, max_depth=10, max_features='sqrt', bootstrap=True, n_jobs=-1, random_state=0)
        else:
            if strategy == 'LightGBM':
                self._Classifier__classifier = LGBMClassifier(n_estimators=500, learning_rate=0.05, colsample_bytree=0.8, subsample=0.9, nthread=-1, seed=0)
            else:
                if strategy == 'ExtraTrees':
                    self._Classifier__classifier = ExtraTreesClassifier(n_estimators=400, max_depth=10, max_features='sqrt', bootstrap=True, n_jobs=-1, random_state=0)
                else:
                    if strategy == 'Tree':
                        self._Classifier__classifier = DecisionTreeClassifier(criterion='gini', splitter='best', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=None, random_state=0, max_leaf_nodes=None, class_weight=None, presort=False)
                    else:
                        if strategy == 'Bagging':
                            self._Classifier__classifier = BaggingClassifier(base_estimator=None, n_estimators=500, max_samples=0.9, max_features=0.85, bootstrap=False, bootstrap_features=False, n_jobs=-1, random_state=0)
                        else:
                            if strategy == 'AdaBoost':
                                self._Classifier__classifier = AdaBoostClassifier(base_estimator=None, n_estimators=400, learning_rate=0.05, algorithm='SAMME.R', random_state=0)
                            else:
                                if strategy == 'Linear':
                                    self._Classifier__classifier = LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1, class_weight=None, random_state=0, solver='lbfgs', max_iter=100, multi_class='ovr', verbose=0, warm_start=False, n_jobs=-1)
                                else:
                                    raise ValueError("Strategy invalid. Please choose between 'LightGBM', 'RandomForest', 'ExtraTrees', 'Tree', 'Bagging', 'AdaBoost' or 'Linear'")

    def fit(self, df_train, y_train):
        """Fits Classifier.

        Parameters
        ----------
        df_train : pandas dataframe of shape = (n_train, n_features)
            The train dataset with numerical features.

        y_train : pandas series of shape = (n_train,)
            The numerical encoded target for classification tasks.

        Returns
        -------
        object
            self

        """
        if type(df_train) != pd.SparseDataFrame and type(df_train) != pd.DataFrame:
            raise ValueError('df_train must be a DataFrame')
        if type(y_train) != pd.core.series.Series:
            raise ValueError('y_train must be a Series')
        self._Classifier__classifier.fit(df_train.values, y_train)
        self._Classifier__col = df_train.columns
        self._Classifier__fitOK = True
        return self

    def feature_importances(self):
        """Compute feature importances.

        Classifier must be fitted before.

        Returns
        -------
        dict
            Dictionnary containing a measure of feature importance (value) for
            each feature (key).

        """
        if self._Classifier__fitOK:
            if self.get_params()['strategy'] in ('Linear', ):
                importance = {}
                f = np.mean(np.abs(self.get_estimator().coef_), axis=0)
                for i, col in enumerate(self._Classifier__col):
                    importance[col] = f[i]

            else:
                if self.get_params()['strategy'] in ('LightGBM', 'RandomForest', 'ExtraTrees',
                                                     'Tree'):
                    importance = {}
                    f = self.get_estimator().feature_importances_
                    for i, col in enumerate(self._Classifier__col):
                        importance[col] = f[i]

                else:
                    if self.get_params()['strategy'] in ('AdaBoost', ):
                        importance = {}
                        norm = self.get_estimator().estimator_weights_.sum()
                        try:
                            f = sum(weight * est.feature_importances_ for weight, est in zip(self.get_estimator().estimator_weights_, self.get_estimator().estimators_)) / norm
                        except:
                            f = sum(weight * np.mean(np.abs(est.coef_), axis=0) for weight, est in zip(self.get_estimator().estimator_weights_, self.get_estimator().estimators_)) / norm

                        for i, col in enumerate(self._Classifier__col):
                            importance[col] = f[i]

                    else:
                        if self.get_params()['strategy'] in ('Bagging', ):
                            importance = {}
                            importance_bag = []
                            for i, b in enumerate(self.get_estimator().estimators_):
                                d = {}
                                try:
                                    f = b.feature_importances_
                                except:
                                    f = np.mean(np.abs(b.coef_), axis=0)

                                for j, c in enumerate(self.get_estimator().estimators_features_[i]):
                                    d[self._Classifier__col[c]] = f[j]

                                importance_bag.append(d.copy())

                            for i, col in enumerate(self._Classifier__col):
                                list_filtered = filter(lambda x: x != 0, [k[col] if col in k else 0 for k in importance_bag])
                                importance[col] = np.mean(list(list_filtered))

                        else:
                            importance = {}
                return importance
            raise ValueError('You must call the fit function before !')

    def predict(self, df):
        """Predicts the target.

        Parameters
        ----------
        df : pandas dataframe of shape = (n, n_features)
            The dataset with numerical features.

        Returns
        -------
        array of shape = (n, )
            The encoded classes to be predicted.

        """
        try:
            if not callable(getattr(self._Classifier__classifier, 'predict')):
                raise ValueError('predict attribute is not callable')
        except Exception as e:
            raise e

        if self._Classifier__fitOK:
            if type(df) != pd.SparseDataFrame and type(df) != pd.DataFrame:
                raise ValueError('df must be a DataFrame')
            return self._Classifier__classifier.predict(df.values)
        raise ValueError('You must call the fit function before !')

    def predict_log_proba(self, df):
        """Predicts class log-probabilities for df.

        Parameters
        ----------
        df : pandas dataframe of shape = (n, n_features)
            The dataset with numerical features.

        Returns
        -------
        y : array of shape = (n, n_classes)
            The log-probabilities for each class

        """
        try:
            if not callable(getattr(self._Classifier__classifier, 'predict_log_proba')):
                raise ValueError('predict_log_proba attribute is not callable')
        except Exception as e:
            raise e

        if self._Classifier__fitOK:
            if type(df) != pd.SparseDataFrame and type(df) != pd.DataFrame:
                raise ValueError('df must be a DataFrame')
            return self._Classifier__classifier.predict_log_proba(df.values)
        raise ValueError('You must call the fit function before !')

    def predict_proba(self, df):
        """Predicts class probabilities for df.

        Parameters
        ----------
        df : pandas dataframe of shape = (n, n_features)
            The dataset with numerical features.

        Returns
        -------
        array of shape = (n, n_classes)
            The probabilities for each class

        """
        try:
            if not callable(getattr(self._Classifier__classifier, 'predict_proba')):
                raise ValueError('predict_proba attribute is not callable')
        except Exception as e:
            raise e

        if self._Classifier__fitOK:
            if type(df) != pd.SparseDataFrame and type(df) != pd.DataFrame:
                raise ValueError('df must be a DataFrame')
            return self._Classifier__classifier.predict_proba(df.values)
        raise ValueError('You must call the fit function before !')

    def score(self, df, y, sample_weight=None):
        """Return the mean accuracy.

        Parameters
        ----------
        df : pandas dataframe of shape = (n, n_features)
            The dataset with numerical features.

        y : pandas series of shape = (n,)
            The numerical encoded target for classification tasks.

        Returns
        -------
        float
            Mean accuracy of self.predict(df) wrt. y.

        """
        try:
            if not callable(getattr(self._Classifier__classifier, 'score')):
                raise ValueError('score attribute is not callable')
        except Exception as e:
            raise e

        if self._Classifier__fitOK:
            if type(df) != pd.SparseDataFrame and type(df) != pd.DataFrame:
                raise ValueError('df must be a DataFrame')
            if type(y) != pd.core.series.Series:
                raise ValueError('y must be a Series')
            return self._Classifier__classifier.score(df.values, y, sample_weight)
        raise ValueError('You must call the fit function before !')

    def get_estimator(self):
        """Return classfier."""
        return copy(self._Classifier__classifier)