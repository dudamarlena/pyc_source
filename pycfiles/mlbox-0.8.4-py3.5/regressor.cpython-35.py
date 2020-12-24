# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mlbox/model/regression/regressor.py
# Compiled at: 2020-04-13 16:34:29
# Size of source mod 2**32: 11758 bytes
import warnings
from copy import copy
import numpy as np, pandas as pd
from sklearn.ensemble import AdaBoostRegressor, BaggingRegressor, ExtraTreesRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor
from lightgbm import LGBMRegressor

class Regressor:
    __doc__ = 'Wrap scikitlearn regressors.\n\n    Parameters\n    ----------\n    strategy : str, default = "LightGBM"\n        The choice for the regressor.\n        Available strategies = {"LightGBM", "RandomForest", "ExtraTrees",\n        "Tree", "Bagging", "AdaBoost" or "Linear"}\n\n    **params : default = None\n        Parameters of the corresponding regressor.\n        Examples : n_estimators, max_depth...\n\n    '

    def __init__(self, **params):
        """Init Regressor object where user can pass a strategy."""
        if 'strategy' in params:
            self._Regressor__strategy = params['strategy']
        else:
            self._Regressor__strategy = 'LightGBM'
        self._Regressor__regress_params = {}
        self._Regressor__regressor = None
        self._Regressor__set_regressor(self._Regressor__strategy)
        self._Regressor__col = None
        self.set_params(**params)
        self._Regressor__fitOK = False

    def get_params(self, deep=True):
        """Get parameters of Regressor object."""
        params = {}
        params['strategy'] = self._Regressor__strategy
        params.update(self._Regressor__regress_params)
        return params

    def set_params(self, **params):
        """Set parameters of Regressor object."""
        self._Regressor__fitOK = False
        if 'strategy' in params.keys():
            self._Regressor__set_regressor(params['strategy'])
            for k, v in self._Regressor__regress_params.items():
                if k not in self.get_params().keys():
                    warnings.warn('Invalid parameter for regressor ' + str(self._Regressor__strategy) + '. Parameter IGNORED. Check the list of available parameters with `regressor.get_params().keys()`')
                else:
                    setattr(self._Regressor__regressor, k, v)

        for k, v in params.items():
            if k == 'strategy':
                continue
            if k not in self._Regressor__regressor.get_params().keys():
                warnings.warn('Invalid parameter for regressor ' + str(self._Regressor__strategy) + '. Parameter IGNORED. Check the list of available parameters with `regressor.get_params().keys()`')
            else:
                setattr(self._Regressor__regressor, k, v)
                self._Regressor__regress_params[k] = v

    def __set_regressor(self, strategy):
        """Set strategy of a regressor object."""
        self._Regressor__strategy = strategy
        if strategy == 'RandomForest':
            self._Regressor__regressor = RandomForestRegressor(n_estimators=400, max_depth=10, max_features='sqrt', bootstrap=True, n_jobs=-1, random_state=0)
        else:
            if strategy == 'LightGBM':
                self._Regressor__regressor = LGBMRegressor(n_estimators=500, learning_rate=0.05, colsample_bytree=0.8, subsample=0.9, nthread=-1, seed=0)
            else:
                if strategy == 'ExtraTrees':
                    self._Regressor__regressor = ExtraTreesRegressor(n_estimators=400, max_depth=10, max_features='sqrt', bootstrap=True, n_jobs=-1, random_state=0)
                else:
                    if strategy == 'Tree':
                        self._Regressor__regressor = DecisionTreeRegressor(criterion='mse', splitter='best', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=None, random_state=0, max_leaf_nodes=None, presort=False)
                    else:
                        if strategy == 'Bagging':
                            self._Regressor__regressor = BaggingRegressor(base_estimator=None, n_estimators=500, max_samples=0.9, max_features=0.85, bootstrap=False, bootstrap_features=False, n_jobs=-1, random_state=0)
                        else:
                            if strategy == 'AdaBoost':
                                self._Regressor__regressor = AdaBoostRegressor(base_estimator=None, n_estimators=400, learning_rate=0.05, random_state=0)
                            else:
                                if strategy == 'Linear':
                                    self._Regressor__regressor = Ridge(alpha=1.0, fit_intercept=True, normalize=False, copy_X=True, max_iter=None, tol=0.001, solver='auto', random_state=0)
                                else:
                                    raise ValueError("Strategy invalid. Please choose between 'LightGBM', 'RandomForest', 'ExtraTrees', 'Tree', 'Bagging', 'AdaBoost' or 'Linear'")

    def fit(self, df_train, y_train):
        """Fits Regressor.

        Parameters
        ----------
        df_train : pandas dataframe of shape = (n_train, n_features)
            The train dataset with numerical features.

        y_train : pandas series of shape = (n_train, )
            The target for regression tasks.

        Returns
        -------
        object
            self

        """
        if type(df_train) != pd.SparseDataFrame and type(df_train) != pd.DataFrame:
            raise ValueError('df_train must be a DataFrame')
        if type(y_train) != pd.core.series.Series:
            raise ValueError('y_train must be a Series')
        self._Regressor__regressor.fit(df_train.values, y_train)
        self._Regressor__col = df_train.columns
        self._Regressor__fitOK = True
        return self

    def feature_importances(self):
        """Computes feature importances.

        Regressor must be fitted before.

        Returns
        -------
        dict
            Dictionnary containing a measure of feature importance (value)
            for each feature (key).

        """
        if self._Regressor__fitOK:
            if self.get_params()['strategy'] in ('Linear', ):
                importance = {}
                f = np.abs(self.get_estimator().coef_)
                for i, col in enumerate(self._Regressor__col):
                    importance[col] = f[i]

            else:
                if self.get_params()['strategy'] in ('LightGBM', 'RandomForest', 'ExtraTrees',
                                                     'Tree'):
                    importance = {}
                    f = self.get_estimator().feature_importances_
                    for i, col in enumerate(self._Regressor__col):
                        importance[col] = f[i]

                else:
                    if self.get_params()['strategy'] in ('AdaBoost', ):
                        importance = {}
                        norm = self.get_estimator().estimator_weights_.sum()
                        try:
                            f = sum(weight * est.feature_importances_ for weight, est in zip(self.get_estimator().estimator_weights_, self.get_estimator().estimators_)) / norm
                        except Exception:
                            f = sum(weight * np.abs(est.coef_) for weight, est in zip(self.get_estimator().estimator_weights_, self.get_estimator().estimators_)) / norm

                        for i, col in enumerate(self._Regressor__col):
                            importance[col] = f[i]

                    else:
                        if self.get_params()['strategy'] in ('Bagging', ):
                            importance = {}
                            importance_bag = []
                            for i, b in enumerate(self.get_estimator().estimators_):
                                d = {}
                                try:
                                    f = b.feature_importances_
                                except Exception:
                                    f = np.abs(b.coef_)

                                estimator = self.get_estimator()
                                items = enumerate(estimator.estimators_features_[i])
                                for j, c in items:
                                    d[self._Regressor__col[c]] = f[j]

                                importance_bag.append(d.copy())

                            for i, col in enumerate(self._Regressor__col):
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
            The target to be predicted.

        """
        try:
            if not callable(getattr(self._Regressor__regressor, 'predict')):
                raise ValueError('predict attribute is not callable')
        except Exception as e:
            raise e

        if self._Regressor__fitOK:
            if (type(df) != pd.SparseDataFrame) & (type(df) != pd.DataFrame):
                raise ValueError('df must be a DataFrame')
            return self._Regressor__regressor.predict(df.values)
        raise ValueError('You must call the fit function before !')

    def transform(self, df):
        """Transform dataframe df.

        Parameters
        ----------
        df : pandas dataframe of shape = (n, n_features)
            The dataset with numerical features.

        Returns
        -------
        pandas dataframe of shape = (n, n_selected_features)
            The transformed dataset with its most important features.

        """
        try:
            if not callable(getattr(self._Regressor__regressor, 'transform')):
                raise ValueError('transform attribute is not callable')
        except Exception as e:
            raise e

        if self._Regressor__fitOK:
            if (type(df) != pd.SparseDataFrame) & (type(df) != pd.DataFrame):
                raise ValueError('df must be a DataFrame')
            return self._Regressor__regressor.transform(df.values)
        raise ValueError('You must call the fit function before !')

    def score(self, df, y, sample_weight=None):
        """Return R^2 coefficient of determination of the prediction.

        Parameters
        ----------
        df : pandas dataframe of shape = (n, n_features)
            The dataset with numerical features.

        y : pandas series of shape = (n,)
            The numerical encoded target for classification tasks.

        Returns
        -------
        float
            R^2 of self.predict(df) wrt. y.

        """
        try:
            if not callable(getattr(self._Regressor__regressor, 'score')):
                raise ValueError('score attribute is not callable')
        except Exception as e:
            raise e

        if self._Regressor__fitOK:
            if type(df) != pd.SparseDataFrame and type(df) != pd.DataFrame:
                raise ValueError('df must be a DataFrame')
            if type(y) != pd.core.series.Series:
                raise ValueError('y must be a Series')
            return self._Regressor__regressor.score(df.values, y, sample_weight)
        raise ValueError('You must call the fit function before !')

    def get_estimator(self):
        """Return classfier."""
        return copy(self._Regressor__regressor)