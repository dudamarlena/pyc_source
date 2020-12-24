# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/weather_0_plotdata.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1064 bytes
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from matplotlib import pyplot
from spm1d import rft1d
weather = rft1d.data.weather()
y0 = weather['Atlantic']
y1 = weather['Pacific']
y2 = weather['Continental']
y3 = weather['Arctic']
y0 = gaussian_filter1d(y0, 8.0, axis=1, mode='wrap')
y1 = gaussian_filter1d(y1, 8.0, axis=1, mode='wrap')
y2 = gaussian_filter1d(y2, 8.0, axis=1, mode='wrap')
y3 = gaussian_filter1d(y3, 8.0, axis=1, mode='wrap')
pyplot.close('all')
labels = ['Atlantic', 'Pacific', 'Continental', 'Artic']
colors = ['r', 'g', 'b', 'k']
ax = pyplot.axes()
for y, color, label in zip((y0, y1, y2, y3), colors, labels):
    h = ax.plot((y.T), color=color)
    h[0].set_label(label)

ax.set_xlabel('Day', size=16)
ax.set_ylabel('Temperature', size=16)
ax.legend()
ax.set_title('Weather dataset (Ramsay et al. 2005)', size=20)
pyplot.show()