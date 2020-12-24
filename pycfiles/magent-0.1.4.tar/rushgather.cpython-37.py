# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mariojayakumar/Documents/School/2019_2020/Sem2/MAgent/python/magent/builtin/rule_model/rushgather.py
# Compiled at: 2020-04-05 18:22:30
# Size of source mod 2**32: 1105 bytes
"""gather agent, rush to food according to minimap"""
import numpy as np
from magent.model import BaseModel
from magent.c_lib import _LIB, as_int32_c_array, as_float_c_array

class RushGatherer(BaseModel):

    def __init__(self, env, handle, *args, **kwargs):
        BaseModel.__init__(self, env, handle)
        self.env = env
        self.handle = handle
        self.n_action = env.get_action_space(handle)
        self.view_size = env.get_view_space(handle)
        self.attack_base, self.view2attack = env.get_view2attack(handle)

    def infer_action(self, states, *args, **kwargs):
        obs_buf = as_float_c_array(states[0])
        hp_buf = as_float_c_array(states[1])
        n, height, width, n_channel = states[0].shape
        buf = np.empty((n,), dtype=(np.int32))
        act_buf = as_int32_c_array(buf)
        attack_base = self.attack_base
        view2attack_buf = as_int32_c_array(self.view2attack)
        _LIB.gather_infer_action(obs_buf, hp_buf, n, height, width, n_channel, act_buf, attack_base, view2attack_buf)
        return buf