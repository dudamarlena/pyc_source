# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mlbox/model/regression/feature_selector.py
# Compiled at: 2020-04-13 16:34:29
# Size of source mod 2**32: 4969 bytes
import numpy as np, pandas as pd
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
import warnings

class Reg_feature_selector:
    __doc__ = 'Selects useful features.\n\n    Several strategies are possible (filter and wrapper methods).\n    Works for regression problems only.\n\n    Parameters\n    ----------\n    strategy : str, defaut = "l1"\n        The strategy to select features.\n        Available strategies = {"variance", "l1", "rf_feature_importance"}\n\n    threshold : float, defaut = 0.3\n        The percentage of variable to discard according the strategy.\n        Must be between 0. and 1.\n    '

    def __init__(self, strategy='l1', threshold=0.3):
        self.strategy = strategy
        self.threshold = threshold
        self._Reg_feature_selector__fitOK = False
        self._Reg_feature_selector__to_discard = []

    def get_params(self, deep=True):
        return {'strategy': self.strategy, 
         'threshold': self.threshold}

    def set_params(self, **params):
        self._Reg_feature_selector__fitOK = False
        for k, v in params.items():
            if k not in self.get_params():
                warnings.warn('Invalid parameter a for feature selectorReg_feature_selector. Parameter IGNORED. Check the list of available parameters with `feature_selector.get_params().keys()`')
            else:
                setattr(self, k, v)

    def fit(self, df_train, y_train):
        """Fits Reg_feature_selector.

        Parameters
        ----------
        df_train : pandas dataframe of shape = (n_train, n_features)
            The train dataset with numerical features and no NA

        y_train : pandas series of shape = (n_train, ).
            The target for regression task.

        Returns
        -------
        sobject
            self
        """
        if type(df_train) != pd.SparseDataFrame and type(df_train) != pd.DataFrame:
            raise ValueError('df_train must be a DataFrame')
        if type(y_train) != pd.core.series.Series:
            raise ValueError('y_train must be a Series')
        if self.strategy == 'variance':
            coef = df_train.std()
            abstract_threshold = np.percentile(coef, 100.0 * self.threshold)
            self._Reg_feature_selector__to_discard = coef[(coef < abstract_threshold)].index
            self._Reg_feature_selector__fitOK = True
        else:
            if self.strategy == 'l1':
                model = Lasso(alpha=100.0, random_state=0)
                model.fit(df_train, y_train)
                coef = np.abs(model.coef_)
                abstract_threshold = np.percentile(coef, 100.0 * self.threshold)
                self._Reg_feature_selector__to_discard = df_train.columns[(coef < abstract_threshold)]
                self._Reg_feature_selector__fitOK = True
            else:
                if self.strategy == 'rf_feature_importance':
                    model = RandomForestRegressor(n_estimators=50, n_jobs=-1, random_state=0)
                    model.fit(df_train, y_train)
                    coef = model.feature_importances_
                    abstract_threshold = np.percentile(coef, 100.0 * self.threshold)
                    self._Reg_feature_selector__to_discard = df_train.columns[(coef < abstract_threshold)]
                    self._Reg_feature_selector__fitOK = True
                else:
                    raise ValueError("Strategy invalid. Please choose between 'variance', 'l1' or 'rf_feature_importance'")
        return self

    def transform(self, df):
        """Transforms the dataset

        Parameters
        ----------
        df : pandas dataframe of shape = (n, n_features)
            The dataset with numerical features and no NA

        Returns
        -------
        pandas dataframe of shape = (n_train, n_features*(1-threshold))
            The train dataset with relevant features
        """
        if self._Reg_feature_selector__fitOK:
            if (type(df) != pd.SparseDataFrame) & (type(df) != pd.DataFrame):
                raise ValueError('df must be a DataFrame')
            return df.drop(self._Reg_feature_selector__to_discard, axis=1)
        raise ValueError('call fit or fit_transform function before')

    def fit_transform(self, df_train, y_train):
        """Fits Reg_feature_selector and transforms the dataset

        Parameters
        ----------
        df_train : pandas dataframe of shape = (n_train, n_features)
            The train dataset with numerical features and no NA

        y_train : pandas series of shape = (n_train, ).
            The target for regression task.

        Returns
        -------
        pandas dataframe of shape = (n_train, n_features*(1-threshold))
            The train dataset with relevant features
        """
        self.fit(df_train, y_train)
        return self.transform(df_train)