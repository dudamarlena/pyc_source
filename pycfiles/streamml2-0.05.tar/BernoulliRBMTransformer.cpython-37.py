# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\bmccs\Desktop\streamml2\streamml2\streamline\transformation\transformers\BernoulliRBMTransformer.py
# Compiled at: 2019-01-19 21:05:43
# Size of source mod 2**32: 706 bytes
from ..AbstractTransformer import *
from sklearn.neural_network import BernoulliRBM

class BernoulliRBMTransformer(AbstractTransformer):

    def __init__(self):
        AbstractTransformer.__init__(self, 'brbm')

    def transform(self, X):
        brbm = BernoulliRBM(n_components=256, learning_rate=0.1,
          batch_size=10,
          n_iter=10,
          verbose=0,
          random_state=None)
        return pd.DataFrame(brbm.fit_transform(X))