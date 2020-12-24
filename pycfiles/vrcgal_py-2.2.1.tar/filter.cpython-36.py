# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benlong/Developer/git/vrcgal_py/vrcgal_py/filter.py
# Compiled at: 2017-08-19 09:51:05
# Size of source mod 2**32: 1075 bytes
from scipy.signal import butter, filtfilt

def bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return (b, a)


def lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    cut = cutoff / nyq
    b, a = butter(order, cut, btype='low')
    return (b, a)


def highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    cut = cutoff / nyq
    b, a = butter(order, cut, btype='high')
    return (b, a)


def bandpass_filter(data, lowcut, highcut, sample_rate, order=5):
    b, a = bandpass(lowcut, highcut, sample_rate, order=order)
    y = filtfilt(b, a, data)
    return y


def lowpass_filter(data, cutoff, sample_rate, order=5):
    b, a = lowpass(cutoff, sample_rate, order=order)
    y = filtfilt(b, a, data)
    return y


def highpass_filter(data, cutoff, sample_rate, order=5):
    b, a = highpass(cutoff, sample_rate, order=order)
    y = filtfilt(b, a, data)
    return y