# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/summarystats/ex_plot_errorcloud.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 504 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
dataset = spm1d.data.uv1d.anova1.SpeedGRFcategorical()
Y, A = dataset.get_data()
Y0 = Y[(A == 1)]
Y1 = Y[(A == 2)]
Y2 = Y[(A == 3)]
datum = Y1.mean(axis=0)
err = np.linspace(0.1, 2.5, datum.size) ** 2
pyplot.close('all')
pyplot.plot(datum, 'b', lw=3)
spm1d.plot.plot_errorcloud(datum, err, facecolor='r', edgecolor='r')
pyplot.show()