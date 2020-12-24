# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/mlgear/encoders.py
# Compiled at: 2019-12-27 10:18:48
# Size of source mod 2**32: 5044 bytes
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import PowerTransformer, MinMaxScaler

class CategoricalDummyEncoder(TransformerMixin):
    __doc__ = 'Identifies categorical columns by dtype of object and dummy codes them. Optionally a pandas.DataFrame\n    can be returned where categories are of pandas.Category dtype and not binarized for better coding strategies\n    than dummy coding.'

    def __init__(self, sparse=False):
        self.categorical_variables = []
        self.categories_per_column = {}
        self.sparse = sparse

    def fit(self, X, categories=None):
        if categories is None:
            self.categorical_variables = list(X.select_dtypes(include=['object']).columns)
        else:
            self.categorical_variables = categories
        for col in self.categorical_variables:
            self.categories_per_column[col] = X[col].astype('category').cat.categories

        return self

    def transform(self, X):
        X = pd.get_dummies(X, sparse=(self.sparse), columns=(self.categorical_variables))
        expected_columns = sum([['{}_{}'.format(k, v) for v in vs] for k, vs in self.categories_per_column.items()], [])
        for c in expected_columns:
            if c not in X.columns:
                X.loc[:, c] = 0

        return X


class ValueCountsEncoder(TransformerMixin):

    def __init__(self):
        self.categorical_variables = []
        self.categories_per_column = {}

    def fit(self, X, categories=None):
        if categories is None:
            self.categorical_variables = list(X.select_dtypes(include=['object']).columns)
        else:
            self.categorical_variables = categories
        for col in self.categorical_variables:
            self.categories_per_column[col] = dict(X[col].value_counts().items())

        return self

    def transform(self, X, suffix=''):
        for col in self.categorical_variables:
            X.loc[:, '{}{}'.format(col, suffix)] = X[col].map(self.categories_per_column[col])

        return X


class BayesTargetEncoder(TransformerMixin):

    def __init__(self):
        self.categorical_variables = []
        self.categories_per_column = {}

    def fit(self, X, target, weight=10, categories=None):
        if categories is None:
            self.categorical_variables = list(X.select_dtypes(include=['object']).columns)
        else:
            self.categorical_variables = categories
        global_mean = X[target].mean()
        for col in self.categorical_variables:
            agg = X.groupby(col)[target].agg(['count', 'mean'])
            counts = agg['count']
            means = agg['mean']
            smooth = (counts * means + weight * global_mean) / (counts + weight)
            self.categories_per_column[col] = smooth

        return self

    def transform(self, X, suffix=''):
        for col in self.categorical_variables:
            X.loc[:, '{}{}'.format(col, suffix)] = X[col].map(self.categories_per_column[col])

        return X


class Scaler(BaseEstimator, TransformerMixin):

    def __init__(self, columns=None, ordinals=None, copy=True, feature_range=(0, 1)):
        if columns:
            self.scaler = PowerTransformer(method='yeo-johnson', standardize=True, copy=True)
        if ordinals:
            self.ordinal_scaler = MinMaxScaler(copy=copy, feature_range=feature_range)
        self.ordinals = ordinals
        self.columns = columns

    def fit(self, X, y=None):
        if self.columns:
            self.scaler.fit(X[self.columns], y)
        if self.ordinals:
            self.ordinal_scaler.fit(X[self.ordinals], y)
        return self

    def transform(self, X, y=None, copy=None):
        init_col_order = X.columns
        if self.columns:
            X_scaled = X[self.columns]
            X_scaled = pd.DataFrame((self.scaler.transform(X_scaled)), columns=(self.columns), index=(X.index))
        if self.ordinals:
            X_ordinals = X[self.ordinals]
            X_ordinals = pd.DataFrame((self.ordinal_scaler.transform(X_ordinals)), columns=(self.ordinals), index=(X.index))
        if self.columns:
            if self.ordinals:
                X_not_scaled = X[list(set(init_col_order) - set(self.columns) - set(self.ordinals))]
                return pd.concat([X_not_scaled, X_scaled, X_ordinals], axis=1)[init_col_order]
        if self.columns:
            X_not_scaled = X[list(set(init_col_order) - set(self.columns))]
            return pd.concat([X_not_scaled, X_scaled], axis=1)[init_col_order]
        if self.ordinals:
            X_not_scaled = X[list(set(init_col_order) - set(self.ordinals))]
            return pd.concat([X_not_scaled, X_ordinals], axis=1)[init_col_order]
        return X