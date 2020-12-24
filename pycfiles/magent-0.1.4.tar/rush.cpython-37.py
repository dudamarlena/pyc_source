# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mariojayakumar/Documents/School/2019_2020/Sem2/MAgent/python/magent/builtin/rule_model/rush.py
# Compiled at: 2020-04-05 18:22:28
# Size of source mod 2**32: 1243 bytes
"""deprecated"""
import ctypes, numpy as np
from magent.model import BaseModel
from magent.c_lib import _LIB, as_int32_c_array, as_float_c_array

class RushPredator(BaseModel):

    def __init__(self, env, handle, attack_handle, *args, **kwargs):
        BaseModel.__init__(self, env, handle)
        self.attack_channel = env.get_channel(attack_handle)
        self.attack_base, self.view2attack = env.get_view2attack(handle)
        print('attack_channel', self.attack_channel)
        print('view2attack', self.view2attack)

    def infer_action(self, observations, *args, **kwargs):
        obs_buf = as_float_c_array(observations[0])
        hp_buf = as_float_c_array(observations[1])
        n, height, width, n_channel = observations[0].shape
        buf = np.empty((n,), dtype=(np.int32))
        act_buf = as_int32_c_array(buf)
        attack_channel = self.attack_channel
        attack_base = self.attack_base
        view2attack_buf = as_int32_c_array(self.view2attack)
        _LIB.rush_prey_infer_action(obs_buf, hp_buf, n, height, width, n_channel, act_buf, attack_channel, attack_base, view2attack_buf, ctypes.c_float(100.0))
        return buf