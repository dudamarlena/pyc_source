# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/vec_normalize.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 1535 bytes
from . import VecEnvWrapper
from deephyper.search.nas.baselines.common.running_mean_std import RunningMeanStd
import numpy as np

class VecNormalize(VecEnvWrapper):
    __doc__ = '\n    A vectorized wrapper that normalizes the observations\n    and returns from an environment.\n    '

    def __init__(self, venv, ob=True, ret=True, clipob=10.0, cliprew=10.0, gamma=0.99, epsilon=1e-08):
        VecEnvWrapper.__init__(self, venv)
        self.ob_rms = RunningMeanStd(shape=(self.observation_space.shape)) if ob else None
        self.ret_rms = RunningMeanStd(shape=()) if ret else None
        self.clipob = clipob
        self.cliprew = cliprew
        self.ret = np.zeros(self.num_envs)
        self.gamma = gamma
        self.epsilon = epsilon

    def step_wait(self):
        obs, rews, news, infos = self.venv.step_wait()
        self.ret = self.ret * self.gamma + rews
        obs = self._obfilt(obs)
        if self.ret_rms:
            self.ret_rms.update(self.ret)
            rews = np.clip(rews / np.sqrt(self.ret_rms.var + self.epsilon), -self.cliprew, self.cliprew)
        self.ret[news] = 0.0
        return (obs, rews, news, infos)

    def _obfilt(self, obs):
        if self.ob_rms:
            self.ob_rms.update(obs)
            obs = np.clip((obs - self.ob_rms.mean) / np.sqrt(self.ob_rms.var + self.epsilon), -self.clipob, self.clipob)
            return obs
        return obs

    def reset(self):
        self.ret = np.zeros(self.num_envs)
        obs = self.venv.reset()
        return self._obfilt(obs)