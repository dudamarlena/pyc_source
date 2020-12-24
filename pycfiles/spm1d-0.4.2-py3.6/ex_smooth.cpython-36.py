# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/processing/ex_smooth.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 581 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
np.random.seed(0)
Y0 = np.random.randn(5, 101)
Y = spm1d.util.smooth(Y0, fwhm=5.0)
pyplot.close('all')
pyplot.figure(figsize=(8, 3.5))
ax0 = pyplot.axes((0.1, 0.15, 0.35, 0.8))
ax1 = pyplot.axes((0.55, 0.15, 0.35, 0.8))
ax0.plot(Y0.T, 'k')
ax1.plot(Y.T, 'k')
ax0.text(0.5, 0.9, 'Before smoothing', size=14, transform=(ax0.transAxes), ha='center')
ax1.text(0.5, 0.9, 'After smoothing', size=14, transform=(ax1.transAxes), ha='center')
pyplot.show()