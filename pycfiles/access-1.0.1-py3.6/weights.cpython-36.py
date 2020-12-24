# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/access/weights/weights.py
# Compiled at: 2020-02-24 17:09:30
# Size of source mod 2**32: 690 bytes
import numpy as np

def step_fn(step_dict):
    if type(step_dict) != dict:
        raise TypeError('step_dict must be of type dict.')
    for v in step_dict.values():
        if v < 0:
            raise ValueError('All weights must be positive.')

    def helper(key_to_test):
        for k, v in sorted(step_dict.items()):
            if key_to_test <= k:
                return v

        return 0

    return helper


def gaussian(width):
    if width == 0:
        raise ValueError('Width must be non-zero.')
    return lambda x: np.exp(-x * x / (2 * width ** 2)) / np.sqrt(2 * np.pi * width ** 2)


def gravity(scale=1, alpha=-1):
    return lambda x: np.power(x / scale, alpha)