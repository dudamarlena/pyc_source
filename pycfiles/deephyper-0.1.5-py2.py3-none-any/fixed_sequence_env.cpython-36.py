# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/envs/fixed_sequence_env.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 1131 bytes
import numpy as np
from gym import Env
from gym.spaces import Discrete

class FixedSequenceEnv(Env):

    def __init__(self, n_actions=10, episode_len=100):
        self.np_random = np.random.RandomState()
        self.sequence = None
        self.action_space = Discrete(n_actions)
        self.observation_space = Discrete(1)
        self.episode_len = episode_len
        self.time = 0

    def reset(self):
        if self.sequence is None:
            self.sequence = [self.np_random.randint(0, self.action_space.n - 1) for _ in range(self.episode_len)]
        self.time = 0
        return 0

    def step(self, actions):
        rew = self._get_reward(actions)
        self._choose_next_state()
        done = False
        if self.episode_len:
            if self.time >= self.episode_len:
                rew = 0
                done = True
        return (
         0, rew, done, {})

    def seed(self, seed=None):
        self.np_random.seed(seed)

    def _choose_next_state(self):
        self.time += 1

    def _get_reward(self, actions):
        if actions == self.sequence[self.time]:
            return 1
        else:
            return 0