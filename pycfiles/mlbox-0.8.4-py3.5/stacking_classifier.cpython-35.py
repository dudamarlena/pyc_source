# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mlbox/model/classification/stacking_classifier.py
# Compiled at: 2020-04-13 16:34:29
# Size of source mod 2**32: 12731 bytes
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from copy import copy as make_copy
from .classifier import Classifier
import warnings

class StackingClassifier:
    __doc__ = 'A stacking classifier.\n\n    A stacking classifier is a classifier that uses the predictions of\n    several first layer estimators (generated with a cross validation method)\n    for a second layer estimator.\n\n    Parameters\n    ----------\n    base_estimators : list, default = [Classifier(strategy="LightGBM"), Classifier(strategy="RandomForest"),Classifier(strategy="ExtraTrees")]\n        List of estimators to fit in the first level using a cross validation.\n\n    level_estimator : object, default = LogisticRegression()\n        The estimator used in second and last level.\n\n    n_folds : int, default = 5\n        Number of folds used to generate the meta features for the training set\n\n    copy : bool, default = False\n        If true, meta features are added to the original dataset\n\n    drop_first : bool, default = True\n        If True, each estimator output n_classes-1 probabilities\n\n    random_state : None or int or RandomState. default = 1\n        Pseudo-random number generator state used for shuffling. If None, use\n        default numpy RNG for shuffling.\n\n    verbose : bool, default = True\n        Verbose mode.\n    '

    def __init__(self, base_estimators=[
 Classifier(strategy='LightGBM'),
 Classifier(strategy='RandomForest'),
 Classifier(strategy='ExtraTrees')], level_estimator=LogisticRegression(n_jobs=-1), n_folds=5, copy=False, drop_first=True, random_state=1, verbose=True):
        self.base_estimators = base_estimators
        if type(self.base_estimators) != list:
            raise ValueError('base_estimators must be a list')
        else:
            for i, est in enumerate(self.base_estimators):
                self.base_estimators[i] = make_copy(est)

        self.level_estimator = level_estimator
        self.n_folds = n_folds
        if type(self.n_folds) != int:
            raise ValueError('n_folds must be an integer')
        self.copy = copy
        if type(self.copy) != bool:
            raise ValueError('copy must be a boolean')
        self.drop_first = drop_first
        if type(self.drop_first) != bool:
            raise ValueError('drop_first must be a boolean')
        self.random_state = random_state
        if type(self.random_state) != int and self.random_state is not None:
            raise ValueError('random_state must be either None or an integer')
        self.verbose = verbose
        if type(self.verbose) != bool:
            raise ValueError('verbose must be a boolean')
        self._StackingClassifier__fitOK = False
        self._StackingClassifier__fittransformOK = False

    def get_params(self, deep=True):
        return {'level_estimator': self.level_estimator, 
         'base_estimators': self.base_estimators, 
         'n_folds': self.n_folds, 
         'copy': self.copy, 
         'drop_first': self.drop_first, 
         'random_state': self.random_state, 
         'verbose': self.verbose}

    def set_params(self, **params):
        self._StackingClassifier__fitOK = False
        self._StackingClassifier__fittransformOK = False
        for k, v in params.items():
            if k not in self.get_params():
                warnings.warn('Invalid parameter a for stacking_classifier StackingClassifier. Parameter IGNORED. Check the list of available parameters with `stacking_classifier.get_params().keys()`')
            else:
                setattr(self, k, v)

    def __cross_val_predict_proba(self, estimator, df, y, cv):
        """Evaluates the target by cross-validation

        Parameters
        ----------
        estimator : estimator object implementing 'fit'
            The object to use to fit the data.

        df : pandas DataFrame
            The data to fit.

        y : pandas Serie
            The target variable to try to predict in the case of
            supervised learning.

        cv : a STRATIFIED cross-validation generator

        Returns
        -------
        y_pred : array-like of shape = (n_samples, n_classes)
            The predicted class probabilities for X.
        """
        classes = y.value_counts()
        classes_to_drop = classes[(classes < 2)].index
        indexes_to_drop = y[y.apply(lambda x: x in classes_to_drop)].index
        y_pred = np.zeros((len(y), len(classes) - len(classes_to_drop)))
        for train_index, test_index in cv.split(df, y):
            df_train, df_test = df.iloc[train_index], df.iloc[test_index]
            y_train = y.iloc[train_index]
            try:
                df_train = df_train.drop(indexes_to_drop)
                y_train = y_train.drop(indexes_to_drop)
            except Exception:
                pass

            estimator.fit(df_train, y_train)
            y_pred[test_index] = estimator.predict_proba(df_test)[:,]

        return y_pred

    def fit_transform(self, df_train, y_train):
        """Creates meta-features for the training dataset.

        Parameters
        ----------
        df_train : pandas dataframe of shape = (n_samples, n_features)
            The training dataset.

        y_train : pandas series of shape = (n_samples, )
            The target.

        Returns
        -------
        pandas dataframe of shape = (n_samples, n_features*int(copy)+n_metafeatures)
            The transformed training dataset.
        """
        if type(df_train) != pd.SparseDataFrame and type(df_train) != pd.DataFrame:
            raise ValueError('df_train must be a DataFrame')
        if type(y_train) != pd.core.series.Series:
            raise ValueError('y_train must be a Series')
        cv = StratifiedKFold(n_splits=self.n_folds, shuffle=True, random_state=self.random_state)
        preds = pd.DataFrame([], index=y_train.index)
        classes = y_train.value_counts()
        classes_to_drop = classes[(classes < 2)].index
        indexes_to_drop = y_train[y_train.apply(lambda x: x in classes_to_drop)].index
        if self.verbose:
            print('')
            print('[=============================================================================] LAYER [===================================================================================]')
            print('')
        for c, clf in enumerate(self.base_estimators):
            if self.verbose:
                print('> fitting estimator n°' + str(c + 1) + ' : ' + str(clf.get_params()) + ' ...')
                print('')
            y_pred = self._StackingClassifier__cross_val_predict_proba(clf, df_train, y_train, cv)
            for i in range(0, y_pred.shape[1] - int(self.drop_first)):
                preds['est' + str(c + 1) + '_class' + str(i)] = y_pred[:, i]

            clf.fit(df_train.drop(indexes_to_drop), y_train.drop(indexes_to_drop))

        layer = 1
        columns = ['layer' + str(layer) + '_' + s for s in preds.columns]
        while len(np.intersect1d(df_train.columns, columns)) > 0:
            layer = layer + 1
            columns = ['layer' + str(layer) + '_' + s for s in preds.columns]

        preds.columns = ['layer' + str(layer) + '_' + s for s in preds.columns]
        self._StackingClassifier__fittransformOK = True
        if self.copy:
            return pd.concat([df_train, preds], axis=1)
        else:
            return preds

    def transform(self, df_test):
        """Creates meta-features for the test dataset.

        Parameters
        ----------
        df_test : pandas dataframe of shape = (n_samples_test, n_features)
            The test dataset.

        Returns
        -------
        pandas dataframe of shape = (n_samples_test, n_features*int(copy)+n_metafeatures)
            The transformed test dataset.
        """
        if type(df_test) != pd.SparseDataFrame and type(df_test) != pd.DataFrame:
            raise ValueError('df_test must be a DataFrame')
        if self._StackingClassifier__fittransformOK:
            preds_test = pd.DataFrame([], index=df_test.index)
            for c, clf in enumerate(self.base_estimators):
                y_pred_test = clf.predict_proba(df_test)
                for i in range(0, y_pred_test.shape[1] - int(self.drop_first)):
                    idx_name = 'est' + str(c + 1) + '_class' + str(i)
                    preds_test[idx_name] = y_pred_test[:, i]

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
        """Fits the first level estimators and the second level estimator on X.

        Parameters
        ----------
        df_train : pandas dataframe of shape (n_samples, n_features)
            Input data

        y_train : pandas series of shape = (n_samples, )
            The target

        Returns
        -------
        object
            self.
        """
        df_train = self.fit_transform(df_train, y_train)
        if self.verbose:
            print('')
            print('[=========================================================================] PREDICTION LAYER [============================================================================]')
            print('')
            print('> fitting estimator : ')
            print(str(self.level_estimator.get_params()) + ' ...')
            print('')
        self.level_estimator.fit(df_train.values, y_train.values)
        self._StackingClassifier__fitOK = True
        return self

    def predict_proba(self, df_test):
        """Predicts class probabilities for the test set using the meta-features.

        Parameters
        ----------
        df_test : pandas DataFrame of shape = (n_samples_test, n_features)
            The testing samples

        Returns
        -------
        array of shape = (n_samples_test, n_classes)
            The class probabilities of the testing samples.
        """
        if self._StackingClassifier__fitOK:
            df_test = self.transform(df_test)
            return self.level_estimator.predict_proba(df_test)
        raise ValueError('Call fit before !')

    def predict(self, df_test):
        """Predicts class for the test set using the meta-features.

        Parameters
        ----------
        df_test : pandas DataFrame of shape = (n_samples_test, n_features)
            The testing samples

        Returns
        -------
        array of shape = (n_samples_test,)
            The predicted classes.
        """
        if self._StackingClassifier__fitOK:
            df_test = self.transform(df_test)
            return self.level_estimator.predict(df_test)
        raise ValueError('Call fit before !')