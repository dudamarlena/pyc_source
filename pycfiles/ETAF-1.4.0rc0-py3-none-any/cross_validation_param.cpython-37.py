# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/cross_validation_param.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 2419 bytes
import copy
from federatedml.param.base_param import BaseParam
from federatedml.util import consts

class CrossValidationParam(BaseParam):
    __doc__ = "\n    Define cross validation params\n\n    Parameters\n    ----------\n    n_splits: int, default: 5\n        Specify how many splits used in KFold\n\n    mode: str, default: 'Hetero'\n        Indicate what mode is current task\n\n    role: str, default: 'Guest'\n        Indicate what role is current party\n\n    shuffle: bool, default: True\n        Define whether do shuffle before KFold or not.\n\n    random_seed: int, default: 1\n        Specify the random seed for numpy shuffle\n\n    need_cv: bool, default True\n        Indicate if this module needed to be run\n\n    "

    def __init__(self, n_splits=5, mode=consts.HETERO, role=consts.GUEST, shuffle=True, random_seed=1, need_cv=False):
        super(CrossValidationParam, self).__init__()
        self.n_splits = n_splits
        self.mode = mode
        self.role = role
        self.shuffle = shuffle
        self.random_seed = random_seed
        self.need_cv = need_cv

    def check(self):
        model_param_descr = "cross validation param's "
        self.check_positive_integer(self.n_splits, model_param_descr)
        self.check_valid_value((self.mode), model_param_descr, valid_values=[consts.HOMO, consts.HETERO])
        self.check_valid_value((self.role), model_param_descr, valid_values=[consts.HOST, consts.GUEST, consts.ARBITER])
        self.check_boolean(self.shuffle, model_param_descr)
        if self.random_seed is not None:
            self.check_positive_integer(self.random_seed, model_param_descr)