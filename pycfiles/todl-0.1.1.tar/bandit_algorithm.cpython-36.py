# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/google/home/rikel/bandits_repo/deep-bayesian-contextual-bandits/research/bandits/core/bandit_algorithm.py
# Compiled at: 2018-07-23 14:29:50
# Size of source mod 2**32: 1183 bytes
"""Define the abstract class for contextual bandit algorithms."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

class BanditAlgorithm(object):
    __doc__ = 'A bandit algorithm must be able to do two basic operations.\n\n  1. Choose an action given a context.\n  2. Update its internal model given a triple (context, played action, reward).\n  '

    def action(self, context):
        pass

    def update(self, context, action, reward):
        pass