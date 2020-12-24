# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/google/home/rikel/bandits_repo/deep-bayesian-contextual-bandits/research/bandits/algorithms/fixed_policy_sampling.py
# Compiled at: 2018-07-23 14:29:50
# Size of source mod 2**32: 1786 bytes
"""Contextual bandit algorithm that selects an action at random."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
from bandits.core.bandit_algorithm import BanditAlgorithm

class FixedPolicySampling(BanditAlgorithm):
    __doc__ = 'Defines a baseline; returns an action at random with probs given by p.'

    def __init__(self, name, p, hparams):
        """Creates a FixedPolicySampling object.

    Args:
      name: Name of the algorithm.
      p: Vector of normalized probabilities corresponding to sampling each arm.
      hparams: Hyper-parameters, including the number of arms (num_actions).

    Raises:
      ValueError: when p dimension does not match the number of actions.
    """
        self.name = name
        self.p = p
        self.hparams = hparams
        if len(p) != self.hparams.num_actions:
            raise ValueError('Policy needs k probabilities.')

    def action(self, context):
        """Selects an action at random according to distribution p."""
        return np.random.choice((range(self.hparams.num_actions)), p=(self.p))