# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/Dropbox/Programming/heatrapy/heatrapy/fields/operating_mode.py
# Compiled at: 2019-02-18 06:24:11
# Size of source mod 2**32: 1678 bytes
"""Contains the function operating_mode.

Used to sweep applied and removed fields

"""
import numpy as np

def operating_mode(mode, time_before, time_after, field_steps, freq, j):
    period = 1.0 / freq
    if mode == 'constant_right':
        time_interval = (1 - time_after - time_before) * period / 2.0
        delta_t = time_interval / field_steps
        return delta_t
    if mode == 'accelerated_right':
        delta_t = 1 / (2 * (1.0 / (1.0 - time_after - time_before)) * freq * np.sqrt(field_steps)) * (np.sqrt(j + 1) - np.sqrt(j))
        return delta_t
    if mode == 'decelerated_right':
        delta_t = 1 / (2 * (1.0 / (1.0 - time_after - time_before)) * freq * np.sqrt(field_steps)) * (np.sqrt(field_steps - j) - np.sqrt(field_steps - j - 1))
        return delta_t
    if mode == 'constant_left':
        time_interval = (1 - time_after - time_before) * period / 2.0
        delta_t = time_interval / field_steps
        return delta_t
    if mode == 'accelerated_left':
        delta_t = 1 / (2 * (1.0 / (1.0 - time_after - time_before)) * freq * np.sqrt(field_steps)) * (np.sqrt(field_steps - j) - np.sqrt(field_steps - j - 1))
        return delta_t
    if mode == 'decelerated_left':
        delta_t = 1 / (2 * (1.0 / (1.0 - time_after - time_before)) * freq * np.sqrt(field_steps)) * (np.sqrt(j + 1) - np.sqrt(j))
        return delta_t
    print('invalid operating mode!')