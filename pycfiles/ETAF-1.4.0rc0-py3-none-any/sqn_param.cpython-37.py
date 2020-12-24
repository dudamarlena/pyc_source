# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/sqn_param.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 1814 bytes
from federatedml.param.base_param import BaseParam

class StochasticQuasiNewtonParam(BaseParam):
    __doc__ = '\n    Parameters used for stochastic quasi-newton method.\n\n    Parameters\n    ----------\n    update_interval_L : int, default: 3\n        Set how many iteration to update hess matrix\n\n    memory_M : int, default: 5\n        Stack size of curvature information, i.e. y_k and s_k in the paper.\n\n    sample_size: int, default: 5000\n        Sample size of data that used to update Hess matrix\n\n    '

    def __init__(self, update_interval_L=3, memory_M=5, sample_size=5000, random_seed=None):
        super().__init__()
        self.update_interval_L = update_interval_L
        self.memory_M = memory_M
        self.sample_size = sample_size
        self.random_seed = random_seed

    def check(self):
        descr = "hetero sqn param's"
        self.check_positive_integer(self.update_interval_L, descr)
        self.check_positive_integer(self.memory_M, descr)
        self.check_positive_integer(self.sample_size, descr)
        if self.random_seed is not None:
            self.check_positive_integer(self.random_seed, descr)
        return True