# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mara_kim/Documents/code/autochthe/kismet-py/kismet/distributions.py
# Compiled at: 2019-01-21 16:43:37
# Size of source mod 2**32: 3251 bytes
from numbers import Number
from pyro import distributions
import torch
from torch.distributions import constraints
from torch.distributions.utils import broadcast_all

class DiscreteUniform(distributions.TorchDistribution):
    __doc__ = '\n    Generates discrete uniformly distributed random samples from the interval\n    ``[low, high]``.\n    Example::\n        >>> m = DiscreteUniform(torch.tensor([0.0]), torch.tensor([5.0]))\n        >>> m.sample()  # uniformly distributed in the range [0.0, 5.0)\n        tensor([ 2.3418])\n    Args:\n        low (float or Tensor): lower range (inclusive).\n        high (float or Tensor): upper range (exclusive).\n    '
    arg_constraints = {'low':constraints.dependent, 
     'high':constraints.dependent}
    has_rsample = True

    @property
    def mean(self):
        return (self.high + self.low) / 2

    @property
    def stddev(self):
        return (self.high - self.low - 1) / 3.4641016151377544

    @property
    def variance(self):
        return (self.high - self.low + 1).pow(2) / 12

    def __init__(self, low, high, validate_args=None):
        self.low, self.high = broadcast_all(low, high)
        if isinstance(low, Number) and isinstance(high, Number):
            batch_shape = torch.Size()
        else:
            batch_shape = self.low.size()
        super(DiscreteUniform, self).__init__(batch_shape, validate_args=validate_args)
        if self._validate_args:
            if not torch.lt(self.low, self.high).all():
                raise ValueError('DiscreteUniform is not defined when low>= high')

    def expand(self, batch_shape, _instance=None):
        new = self._get_checked_instance(DiscreteUniform, _instance)
        batch_shape = torch.Size(batch_shape)
        new.low = self.low.expand(batch_shape)
        new.high = self.high.expand(batch_shape)
        super(DiscreteUniform, new).__init__(batch_shape, validate_args=False)
        new._validate_args = self._validate_args
        return new

    @constraints.dependent_property
    def support(self):
        return constraints.interval(self.low, self.high)

    def rsample(self, sample_shape=torch.Size()):
        shape = self._extended_shape(sample_shape)
        rand = torch.rand(shape, dtype=(self.low.dtype), device=(self.low.device))
        return torch.floor(self.low + rand * (self.high - self.low + 1)).type(torch.LongTensor)

    def log_prob(self, value):
        if self._validate_args:
            self._validate_sample(value)
        lb = value.ge(self.low).type_as(self.low)
        ub = value.lt(self.high).type_as(self.low)
        return torch.log(lb.mul(ub)) - torch.log(self.high - self.low + 1)

    def cdf(self, value):
        if self._validate_args:
            self._validate_sample(value)
        result = (value - self.low + 1) / (self.high - self.low + 1)
        return result.clamp(min=0, max=1)

    def icdf(self, value):
        if self._validate_args:
            self._validate_sample(value)
        result = value * (self.high - self.low + 1) + self.low - 1
        return result

    def entropy(self):
        return torch.log(self.high - self.low + 1)