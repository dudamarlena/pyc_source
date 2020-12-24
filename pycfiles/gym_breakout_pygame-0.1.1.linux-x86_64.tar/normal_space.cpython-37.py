# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marcofavorito/.pyenv/versions/3.7.6/lib/python3.7/site-packages/gym_breakout_pygame/wrappers/normal_space.py
# Compiled at: 2020-01-21 06:34:35
# Size of source mod 2**32: 2392 bytes
"""Breakout environments using a "normal" state space.
- BreakoutNMultiDiscrete
- BreakoutNDiscrete
"""
from typing import Optional
import numpy as np
from gym.spaces import Discrete, MultiDiscrete
from gym_breakout_pygame.breakout_env import Breakout, BreakoutConfiguration, BreakoutState
from gym_breakout_pygame.utils import encode
from gym_breakout_pygame.wrappers.skipper import BreakoutSkipper

class BreakoutNMultiDiscrete(BreakoutSkipper):
    __doc__ = '\n    Breakout env with a gym.MultiDiscrete observation space composed by:\n    - paddle x position\n    - ball x position\n    - ball y position\n    - ball direction\n\n    '

    def __init__(self, config=None):
        super().__init__(config)
        self.observation_space = MultiDiscrete((
         self._paddle_x_space.n,
         self._ball_x_space.n,
         self._ball_y_space.n,
         self._ball_x_speed_space.n,
         self._ball_y_speed_space.n))

    @classmethod
    def compare(cls, obs1: np.ndarray, obs2: np.ndarray):
        return (obs1 == obs2).all()

    @classmethod
    def observe(cls, state: BreakoutState):
        paddle_x = state.paddle.x // state.config.resolution_x
        ball_x = state.ball.x // state.config.resolution_x
        ball_y = state.ball.y // state.config.resolution_y
        ball_x_speed = state.ball.speed_x_norm
        ball_y_speed = state.ball.speed_y_norm
        obs = [
         paddle_x, ball_x, ball_y, ball_x_speed, ball_y_speed]
        return np.asarray(obs)


class BreakoutNDiscrete(BreakoutSkipper):
    __doc__ = '\n    The same of BreakoutNMultiDiscrete, but the observation space encoded in one integer.\n    '

    def __init__(self, config=None):
        super().__init__(config)
        self.observation_space = Discrete(config.n_paddle_x * config.n_ball_x * config.n_ball_y * config.n_ball_x_speed * config.n_ball_y_speed)

    @classmethod
    def observe(cls, state: BreakoutState):
        obs = BreakoutNMultiDiscrete.observe(state)
        dims = [state.config.n_paddle_x, state.config.n_ball_x, state.config.n_ball_y,
         state.config.n_ball_x_speed, state.config.n_ball_y_speed]
        return encode(list(obs), dims)

    @classmethod
    def compare(cls, obs1, obs2):
        return obs1 == obs2