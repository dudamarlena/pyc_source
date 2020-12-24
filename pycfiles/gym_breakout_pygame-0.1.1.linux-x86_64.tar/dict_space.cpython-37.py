# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marcofavorito/.pyenv/versions/3.7.6/lib/python3.7/site-packages/gym_breakout_pygame/wrappers/dict_space.py
# Compiled at: 2020-04-04 09:47:59
# Size of source mod 2**32: 1777 bytes
"""Breakout environments using a "dict" state space."""
from gym.spaces import Dict
from gym_breakout_pygame.breakout_env import BreakoutState
from gym_breakout_pygame.wrappers.skipper import BreakoutSkipper

class BreakoutDictSpace(BreakoutSkipper):
    __doc__ = 'A Breakout environment with a dictionary state space.\n    The components of the space are:\n    - Paddle x coordinate (Discrete)\n    - Ball x coordinate (Discrete)\n    - Ball y coordinate (Discrete)\n    - Ball horizontal speed (Discrete)\n    - Ball vertical speed (Discrete)\n    - Brick matrix (MultiBinary)\n    '

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        if self.config.ball_enabled:
            self.observation_space = Dict({'paddle_x':self._paddle_x_space, 
             'ball_x':self._ball_x_space, 
             'ball_y':self._ball_y_space, 
             'ball_x_speed':self._ball_x_speed_space, 
             'ball_y_speed':self._ball_y_speed_space, 
             'bricks_matrix':self._bricks_matrix_space})
        else:
            self.observation_space = Dict({'paddle_x':self._paddle_x_space, 
             'bricks_matrix':self._bricks_matrix_space})

    def observe(self, state: BreakoutState):
        """Observe the state."""
        dictionary = state.to_dict()
        if not self.config.ball_enabled:
            dictionary.pop('ball_x')
            dictionary.pop('ball_y')
            dictionary.pop('ball_x_speed')
            dictionary.pop('ball_y_speed')
        return dictionary

    @classmethod
    def compare(cls, obs1, obs2) -> bool:
        """Compare two observations."""
        return False