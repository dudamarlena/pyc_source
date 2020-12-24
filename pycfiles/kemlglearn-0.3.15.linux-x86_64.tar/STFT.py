# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/kemlglearn/time_series/decomposition/STFT.py
# Compiled at: 2017-04-24 03:45:20
"""
.. module:: SFFT

SFFT
*************

:Description: SFFT

    

:Authors: bejar
    

:Version: 

:Created on: 19/06/2015 11:36 

"""
__author__ = 'bejar'
import scipy, numpy as np

def stft(x, fftsize=1024, overlap=4, ban=0):
    """
    Short Time Fourier Transform

    :param x: Signal
    :param fftsize: Window length
    :param overlap: Overlaping between consecutive frequencies
    :param ban: numer of Frequencies to null
    :return:
    """
    hop = int(fftsize / overlap)
    w = scipy.hanning(fftsize + 1)[:-1]
    l = []
    for i in range(0, len(x) - fftsize, hop):
        v = np.fft.rfft(w * x[i:i + fftsize])
        for j in range(ban):
            v[j] = 0

        l.append(np.abs(v) ** 2 / np.max(np.abs(v) ** 2))

    return np.array(l)