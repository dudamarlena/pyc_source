# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/building_custom_algorithms/most_basic_algorithm2.py
# Compiled at: 2019-01-04 08:05:49
# Size of source mod 2**32: 1051 bytes
"""
This module descibes how to build your own prediction algorithm. Please refer
to User Guide for more insight.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
from surprise import AlgoBase
from surprise import Dataset
from surprise.model_selection import cross_validate

class MyOwnAlgorithm(AlgoBase):

    def __init__(self):
        AlgoBase.__init__(self)

    def fit(self, trainset):
        AlgoBase.fit(self, trainset)
        self.the_mean = np.mean([r for _, _, r in self.trainset.all_ratings()])
        return self

    def estimate(self, u, i):
        return self.the_mean


data = Dataset.load_builtin('ml-100k')
algo = MyOwnAlgorithm()
cross_validate(algo, data, verbose=True)