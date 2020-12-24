# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/google/home/rikel/bandits_repo/deep-bayesian-contextual-bandits/research/bandits/algorithms/uniform_sampling.py
# Compiled at: 2018-07-23 14:29:50
# Size of source mod 2**32: 1465 bytes
"""Contextual bandit algorithm that selects an action uniformly at random."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
from bandits.core.bandit_algorithm import BanditAlgorithm

class UniformSampling(BanditAlgorithm):
    __doc__ = 'Defines a baseline; returns one action uniformly at random.'

    def __init__(self, name, hparams):
        """Creates a UniformSampling object.

    Args:
      name: Name of the algorithm.
      hparams: Hyper-parameters, including the number of arms (num_actions).
    """
        self.name = name
        self.hparams = hparams

    def action(self, context):
        """Selects an action uniformly at random."""
        return np.random.choice(range(self.hparams.num_actions))