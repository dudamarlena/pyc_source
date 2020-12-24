# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mlbox/preprocessing/drift/drift_estimator.py
# Compiled at: 2020-04-13 16:34:29
# Size of source mod 2**32: 4904 bytes
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_predict

class DriftEstimator:
    __doc__ = 'Estimates the drift between two datasets\n    \n        \n    Parameters\n    ----------\n    estimator : classifier, defaut = RandomForestClassifier(n_estimators = 50, n_jobs=-1, max_features=1., min_samples_leaf = 5, max_depth = 5)\n        The estimator that estimates the drift between two datasets\n        \n    n_folds : int, defaut = 2\n        Number of folds used to estimate the drift\n\n    stratify : bool, defaut = True\n        Whether the cv is stratified (same number of train and test samples within each fold)\n\n    random_state : int, defaut = 1\n        Random state for cv\n    '

    def __init__(self, estimator=RandomForestClassifier(n_estimators=50, n_jobs=-1, max_features=1.0, min_samples_leaf=5, max_depth=5), n_folds=2, stratify=True, random_state=1):
        self.estimator = estimator
        self.n_folds = n_folds
        self.stratify = stratify
        self.random_state = random_state
        self._DriftEstimator__cv = None
        self._DriftEstimator__pred = None
        self._DriftEstimator__target = None
        self._DriftEstimator__fitOK = False

    def get_params(self):
        return {'estimator': self.estimator, 
         'n_folds': self.n_folds, 
         'stratify': self.stratify, 
         'random_state': self.random_state}

    def set_params(self, **params):
        if 'estimator' in params.keys():
            self.estimator = params['estimator']
        if 'n_folds' in params.keys():
            self.n_folds = params['n_folds']
        if 'stratify' in params.keys():
            self.stratify = params['stratify']
        if 'random_state' in params.keys():
            self.random_state = params['random_state']

    def fit(self, df_train, df_test):
        """
        Computes the drift between the two datasets

        Parameters
        ----------
        df_train : pandas dataframe of shape = (n_train, p)
            The train set

        df_test : pandas dataframe of shape = (n_test, p)
            The test set

        Returns
        -------
        self : object
            Returns self.
        """
        df_train['target'] = 0
        df_test['target'] = 1
        self._DriftEstimator__target = pd.concat((df_train.target, df_test.target), ignore_index=True)
        if self.stratify:
            self._DriftEstimator__cv = StratifiedKFold(n_splits=self.n_folds, shuffle=True, random_state=self.random_state)
        else:
            self._DriftEstimator__cv = KFold(n_splits=self.n_folds, shuffle=True, random_state=self.random_state)
        X_tmp = pd.concat((df_train, df_test), ignore_index=True).drop(['target'], axis=1)
        self._DriftEstimator__pred = cross_val_predict(estimator=self.estimator, X=X_tmp, y=self._DriftEstimator__target, cv=self._DriftEstimator__cv, method='predict_proba')[:, 1]
        del df_train['target']
        del df_test['target']
        self._DriftEstimator__fitOK = True
        return self

    def score(self):
        """Returns the global drift measure between two datasets.

         0. = No drift. 1. = Maximal Drift

        Returns
        -------
        float
            The drift measure
        """
        S = []
        if self._DriftEstimator__fitOK:
            X_zeros = np.zeros(len(self._DriftEstimator__target))
            for train_index, test_index in self._DriftEstimator__cv.split(X=X_zeros, y=self._DriftEstimator__target):
                S.append(roc_auc_score(self._DriftEstimator__target.iloc[test_index], self._DriftEstimator__pred[test_index]))

            return (max(np.mean(S), 1 - np.mean(S)) - 0.5) * 2
        raise ValueError('Call the fit function before !')

    def predict(self):
        """Returns the probabilities that the sample belongs to the test dataset

        Returns
        -------
        Array of shape = (n_train+n_test,)
            The probabilities
        """
        if self._DriftEstimator__fitOK:
            return self._DriftEstimator__pred
        raise ValueError('Call the fit function before !')