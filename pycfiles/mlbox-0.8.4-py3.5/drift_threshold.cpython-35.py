# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mlbox/preprocessing/drift/drift_threshold.py
# Compiled at: 2020-04-13 16:34:29
# Size of source mod 2**32: 7828 bytes
import sys
from joblib import Parallel, delayed
from sklearn.tree import DecisionTreeClassifier
from .drift_estimator import DriftEstimator

def sync_fit(df_train, df_test, estimator, n_folds=2, stratify=True, random_state=1):
    """Compute the univariate drifts between df_train and df_test datasets.

    Multi-threaded version.

    Parameters
    ----------
    df_train : pandas dataframe of shape = (n_train, p)
        The train set

    df_test : pandas dataframe of shape = (n_test, p)
        The test set

    estimator : classifier, defaut = RandomForestClassifier(n_estimators = 50,
                                                            n_jobs=-1,
                                                            max_features=1.,
                                                            min_samples_leaf = 5,
                                                            max_depth = 5)
        The estimator that estimates the drift between two datasets

    n_folds : int, default = 2
        Number of folds used to estimate the drift

    stratify : bool, default = True
        Whether the cv is stratified (same number of train and test samples
        within each fold)

    random_state : int, default = 1
        Random state for cv

    Returns
    -------
    float
        drift measure

    """
    de = DriftEstimator(estimator, n_folds, stratify, random_state)
    de.fit(df_train, df_test)
    return de.score()


class DriftThreshold:
    __doc__ = 'Estimate the univariate drift between two datasets.\n\n    Estimate the univariate drift between two datasets\n    and select features with low drifts\n\n    Parameters\n    ----------\n    threshold : float, defaut = 0.6\n        The drift threshold (univariate drift below are kept)\n        Must be between 0. and 1.\n\n    subsample : float, defaut = 1.\n        Subsampling parameter for the datasets.\n        Must be between 0. and 1.\n\n    estimator : classifier, default = DecisionTreeClassifier(max_depth=6)\n        The estimator that estimates the drift between two datasets.\n\n    n_folds : int, default = 2\n        Number of folds used to estimate the drift.\n\n    stratify : bool, default = True\n        Whether the cv is stratified (same number of train and test samples\n        within each fold)\n\n    random_state : int, default = 1\n        Seed for for cv and subsampling.\n\n    n_jobs : int, defaut = -1\n        Number of cores used for processing (-1 for all cores)\n\n    '

    def __init__(self, threshold=0.6, subsample=1.0, estimator=DecisionTreeClassifier(max_depth=6), n_folds=2, stratify=True, random_state=1, n_jobs=-1):
        """Init a DriftThreshold object."""
        self.threshold = threshold
        self.subsample = subsample
        self.estimator = estimator
        self.n_folds = n_folds
        self.stratify = stratify
        self.random_state = random_state
        self.n_jobs = n_jobs
        self._DriftThreshold__Ddrifts = dict()
        self._DriftThreshold__fitOK = False

    def get_params(self):
        """Get parameters of a DriftThreshold object."""
        return {'threshold': self.threshold, 
         'subsample': self.subsample, 
         'estimator': self.estimator, 
         'n_folds': self.n_folds, 
         'stratify': self.stratify, 
         'random_state': self.random_state, 
         'n_jobs': self.n_jobs}

    def set_params(self, **params):
        """Set parameters of a DriftThreshold object."""
        if 'threshold' in params.keys():
            self.threshold = params['threshold']
        if 'subsample' in params.keys():
            self.subsample = params['subsample']
        if 'estimator' in params.keys():
            self.estimator = params['estimator']
        if 'n_folds' in params.keys():
            self.n_folds = params['n_folds']
        if 'stratify' in params.keys():
            self.stratify = params['stratify']
        if 'random_state' in params.keys():
            self.random_state = params['random_state']
        if 'n_jobs' in params.keys():
            self.n_jobs = params['n_jobs']

    def fit(self, df_train, df_test):
        """Compute the univariate drifts between df_train and df_test datasets.

        Parameters
        ----------
        df_train : pandas dataframe of shape = (n_train, p)
            The train set

        df_test : pandas dataframe of shape = (n_test, p)
            The test set

        Returns
        -------
        None

        """
        self._DriftThreshold__Ddrifts = dict()
        if sys.platform == 'win32':
            Ldrifts = [sync_fit(df_train.sample(frac=self.subsample)[[col]], df_test.sample(frac=self.subsample)[[col]], self.estimator, self.n_folds, self.stratify, self.random_state) for col in df_train.columns]
        else:
            Ldrifts = Parallel(n_jobs=self.n_jobs)(delayed(sync_fit)(df_train.sample(frac=self.subsample)[[col]], df_test.sample(frac=self.subsample)[[col]], self.estimator, self.n_folds, self.stratify, self.random_state) for col in df_train.columns)
        for i, col in enumerate(df_train.columns):
            self._DriftThreshold__Ddrifts[col] = Ldrifts[i]

        del Ldrifts
        self._DriftThreshold__fitOK = True

    def transform(self, df):
        """Select the features with low drift.

        Parameters
        ----------
        df : pandas dataframe
            A dataset with the same features

        Returns
        -------
        pandas DataFrame
            The transformed dataframe

        """
        if self._DriftThreshold__fitOK:
            selected_col = []
            for i, col in enumerate(df.columns):
                if self._DriftThreshold__Ddrifts[col] < self.threshold:
                    selected_col.append(col)

            return df[selected_col]
        raise ValueError('Call the fit function before !')

    def get_support(self, complement=False):
        """Return the variables kept or dropped.

        Parameters
        ----------
        complement : bool, default = True
            If True, returns the features to drop
            If False, returns the features to keep

        Returns
        -------
        list
            The list of features to keep or to drop.

        """
        if self._DriftThreshold__fitOK:
            keepList = []
            dropList = []
            for col in self._DriftThreshold__Ddrifts:
                if self._DriftThreshold__Ddrifts[col] < self.threshold:
                    keepList.append(col)
                else:
                    dropList.append(col)

            if complement:
                return dropList
            else:
                return keepList
        else:
            raise ValueError('Call the fit function before !')

    def drifts(self):
        """Return the univariate drifts for all variables.

        Returns
        -------
        dict
            The dictionnary of drift measures for each features

        """
        if self._DriftThreshold__fitOK:
            return self._DriftThreshold__Ddrifts
        raise ValueError('Call the fit function before !')