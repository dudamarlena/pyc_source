# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seismology/plotsource.py
# Compiled at: 2019-08-03 04:29:55
# Size of source mod 2**32: 1198 bytes
import numpy as np, source as S, matplotlib.pyplot as plt, obspy.imaging.beachball as BL
plt.rcParams
ex = S.SeismicSource([1, 2, 3, 4, 5, 6])
ex.Vavryeuk.plot('P', 'p')