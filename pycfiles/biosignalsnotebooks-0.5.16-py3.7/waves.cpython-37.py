# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\biosignalsnotebooks\external_packages\novainstrumentation\waves\waves.py
# Compiled at: 2020-03-23 15:40:39
# Size of source mod 2**32: 677 bytes
from numpy import *
import numpy as np

def waves(signal, events, lowerBound, upperBound):
    signal = [signal[center + lowerBound:center + upperBound] for center in events]
    x = np.array(list(filter(lambda i: upperBound - lowerBound == len(i), signal)))
    return x