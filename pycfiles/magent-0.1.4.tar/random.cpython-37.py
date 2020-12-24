# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mariojayakumar/Documents/School/2019_2020/Sem2/MAgent/python/magent/builtin/rule_model/random.py
# Compiled at: 2020-04-05 18:22:23
# Size of source mod 2**32: 495 bytes
"""A random agent"""
import numpy as np
from magent.model import BaseModel

class RandomActor(BaseModel):

    def __init__(self, env, handle, *args, **kwargs):
        BaseModel.__init__(self, env, handle)
        self.env = env
        self.handle = handle
        self.n_action = env.get_action_space(handle)[0]

    def infer_action(self, obs, *args, **kwargs):
        num = len(obs[0])
        actions = np.random.randint((self.n_action), size=num, dtype=(np.int32))
        return actions