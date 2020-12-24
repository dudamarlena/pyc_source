# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/skmultilearn/base/mock.py
# Compiled at: 2018-09-03 19:16:42
from .base import MLClassifierBase

class MockClassifier(MLClassifierBase):
    """A stub classifier"""

    def __init__(self):
        super(MockClassifier, self).__init__()

    def fit(X, y):
        self.label_count = y.shape[1]
        return self

    def predict(X):
        return csr_matrix(np.ones(shape=(X.shape[0], self.label_count), dtype=int))