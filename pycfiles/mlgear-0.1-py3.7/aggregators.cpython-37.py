# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/mlgear/aggregators.py
# Compiled at: 2019-12-27 10:16:19
# Size of source mod 2**32: 373 bytes
import numpy as np

def mean_diff(x):
    return np.mean(np.diff(np.sort(x)))


def std_diff(x):
    return np.std(np.diff(np.sort(x)))


def min_diff(x):
    return np.min(np.diff(np.sort(x)))


def max_diff(x):
    return np.max(np.diff(np.sort(x)))


def nth_smallest(x, n):
    return np.partition(x, n - 1)[(n - 1)]


def second_min(x):
    return nth_smallest(x, 2)