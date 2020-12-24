# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/dataset/mini_batch.py
# Compiled at: 2016-05-15 23:48:32
from . import Dataset
import numpy as np

class MiniBatches(Dataset):
    """
    Convert data into mini-batches.
    """

    def __init__(self, dataset, batch_size=20, cache=True):
        self.origin = dataset
        self.size = batch_size
        self._cached_train_set = None
        self._cached_valid_set = None
        self._cached_test_set = None
        self.cache = cache
        return

    def _yield_data(self, subset):
        for i in xrange(0, len(subset), self.size):
            yield map(np.array, list(zip(*subset[i:i + self.size])))

    def train_set(self):
        if self.cache and self._cached_train_set is not None:
            return self._cached_train_set
        else:
            data_generator = self._yield_data(self.origin.train_set())
            if data_generator is None:
                return
            if self.cache:
                self._cached_train_set = list(data_generator)
                return self._cached_train_set
            return data_generator
            return

    def test_set(self):
        if self.cache and self._cached_test_set is not None:
            return self._cached_test_set
        else:
            data_generator = self._yield_data(self.origin.test_set())
            if data_generator is None:
                return
            if self.cache:
                self._cached_test_set = list(data_generator)
                return self._cached_test_set
            return data_generator
            return

    def valid_set(self):
        if self.cache and self._cached_valid_set is not None:
            return self._cached_valid_set
        else:
            data_generator = self._yield_data(self.origin.valid_set())
            if data_generator is None:
                return
            if self.cache:
                self._cached_valid_set = list(data_generator)
                return self._cached_valid_set
            return data_generator
            return

    def train_size(self):
        train_size = self.origin.train_size()
        if train_size is None:
            train_size = len(list(self.origin.train_set()))
        return train_size / self.size