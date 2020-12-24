# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/dataset/mini_batch.py
# Compiled at: 2014-11-17 04:04:57
from abstract_dataset import AbstractDataset

class MiniBatches(AbstractDataset):

    def __init__(self, dataset, batch_size=20):
        self.origin = dataset
        self.size = batch_size

    def _yield_data(self, data, targets):
        for i in xrange(len(data) / self.size):
            yield (data[i:i + self.size], targets[i:i + self.size])

    def train_set(self):
        data, targets = self.origin.train_set()[0]
        return list(self._yield_data(data, targets))

    def test_set(self):
        data, targets = self.origin.test_set()[0]
        return list(self._yield_data(data, targets))

    def valid_set(self):
        data, targets = self.origin.valid_set()[0]
        return list(self._yield_data(data, targets))