# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/src/p_util/plots.py
# Compiled at: 2020-04-07 02:06:03
# Size of source mod 2**32: 185 bytes
import matplotlib.pyplot as plt
import neurodsp.spectral.power.compute_spectrum as computer_spectrum

def plotAll(signal, spikes):
    compute_spectrum(signal)
    plt.eventplot(spikes)