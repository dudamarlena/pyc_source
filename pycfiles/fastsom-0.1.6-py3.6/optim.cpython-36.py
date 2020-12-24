# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fastsom/learn/optim.py
# Compiled at: 2020-04-24 11:45:18
# Size of source mod 2**32: 1172 bytes
"""
Experimental.
Do not use
"""
from torch import Tensor
from torch.optim import Optimizer
from fastai.callback import OptimWrapper
__all__ = [
 'SplashOptimizer',
 'SomOptimizer']

class SplashOptimizer(Optimizer):
    __doc__ = 'Optimizer used `zero_grad`. But, it failed!'

    def __init__(self, params):
        defaults = dict(momentum=0.1, lr=0.1)
        super(SplashOptimizer, self).__init__(params, defaults)

    def __call__(self, *args, **kwargs):
        pass

    def zero_grad(self):
        pass

    def step(self, closure):
        pass


class SomOptimizer(Optimizer):
    __doc__ = 'Optimizer used to update `alpha` and `sigma` params.'

    def __init__(self, params, **defaults):
        defaults = dict(momentum=0.1)
        super().__init__(params, defaults)

    def __call__(self, *args, **kwargs):
        print(f"{self.__class__.__name__} has been called")

    def zero_grad(self):
        pass

    def step(self, closure=None):
        pass