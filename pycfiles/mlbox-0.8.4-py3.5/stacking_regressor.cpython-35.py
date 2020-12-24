# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mlbox/model/regression/stacking_regressor.py
# Compiled at: 2020-04-13 16:34:29
# Size of source mod 2**32: 9780 bytes
import numpy as np, pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_predict
from copy import copy as make_copy
from .regressor import Regressor
import warnings

class StackingRegressor:
    __doc__ = 'A Stacking regressor.\n\n     A stacking regressor is a regressor that uses the predictions of\n    several first layer estimators (generated with a cross validation method)\n    for a second layer estimator.\n\n\n    Parameters\n    ----------\n    base_estimators : list, default = [Regressor(strategy="LightGBM"),\n                                       Regressor(strategy="RandomForest"),\n                                       Regressor(strategy="ExtraTrees")]\n        List of estimators to fit in the first level using a cross validation.\n\n    level_estimator : object, default = LinearRegression()\n        The estimator used in second and last level\n\n    n_folds : int, default = 5\n        Number of folds used to generate the meta features for the training set\n\n    copy : bool, default = False\n        If true, meta features are added to the original dataset\n\n    random_state : None, int or RandomState. default = 1\n        Pseudo-random number generator state used for shuffling.\n        If None, use default numpy RNG for shuffling.\n\n    verbose : bool, default = True\n        Verbose mode.\n\n    '

    def __init__(self, base_estimators=[
 Regressor(strategy='LightGBM'),
 Regressor(strategy='RandomForest'),
 Regressor(strategy='ExtraTrees')], level_estimator=LinearRegression(), n_folds=5, copy=False, random_state=1, verbose=True):
        """Init method for StackingRegressor."""
        self.base_estimators = base_estimators
        if type(base_estimators) != list:
            raise ValueError('base_estimators must be a list')
        else:
            for i, est in enumerate(self.base_estimators):
                self.base_estimators[i] = make_copy(est)

        self.level_estimator = level_estimator
        self.n_folds = n_folds
        if type(n_folds) != int:
            raise ValueError('n_folds must be an integer')
        self.copy = copy
        if type(copy) != bool:
            raise ValueError('copy must be a boolean')
        self.random_state = random_state
        if type(self.random_state) != int and self.random_state is not None:
            raise ValueError('random_state must be either None or an integer')
        self.verbose = verbose
        if type(self.verbose) != bool:
            raise ValueError('verbose must be a boolean')
        self._StackingRegressor__fitOK = False
        self._StackingRegressor__fittransformOK = False

    def get_params(self, deep=True):
        """Get parameters of a StackingRegressor object."""
        return {'level_estimator': self.level_estimator, 
         'base_estimators': self.base_estimators, 
         'n_folds': self.n_folds, 
         'copy': self.copy, 
         'random_state': self.random_state, 
         'verbose': self.verbose}

    def set_params(self, **params):
        """Set parameters of a StackingRegressor object."""
        self._StackingRegressor__fitOK = False
        self._StackingRegressor__fittransformOK = False
        for k, v in params.items():
            if k not in self.get_params():
                warnings.warn('Invalid parameter a for stacking_regressor StackingRegressor. Parameter IGNORED. Check the list of available parameters with `stacking_regressor.get_params().keys()`')
            else:
                setattr(self, k, v)

    def fit_transform(self, df_train, y_train):
        """Create meta-features for the training dataset.

        Parameters
        ----------
        df_train : pandas DataFrame of shape = (n_samples, n_features)
            The training dataset.

        y_train : pandas series of shape = (n_samples, )
            The target

        Returns
        -------
        pandas DataFrame of shape = (n_samples,
                                     n_features*int(copy)+n_metafeatures)
            The transformed training dataset.

        """
        if (type(df_train) != pd.SparseDataFrame) & (type(df_train) != pd.DataFrame):
            raise ValueError('df_train must be a DataFrame')
        if type(y_train) != pd.core.series.Series:
            raise ValueError('y_train must be a Series')
        cv = KFold(n_splits=self.n_folds, shuffle=True, random_state=self.random_state)
        preds = pd.DataFrame([], index=y_train.index)
        if self.verbose:
            print('')
            print('[=============================================================================] LAYER [===================================================================================]')
            print('')
        for c, reg in enumerate(self.base_estimators):
            if self.verbose:
                print('> fitting estimator n°' + str(c + 1) + ' : ' + str(reg.get_params()) + ' ...')
                print('')
            y_pred = cross_val_predict(estimator=reg, X=df_train, y=y_train, cv=cv)
            preds['est' + str(c + 1)] = y_pred
            reg.fit(df_train, y_train)

        layer = 1
        columns = ['layer' + str(layer) + '_' + s for s in preds.columns]
        while len(np.intersect1d(df_train.columns, columns)) > 0:
            layer = layer + 1
            columns = ['layer' + str(layer) + '_' + s for s in preds.columns]

        preds.columns = ['layer' + str(layer) + '_' + s for s in preds.columns]
        self._StackingRegressor__fittransformOK = True
        if self.copy:
            return pd.concat([df_train, preds], axis=1)
        else:
            return preds

    def transform(self, df_test):
        """Create meta-features for the test dataset.

        Parameters
        ----------
        df_test : pandas DataFrame of shape = (n_samples_test, n_features)
            The test dataset.

        Returns
        -------
        pandas DataFrame of shape = (n_samples_test,
                                     n_features*int(copy)+n_metafeatures)
            The transformed test dataset.

        """
        if type(df_test) != pd.SparseDataFrame and type(df_test) != pd.DataFrame:
            raise ValueError('df_test must be a DataFrame')
        if self._StackingRegressor__fittransformOK:
            preds_test = pd.DataFrame([], index=df_test.index)
            for c, reg in enumerate(self.base_estimators):
                y_pred_test = reg.predict(df_test)
                preds_test['est' + str(c + 1)] = y_pred_test

            layer = 1
            columns = ['layer' + str(layer) + '_' + s for s in preds_test.columns]
            while len(np.intersect1d(df_test.columns, columns)) > 0:
                layer = layer + 1
                columns = ['layer' + str(layer) + '_' + s for s in preds_test.columns]

            preds_test.columns = ['layer' + str(layer) + '_' + s for s in preds_test.columns]
            if self.copy:
                return pd.concat([df_test, preds_test], axis=1)
            else:
                return preds_test
        else:
            raise ValueError('Call fit_transform before !')

    def fit(self, df_train, y_train):
        """Fit the first level estimators and the second level estimator on X.

        Parameters
        ----------
        df_train : pandas DataFrame of shape (n_samples, n_features)
            Input data

        y_train : pandas series of shape = (n_samples, )
            The target

        Returns
        -------
        object
            self

        """
        df_train = self.fit_transform(df_train, y_train)
        if self.verbose:
            print('')
            print('[=========================================================================] PREDICTION LAYER [============================================================================]')
            print('')
            print('> fitting estimator : ' + str(self.level_estimator.get_params()) + ' ...')
            print('')
        self.level_estimator.fit(df_train.values, y_train.values)
        self._StackingRegressor__fitOK = True
        return self

    def predict(self, df_test):
        """Predict regression target for X_test using the meta-features.

        Parameters
        ----------
        df_test : pandas DataFrame of shape = (n_samples_test, n_features)
            The testing samples

        Returns
        -------
        array of shape = (n_samples_test, )
            The predicted values.

        """
        if self._StackingRegressor__fitOK:
            df_test = self.transform(df_test)
            return self.level_estimator.predict(df_test)
        raise ValueError('Call fit before !')