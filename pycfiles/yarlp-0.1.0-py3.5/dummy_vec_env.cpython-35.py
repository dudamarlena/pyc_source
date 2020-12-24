# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/baselines/common/vec_env/dummy_vec_env.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 1002 bytes
import numpy as np
from . import VecEnv

class DummyVecEnv(VecEnv):

    def __init__(self, env_fns):
        self.envs = [fn() for fn in env_fns]
        env = self.envs[0]
        VecEnv.__init__(self, len(env_fns), env.observation_space, env.action_space)
        self.ts = np.zeros(len(self.envs), dtype='int')
        self.actions = None

    def step_async(self, actions):
        self.actions = actions

    def step_wait(self):
        results = [env.step(a) for a, env in zip(self.actions, self.envs)]
        obs, rews, dones, infos = map(np.array, zip(*results))
        self.ts += 1
        for i, done in enumerate(dones):
            if done:
                obs[i] = self.envs[i].reset()
                self.ts[i] = 0

        self.actions = None
        return (np.array(obs), np.array(rews), np.array(dones), infos)

    def reset(self):
        results = [env.reset() for env in self.envs]
        return np.array(results)

    def close(self):
        pass