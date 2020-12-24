# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/projects_nils/photon_core/photonai/processing/cross_validation.py
# Compiled at: 2019-11-21 04:32:21
# Size of source mod 2**32: 5633 bytes
from sklearn.utils import check_random_state
from sklearn.model_selection._split import _BaseKFold
import numpy as np

class StratifiedKFoldRegression(_BaseKFold):
    __doc__ = 'Stratified K-Folds cross-validator for continuous target values (regression tasks)\n       Provides train/test indices to split data in train/test sets.\n       This cross-validation object is a variation of StratifiedKFold that returns\n       stratified folds with regard to a continuous target. The folds are made by first sorting\n       samples with respect to y. Subsequently, we step through each consecutive k samples and\n       randomly allocate exactly one of them to one of the test folds. For a detailed description\n       of the process see: http://scottclowe.com/2016-03-19-stratified-regression-partitions/.\n       Read more in the :ref:`User Guide <cross_validation>`.\n       Parameters\n       ----------\n       n_splits : int, default=3\n           Number of folds. Must be at least 2.\n       shuffle : boolean, optional\n           Whether to shuffle each stratification of the data before splitting\n           into batches.\n       random_state : int, RandomState instance or None, optional, default=None\n           If int, random_state is the seed used by the random number generator;\n           If RandomState instance, random_state is the random number generator;\n           If None, the random number generator is the RandomState instance used\n           by `np.random`. Used when ``shuffle`` == True.\n       Examples\n       --------\n       >>> from photonai.validation.cross_validation import StratifiedKFoldRegression\n       >>> X = np.array([[1, 2], [3, 4], [5, 6], [1, 2], [3, 4], [5, 6]])\n       >>> y = np.array([0, 1, 2, 3, 4, 5])\n       >>> skf = StratifiedKFoldRegression(n_splits=2)\n       >>> skf.get_n_splits(X, y)\n       2\n       >>> print(skf)  # doctest: +NORMALIZE_WHITESPACE\n       StratifiedKFoldRegression(n_splits=2, random_state=None, shuffle=False)\n       >>> for train_index, test_index in skf.split(X, y):\n       ...    print("TRAIN:", train_index, "TEST:", test_index)\n       ...    X_train, X_test = X[train_index], X[test_index]\n       ...    y_train, y_test = y[train_index], y[test_index]\n       TRAIN: [1 3 5] TEST: [0 2 4]\n       TRAIN: [0 2 4] TEST: [1 3 5]\n       Notes\n       -----\n       All the folds have size ``trunc(n_samples / n_splits)``, the last one has\n       the complementary.\n       '

    def __init__(self, n_splits=3, shuffle=False, random_state=None):
        super(StratifiedKFoldRegression, self).__init__(n_splits, shuffle, random_state)

    def _make_test_folds(self, X, y=None):
        rng = self.random_state
        n_splits = self.n_splits
        y = np.asarray(y)
        if y.ndim > 1:
            raise ValueError('Target data has more than one dimension. Must be single vector of continuous values.')
        n_samples = y.shape[0]
        self.n_samples = n_samples
        sort_indices = np.argsort(y)
        min_test_samples_per_fold = int(np.ceil(n_samples / n_splits))
        test_folds = [[] for _ in range(n_splits)]
        current = 0
        for i in range(min_test_samples_per_fold):
            start, stop = current, current + n_splits
            if i + 1 < min_test_samples_per_fold:
                subset = sort_indices[start:stop]
            else:
                subset = sort_indices[start:]
            if self.shuffle:
                check_random_state(rng).shuffle(subset)
            for k in range(len(subset)):
                test_folds[k].append(subset[k])

            current = stop

        return test_folds

    def _iter_test_masks(self, X, y, groups=None):
        test_folds = self._make_test_folds(X, y)
        for i in range(self.n_splits):
            test_mask = np.zeros((self.n_samples), dtype=(np.bool))
            test_mask[test_folds[i]] = True
            yield test_mask

    def split(self, X, y, groups=None):
        return super(StratifiedKFoldRegression, self).split(X, y, groups)


class OutlierKFold(_BaseKFold):

    def __init__(self, n_splits=3, shuffle=False, random_state=None):
        super(OutlierKFold, self).__init__(n_splits, shuffle, random_state)

    def _make_test_folds(self, X, y=None):
        rng = self.random_state
        n_splits = self.n_splits
        y = np.asarray(y)
        if y.ndim > 1:
            raise ValueError('Target data has more than one dimension. Must be single vector of continuous values.')
        n_samples = y.shape[0]
        self.n_samples = n_samples
        one_class = np.where(y == 1)[0]
        outlier = np.where(y == -1)[0]
        one_class_chunks = self.chunk_array(one_class)
        outlier_chunks = self.chunk_array(outlier)
        folds = [np.concatenate((i, j)) for i, j in zip(one_class_chunks, outlier_chunks)]
        return folds

    def chunk_array(self, index_list: list):
        num_samples = len(index_list)
        test_samples_per_fold = int(np.ceil(num_samples / self.n_splits))
        test_folds = []
        for i in range(0, num_samples, test_samples_per_fold):
            stop = i + test_samples_per_fold
            if stop > num_samples:
                stop = num_samples
            test_folds.append(index_list[i:stop])

        return test_folds

    def _iter_test_masks(self, X, y, groups=None):
        test_folds = self._make_test_folds(X, y)
        for i in range(self.n_splits):
            test_mask = np.zeros((self.n_samples), dtype=(np.bool))
            test_mask[test_folds[i]] = True
            yield test_mask

    def split(self, X, y, groups=None):
        return super(OutlierKFold, self).split(X, y, groups)