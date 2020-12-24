# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/models/incremental/TimeVariant.py
# Compiled at: 2019-02-27 12:31:52
# Size of source mod 2**32: 2914 bytes
__doc__ = '\nMeta model that wraps another FTS method and continously retrain it using a data window with the most recent data\n'
import numpy as np
from pyFTS.common import FuzzySet, FLR, fts, flrg
from pyFTS.partitioners import Grid

class Retrainer(fts.FTS):
    """Retrainer"""

    def __init__(self, **kwargs):
        (super(Retrainer, self).__init__)(**kwargs)
        self.partitioner_method = kwargs.get('partitioner_method', Grid.GridPartitioner)
        self.partitioner_params = kwargs.get('partitioner_params', {'npart': 10})
        self.partitioner = None
        self.fts_method = kwargs.get('fts_method', None)
        self.fts_params = kwargs.get('fts_params', {})
        self.model = None
        self.window_length = kwargs.get('window_length', 100)
        self.auto_update = False
        self.batch_size = kwargs.get('batch_size', 10)
        self.is_high_order = True
        self.uod_clip = False
        self.max_lag = self.window_length + self.order
        self.is_wrapper = True

    def train(self, data, **kwargs):
        self.partitioner = (self.partitioner_method)(data=data, **self.partitioner_params)
        self.model = (self.fts_method)(partitioner=self.partitioner, **self.fts_params)
        if self.model.is_high_order:
            self.model.order = self.model = (self.fts_method)(partitioner=self.partitioner, order=self.order, **self.fts_params)
        (self.model.fit)(data, **kwargs)
        self.shortname = self.model.shortname

    def forecast(self, data, **kwargs):
        l = len(data)
        horizon = self.window_length + self.order
        ret = []
        for k in np.arange(horizon, l + 1):
            _train = data[k - horizon:k - self.order]
            _test = data[k - self.order:k]
            if k % self.batch_size == 0 or self.model is None:
                if self.auto_update:
                    self.model.train(_train)
                else:
                    (self.train)(_train, **kwargs)
            ret.extend((self.model.predict)(_test, **kwargs))

        return ret

    def __str__(self):
        """String representation of the model"""
        return str(self.model)

    def __len__(self):
        """
        The length (number of rules) of the model

        :return: number of rules
        """
        return len(self.model)