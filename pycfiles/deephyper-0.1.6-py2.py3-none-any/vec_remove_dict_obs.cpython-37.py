# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/vec_env/vec_remove_dict_obs.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 321 bytes
from .vec_env import VecEnvObservationWrapper

class VecExtractDictObs(VecEnvObservationWrapper):

    def __init__(self, venv, key):
        self.key = key
        super().__init__(venv=venv, observation_space=(venv.observation_space.spaces[self.key]))

    def process(self, obs):
        return obs[self.key]