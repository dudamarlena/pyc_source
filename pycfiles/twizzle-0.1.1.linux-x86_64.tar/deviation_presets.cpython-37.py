# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/twizzle/deviation_presets.py
# Compiled at: 2019-06-24 18:49:59
# Size of source mod 2**32: 358 bytes
"""
This module defines common functions to calculate the deviation between two hashes
"""
import numpy as np

def hamming_distance(array1, array2):
    if array1.size != array2.size:
        raise Exception('Arrays have to have the same size')
    hamming = array1 != array2
    return np.count_nonzero(hamming) / hamming.size