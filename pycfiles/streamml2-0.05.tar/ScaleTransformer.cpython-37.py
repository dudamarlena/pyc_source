# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\bmccs\Desktop\streamml2\streamml2\streamline\transformation\transformers\ScaleTransformer.py
# Compiled at: 2019-01-19 21:05:43
# Size of source mod 2**32: 552 bytes
from ..AbstractTransformer import *
from sklearn.preprocessing import scale

class ScaleTransformer(AbstractTransformer):

    def __init__(self):
        AbstractTransformer.__init__(self, 'scale')

    def transform(self, X):
        assert (
         isinstance(X, pd.DataFrame), 'please ensure X is of type pd.DataFrame')
        columns = list(X.columns)
        return pd.DataFrame((scale(X)), columns=columns)