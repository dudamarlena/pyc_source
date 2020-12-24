# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/building_custom_algorithms/with_baselines_or_sim.py
# Compiled at: 2019-01-04 08:05:49
# Size of source mod 2**32: 1738 bytes
"""
This module descibes how to build your own prediction algorithm. Please refer
to User Guide for more insight.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from surprise import AlgoBase
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise import PredictionImpossible

class MyOwnAlgorithm(AlgoBase):

    def __init__(self, sim_options={}, bsl_options={}):
        AlgoBase.__init__(self, sim_options=sim_options, bsl_options=bsl_options)

    def fit(self, trainset):
        AlgoBase.fit(self, trainset)
        self.bu, self.bi = self.compute_baselines()
        self.sim = self.compute_similarities()
        return self

    def estimate(self, u, i):
        if not (self.trainset.knows_user(u) and self.trainset.knows_item(i)):
            raise PredictionImpossible('User and/or item is unkown.')
        neighbors = [(v, self.sim[(u, v)]) for v, r in self.trainset.ir[i]]
        neighbors = sorted(neighbors, key=(lambda x: x[1]), reverse=True)
        print('The 3 nearest neighbors of user', str(u), 'are:')
        for v, sim_uv in neighbors[:3]:
            print('user {0:} with sim {1:1.2f}'.format(v, sim_uv))

        bsl = self.trainset.global_mean + self.bu[u] + self.bi[i]
        return bsl


data = Dataset.load_builtin('ml-100k')
algo = MyOwnAlgorithm()
cross_validate(algo, data, verbose=True)