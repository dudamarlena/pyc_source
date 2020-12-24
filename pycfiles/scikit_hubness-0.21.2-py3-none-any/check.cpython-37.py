# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/utils/check.py
# Compiled at: 2019-10-11 04:29:10
# Size of source mod 2**32: 507 bytes
import numpy as np
__all__ = [
 'check_n_candidates']

def check_n_candidates(n_candidates):
    if n_candidates <= 0:
        raise ValueError(f"Expected n_neighbors > 0. Got {n_candidates:d}")
    if not np.issubdtype(type(n_candidates), np.integer):
        raise TypeError(f"n_neighbors does not take {type(n_candidates)} value, enter integer value")
    return n_candidates