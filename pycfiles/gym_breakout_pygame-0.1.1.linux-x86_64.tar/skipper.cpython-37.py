# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marcofavorito/.pyenv/versions/3.7.6/lib/python3.7/site-packages/gym_breakout_pygame/wrappers/skipper.py
# Compiled at: 2020-01-21 06:34:35
# Size of source mod 2**32: 1290 bytes
"""
This module contains a Gym wrapper that repeats the same action until the observation does not change.
"""
from abc import ABC, abstractmethod
from typing import Optional, Any
from gym_breakout_pygame.breakout_env import Breakout, BreakoutConfiguration

class BreakoutSkipper(Breakout, ABC):
    __doc__ = 'Repeat same step until a different observation is obtained.'

    def __init__(self, breakout_config=None):
        super().__init__(breakout_config)
        self._previous_obs = None

    @classmethod
    @abstractmethod
    def compare(cls, obs1, obs2):
        """Compare two observations"""
        return False

    def reset(self):
        obs = super().reset()
        self._previous_obs = obs
        return obs

    def step(self, action):
        obs, reward, is_finished, info = super().step(action)
        while self.compare(obs, self._previous_obs):
            next_obs, next_reward, next_is_finished, next_info = is_finished or super().step(action)
            obs = next_obs
            reward += next_reward
            is_finished = is_finished or next_is_finished
            info.update(next_info)

        self._previous_obs = obs
        return (obs, reward, is_finished, info)