# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\stochannpy\mccv.py
# Compiled at: 2018-02-07 04:12:49
# Size of source mod 2**32: 12916 bytes
"""
Author: Keurfon Luu <keurfon.luu@mines-paristech.fr>
License: MIT
"""
import numpy as np
from warnings import warn
from abc import ABCMeta, abstractmethod
from six import with_metaclass
from sklearn.base import BaseEstimator, ClassifierMixin, clone
from sklearn.utils import check_X_y, check_array
from sklearn.utils.validation import check_is_fitted
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from stochannpy import ENNClassifier
from joblib import Parallel, delayed, cpu_count
__all__ = [
 'MCCVClassifier']

class BaseMonteCarloCV(with_metaclass(ABCMeta, BaseEstimator)):
    __doc__ = "\n    Base class for Monte-Carlo Cross-Validation estimators.\n    \n    Do not use this class, please use derived classes.\n    \n    Parameters\n    ----------\n    base_estimator : object, optional, default None\n        The base estimator on which the Monte-Carlo Cross-Validation is\n        applied.\n    n_split : int, optional, default 1\n        Number of Monte-Carlo splits.\n    test_size : scalar, optional, default 0.5\n        Test size as a percentage of the number of data.\n    scoring : None or {'acurracy', 'precision', 'recall', 'f1, 'roc_auc'},\n        default None\n        Scoring method. If scoring = None, the estimator's score method is used.\n    n_jobs : int, optional, default 1\n        Number of jobs to run in parallel.\n    random_state : int, optional, default None\n        Seed for random number generator.\n    "

    @abstractmethod
    def __init__(self, base_estimator=None, n_split=1, test_size=0.5, scoring=None, n_jobs=1, random_state=None):
        self.base_estimator = base_estimator
        self.n_split = n_split
        self.test_size = test_size
        self.scoring = scoring
        self.n_jobs = n_jobs
        self.random_state = random_state

    def _validate_base_hyperparameters(self):
        if self.base_estimator is not None:
            if not isinstance(self.base_estimator, BaseEstimator):
                raise ValueError('base_estimator is not an actual estimator')
            else:
                if not isinstance(self.n_split, int) or self.n_split <= 0:
                    raise ValueError('n_split must be a positive integer, got %s' % self.n_split)
                if not isinstance(self.test_size, float):
                    if not isinstance(self.test_size, int):
                        if not 0 < self.test_size <= 1.0:
                            raise ValueError('test_size must be a positive scalar in ] 0, 1 ], got %s' % self.test_size)
                if self.scoring is not None:
                    if not isinstance(self.scoring, str) or self.scoring not in ('accuracy',
                                                                                 'precision',
                                                                                 'recall',
                                                                                 'f1',
                                                                                 'roc_auc'):
                        raise ValueError("scoring must either be 'accuracy', 'precision', 'recall', 'f1' or 'roc_auc', got %s" % self.scoring)
        else:
            if not isinstance(self.n_jobs, int) or self.n_jobs <= 0:
                max_cpu = cpu_count()
                if self.n_jobs > max_cpu:
                    self.n_jobs = max_cpu
                    warn('n_jobs cannot be greater than %s, n_jobs set to %s' % (
                     max_cpu, max_cpu), UserWarning)
                else:
                    raise ValueError('n_split must be a positive integer, got %s' % self.n_jobs)
            if self.random_state is not None:
                np.random.seed(self.random_state)

    def _compute_scores(self, X, y):
        """
        Compute a score for each estimator.
        
        Parameters
        ----------
        X : list of ndarray
            The ith element holds the test data for the ith estimator.
        y : list of ndarray
            The ith element holds the test targets for the ith estimator.
        
        Returns
        -------
        scores : ndarray
            The ith element holds the score of the ith estimator.
        """
        if self.scoring is None:
            scores = np.array([estimator.score(X[i], y[i]) for i, estimator in enumerate(self._estimators)])
        else:
            if self.scoring == 'accuracy':
                scores = np.array([accuracy_score(y[i], estimator.predict(X[i])) for i, estimator in enumerate(self._estimators)])
            else:
                if self.scoring == 'precision':
                    scores = np.array([precision_score(y[i], estimator.predict(X[i])) for i, estimator in enumerate(self._estimators)])
                else:
                    if self.scoring == 'recall':
                        scores = np.array([recall_score(y[i], estimator.predict(X[i])) for i, estimator in enumerate(self._estimators)])
                    else:
                        if self.scoring == 'f1':
                            scores = np.array([f1_score(y[i], estimator.predict(X[i])) for i, estimator in enumerate(self._estimators)])
                        else:
                            if self.scoring == 'roc_auc':
                                scores = np.array([roc_auc_score(y[i], estimator.predict(X[i])) for i, estimator in enumerate(self._estimators)])
        return scores

    def _shuffle(self, X, y):
        """
        Split input data into multiple train and test data.
        
        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Input data.
        y : ndarray of length n_samples
            Target values.
        
        Returns
        -------
        X_train : list of ndarray
            The ith element holds the train data for the ith estimator.
        y_train : list of ndarray
            The ith element holds the train targets for the ith estimator.
        X_test : list of ndarray
            The ith element holds the test data for the ith estimator.
        y_test : list of ndarray
            The ith element holds the test targets for the ith estimator.
        """
        n_train = int((1.0 - self.test_size) * X.shape[0])
        X_train, y_train, X_test, y_test = ([], [], [], [])
        for i in range(self.n_split):
            idx_train = np.random.permutation(X.shape[0])[:n_train]
            idx_test = np.ones((X.shape[0]), dtype=bool)
            idx_test[idx_train] = False
            X_train.append(X[idx_train, :])
            y_train.append(y[idx_train])
            X_test.append(X[idx_test, :])
            y_test.append(y[idx_test])

        return (
         X_train, y_train, X_test, y_test)

    def _predict(self, X):
        """
        Predict using the trained model.
        
        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Input data.
        
        Returns
        -------
        y_pred : ndarray of length n_samples
            Predicted labels.
        """
        check_is_fitted(self, 'scores_')
        X = check_array(X)
        classes = self.classes_[:, np.newaxis]
        weights = np.array(self.scores_ / np.sum(self.scores_))
        y_pred = np.array([weights[i] * (estimator.predict(X) == classes).T for i, estimator in enumerate(self._estimators)])
        return y_pred

    def _predict_proba(self, X):
        """
        Probability estimates.
        
        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Input data.
        
        Returns
        -------
        y_prob : ndarray of shape (n_samples, n_outputs)
            The ith row and jth column holds the probability of the ith sample
            to the jth class
        """
        check_is_fitted(self, 'scores_')
        X = check_array(X)
        weights = np.array(self.scores_ / np.sum(self.scores_))
        y_prob = np.array([weights[i] * estimator.predict_proba(X) for i, estimator in enumerate(self._estimators)])
        return y_prob


