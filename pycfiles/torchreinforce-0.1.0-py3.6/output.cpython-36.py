# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/torchreinforce/output.py
# Compiled at: 2019-01-18 11:50:58
# Size of source mod 2**32: 533 bytes


class ReinforceOutput:

    def __init__(self, distribution):
        self.distribution = distribution
        self.action = None
        self._reward = None
        self.used = False

    def get(self):
        self.action = self.distribution.sample()
        return self.action.item()

    def reward(self, reward):
        self._reward = reward

    def get_reward(self):
        return self._reward

    def _log_prob(self):
        self.used = True
        return self.distribution.log_prob(self.action).unsqueeze(0)