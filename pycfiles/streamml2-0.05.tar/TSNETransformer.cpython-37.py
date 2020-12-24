# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\bmccs\Desktop\streamml2\streamml2\streamline\transformation\transformers\TSNETransformer.py
# Compiled at: 2019-01-19 21:05:43
# Size of source mod 2**32: 720 bytes
from ..AbstractTransformer import *
from sklearn.manifold import TSNE

class TSNETransformer(AbstractTransformer):

    def __init__(self, ncomps):
        self._tsne_n_components = ncomps
        AbstractTransformer.__init__(self, 'scale')

    def transform(self, X):
        assert (
         isinstance(X, pd.DataFrame), 'please ensure X is of type pd.DataFrame')
        X_embedded = TSNE(n_components=(self._tsne_n_components)).fit_transform(X)
        cols = X_embedded.shape[1]
        columns = ['embedding_' + str(i) for i in range(cols)]
        return pd.DataFrame(X_embedded, columns=columns)