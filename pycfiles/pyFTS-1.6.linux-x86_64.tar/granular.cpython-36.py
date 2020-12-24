# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/models/multivariate/granular.py
# Compiled at: 2019-04-12 12:32:25
# Size of source mod 2**32: 888 bytes
from pyFTS.models.multivariate import cmvfts, grid
from pyFTS.models import hofts

class GranularWMVFTS(cmvfts.ClusteredMVFTS):
    __doc__ = '\n    Granular multivariate weighted high order FTS\n    '

    def __init__(self, **kwargs):
        (super(GranularWMVFTS, self).__init__)(**kwargs)
        self.fts_method = hofts.WeightedHighOrderFTS
        self.model = None
        self.knn = kwargs.get('knn', 2)
        self.order = kwargs.get('order', 2)
        self.shortname = 'GranularWMVFTS'
        self.name = 'Granular Weighted Multivariate FTS'

    def train(self, data, **kwargs):
        self.partitioner = grid.IncrementalGridCluster(explanatory_variables=(self.explanatory_variables),
          target_variable=(self.target_variable),
          neighbors=(self.knn))
        (super(GranularWMVFTS, self).train)(data, **kwargs)