# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/init_model_param.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 2774 bytes
from federatedml.param.base_param import BaseParam

class InitParam(BaseParam):
    __doc__ = "\n    Initialize Parameters used in initializing a model.\n\n    Parameters\n    ----------\n    init_method : str, 'random_uniform', 'random_normal', 'ones', 'zeros' or 'const'. default: 'random_uniform'\n        Initial method.\n\n    init_const : int or float, default: 1\n        Required when init_method is 'const'. Specify the constant.\n\n    fit_intercept : bool, default: True\n        Whether to initialize the intercept or not.\n\n    "

    def __init__(self, init_method='random_uniform', init_const=1, fit_intercept=True, random_seed=None):
        super().__init__()
        self.init_method = init_method
        self.init_const = init_const
        self.fit_intercept = fit_intercept
        self.random_seed = random_seed

    def check(self):
        if type(self.init_method).__name__ != 'str':
            raise ValueError("Init param's init_method {} not supported, should be str type".format(self.init_method))
        else:
            self.init_method = self.init_method.lower()
            if self.init_method not in ('random_uniform', 'random_normal', 'ones',
                                        'zeros', 'const'):
                raise ValueError("Init param's init_method {} not supported, init_method should in 'random_uniform', 'random_normal' 'ones', 'zeros' or 'const'".format(self.init_method))
            else:
                if type(self.init_const).__name__ not in ('int', 'float'):
                    raise ValueError("Init param's init_const {} not supported, should be int or float type".format(self.init_const))
                if type(self.fit_intercept).__name__ != 'bool':
                    raise ValueError("Init param's fit_intercept {} not supported, should be bool type".format(self.fit_intercept))
                if self.random_seed is not None and type(self.random_seed).__name__ != 'int':
                    raise ValueError("Init param's random_seed {} not supported, should be int or float type".format(self.random_seed))
            return True