# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mariojayakumar/Documents/School/2019_2020/Sem2/MAgent/python/magent/builtin/rule_model/runaway.py
# Compiled at: 2020-04-05 18:22:26
# Size of source mod 2**32: 1006 bytes
"""deprecated"""
import numpy as np
from magent.model import BaseModel
from magent.c_lib import _LIB, as_int32_c_array, as_float_c_array

class RunawayPrey(BaseModel):

    def __init__(self, env, handle, away_handle, *args, **kwargs):
        BaseModel.__init__(self, env, handle)
        self.away_channel = env.get_channel(away_handle)
        self.attack_base, _ = env.get_view2attack(handle)
        self.move_back = 4
        print('attack base', self.attack_base, 'away', self.away_channel)

    def infer_action(self, observations, *args, **kwargs):
        obs_buf = as_float_c_array(observations[0])
        hp_buf = as_float_c_array(observations[1])
        n, height, width, n_channel = observations[0].shape
        buf = np.empty((n,), dtype=(np.int32))
        act_buf = as_int32_c_array(buf)
        _LIB.runaway_infer_action(obs_buf, hp_buf, n, height, width, n_channel, self.attack_base, act_buf, self.away_channel, self.move_back)
        return buf