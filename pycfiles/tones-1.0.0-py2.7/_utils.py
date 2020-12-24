# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tones/_utils.py
# Compiled at: 2018-11-18 03:32:28
import math, tones

def _fade_up(data, start, end, istep=1, astep=0.005):
    amp = 0.0
    for i in range(start, end, istep):
        if amp >= 1.0:
            break
        data[i] *= amp
        amp += astep


def _translate(value, inmin, inmax, outmin, outmax):
    scaled = float(value - inmin) / float(inmax - inmin)
    return outmin + scaled * (outmax - outmin)


def _sine_sample(amp, freq, period, rate, i):
    return float(amp) * math.sin(2.0 * math.pi * float(freq) * (float(i % period) / float(rate)))