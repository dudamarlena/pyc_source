# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fastsom/datasets/samplers.py
# Compiled at: 2020-04-24 11:45:18
# Size of source mod 2**32: 1085 bytes
"""
This module contains various PyTorch `Sampler` utilities.
"""
from enum import Enum
from torch.utils.data import Dataset, Sampler, RandomSampler, SequentialSampler
from typing import Union
from ..core import enum_eq
__all__ = [
 'SamplerType',
 'SamplerTypeOrString',
 'get_sampler']

class SamplerType(Enum):
    __doc__ = 'Enum used to pick PyTorch Samplers.'
    RANDOM = 'random'
    SHUFFLE = 'shuffle'
    SEQUENTIAL = 'seq'


SamplerTypeOrString = Union[(str, SamplerType)]

def get_sampler(st: SamplerTypeOrString, dataset: Dataset, bs: int) -> Sampler:
    """Creates the correct PyTorch sampler for the given `SamplerType`."""
    if enum_eq(SamplerType.RANDOM, st):
        return RandomSampler(dataset, replacement=True, num_samples=bs)
    else:
        if enum_eq(SamplerType.SHUFFLE, st):
            return RandomSampler(dataset, replacement=False)
        if enum_eq(SamplerType.SEQUENTIAL, st):
            return SequentialSampler(dataset)
        print(f'Unknown sampler "{str(st)}" requested; falling back to SequentialSampler.')
        return SequentialSampler(dataset)