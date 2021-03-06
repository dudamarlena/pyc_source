# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\python362\Lib\site-packages\novainstrumentation\panthomkins\butterworth_filters.py
# Compiled at: 2017-03-06 22:19:14
# Size of source mod 2**32: 531 bytes
from novainstrumentation import filter

def butter_lowpass_filter(data, cutoff, fs):
    y = filter.lowpass(data, cutoff, order=2, fs=fs)
    return y


def butter_bandpass_filter(data, cutoffa, cutoffb, fs):
    y = filter.bandpass(data, cutoffa, cutoffb, fs=fs, order=2)
    return y


def butter_bandstop_filter(data, cutoffa, cutoffb, fs):
    y = filter.bandstop(data, cutoffa, cutoffb, fs=fs, order=2)
    return y


def butter_high_pass(data, cutoff, fs):
    y = filter.highpass(data, cutoff, order=2, fs=fs)
    return y