# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/torchreinforce/distributions/categorical.py
# Compiled at: 2019-01-18 12:12:17
# Size of source mod 2**32: 608 bytes
import torch
from .base import ReinforceDistribution

class Categorical(ReinforceDistribution, torch.distributions.Categorical):

    def __init__(self, probs, **kwargs):
        self.deterministic = kwargs['deterministic'] if 'deterministic' in kwargs else False
        self.probs = probs
        if 'deterministic' in kwargs:
            del kwargs['deterministic']
        (torch.distributions.Categorical.__init__)(self, probs, **kwargs)

    def sample(self):
        if self.deterministic:
            return self.probs.max(0)[1]
        else:
            return torch.distributions.Categorical.sample(self)