class MCCVClassifier(BaseMonteCarloCV, ClassifierMixin):
    __doc__ = "\n    Monte-Carlo Cross-Validation classifier.\n    \n    This classifier is a meta-estimator that performs multiple trainings with\n    the same classifier on different train and test data sets. The predictions\n    are weighted averages of the predictions from each trained estimator.\n    \n    Parameters\n    ----------\n    base_estimator : object, optional, default None\n        The base estimator on which the Monte-Carlo Cross-Validation is\n        applied.\n    n_split : int, optional, default 1\n        Number of Monte-Carlo splits.\n    test_size : scalar, optional, default 0.5\n        Test size as a percentage of the number of data.\n    scoring : None or {'acurracy', 'precision', 'recall', 'f1, 'roc_auc'},\n        default None\n        Scoring method. If scoring = None, the estimator's score method is used.\n    n_jobs : int, optional, default 1\n        Number of jobs to run in parallel.\n    random_state : int, optional, default None\n        Seed for random number generator.\n    \n    Examples\n    --------\n    Import the module and initialize the classifier:\n    \n    >>> import numpy as np\n    >>> from stochannpy import MCCVClassifier, ENNClassifier\n    >>> clf = MCCVClassifier(ENNClassifier(hidden_layer_sizes = (5,)))\n    \n    Fit the training set:\n    \n    >>> clf.fit(X_train, y_train)\n    \n    Predict the test set:\n    \n    >>> ypred = clf.predict(X_test)\n    \n    Compute the accuracy:\n    \n    >>> print(np.mean(ypred == y_test))\n    "

    def __init__(self, base_estimator=None, n_split=1, test_size=0.5, scoring=None, n_jobs=1, random_state=None):
        super(MCCVClassifier, self).__init__(base_estimator=base_estimator,
          n_split=n_split,
          test_size=test_size,
          scoring=scoring,
          n_jobs=n_jobs,
          random_state=random_state)

    def _validate_input(self, X, y):
        X, y = check_X_y(X, y)
        self._label_binarizer = LabelBinarizer()
        self._label_binarizer.fit(y)
        self.classes_ = self._label_binarizer.classes_
        return (X, y)

    def fit(self, X, y):
        """
        Fit the model to data matrix X and target y.
        
        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Input data.
        y : ndarray of length n_samples
            Target values.
        
        Returns
        -------
        self : returns a trained estimator.
        """
        if self.base_estimator is None:
            self.base_estimator_ = ENNClassifier()
        else:
            self.base_estimator_ = self.base_estimator
        self._validate_base_hyperparameters()
        X, y = self._validate_input(X, y)
        X_train, y_train, X_test, y_test = self._shuffle(X, y)
        self._estimators = [clone(self.base_estimator_) for i in range(self.n_split)]
        with Parallel(n_jobs=(self.n_jobs)) as (parallel):
            self._estimators = parallel(delayed(estimator.fit)(X_train[i], y_train[i]) for i, estimator in enumerate(self._estimators))
        self.scores_ = self._compute_scores(X_test, y_test)
        return self

    def predict(self, X):
        """
        Predict using the trained model.
        
        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Input data.
        
        Returns
        -------
        y_pred : ndarray of length n_samples
            Predicted labels.
        """
        y_pred = self._predict(X)
        y_pred = np.sum(y_pred, 0)
        return self.classes_.take(np.argmax(y_pred, axis=1), axis=0)

    def predict_log_proba(self, X):
        """
        Log of probability estimates.
        
        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Input data.
        
        Returns
        -------
        y_prob : ndarray of shape (n_samples, n_outputs)
            The ith row and jth column holds the log-probability of the ith
            sample to the jth class
        """
        return np.log(self.predict_proba(X))

    def predict_proba(self, X):
        """
        Probability estimates.
        
        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Input data.
        
        Returns
        -------
        y_prob : ndarray of shape (n_samples, n_outputs)
            The ith row and jth column holds the probability of the ith sample
            to the jth class
        """
        y_prob = self._predict_proba(X)
        y_prob = np.sum(y_prob, 0)
        return y_prob