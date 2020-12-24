# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/vec_frame_stack.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 1150 bytes
from .vec_env import VecEnvWrapper
import numpy as np
from gym import spaces

class VecFrameStack(VecEnvWrapper):

    def __init__(self, venv, nstack):
        self.venv = venv
        self.nstack = nstack
        wos = venv.observation_space
        low = np.repeat((wos.low), (self.nstack), axis=(-1))
        high = np.repeat((wos.high), (self.nstack), axis=(-1))
        self.stackedobs = np.zeros((venv.num_envs,) + low.shape, low.dtype)
        observation_space = spaces.Box(low=low, high=high, dtype=(venv.observation_space.dtype))
        VecEnvWrapper.__init__(self, venv, observation_space=observation_space)

    def step_wait(self):
        obs, rews, news, infos = self.venv.step_wait()
        self.stackedobs = np.roll((self.stackedobs), shift=(-1), axis=(-1))
        for i, new in enumerate(news):
            if new:
                self.stackedobs[i] = 0

        self.stackedobs[..., -obs.shape[(-1)]:] = obs
        return (self.stackedobs, rews, news, infos)

    def reset(self):
        obs = self.venv.reset()
        self.stackedobs[...] = 0
        self.stackedobs[..., -obs.shape[(-1)]:] = obs
        return self.stackedobs