# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/google/home/rikel/bandits_repo/deep-bayesian-contextual-bandits/research/bandits/core/bayesian_nn.py
# Compiled at: 2018-07-23 14:29:50
# Size of source mod 2**32: 1112 bytes
"""Define the abstract class for Bayesian Neural Networks."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

class BayesianNN(object):
    __doc__ = 'A Bayesian neural network keeps a distribution over neural nets.'

    def __init__(self, optimizer):
        pass

    def build_model(self):
        pass

    def train(self, data):
        pass

    def sample(self, steps):
        pass