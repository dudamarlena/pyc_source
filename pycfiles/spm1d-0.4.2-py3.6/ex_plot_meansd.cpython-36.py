# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/summarystats/ex_plot_meansd.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 602 bytes
from matplotlib import pyplot
import spm1d
dataset = spm1d.data.uv1d.anova1.SpeedGRFcategorical()
Y, A = dataset.get_data()
Y0 = Y[(A == 1)]
Y1 = Y[(A == 2)]
Y2 = Y[(A == 3)]
pyplot.close('all')
spm1d.plot.plot_mean_sd(Y0, linecolor='b', facecolor=(0.7, 0.7, 1), edgecolor='b', label='Slow')
spm1d.plot.plot_mean_sd(Y1, label='Normal')
spm1d.plot.plot_mean_sd(Y2, linecolor='r', facecolor=(1, 0.7, 0.7), edgecolor='r', label='Fast')
pyplot.xlim(0, 100)
pyplot.xlabel('Time (%)', size=20)
pyplot.ylabel('VGRF  (BW)', size=20)
pyplot.legend(loc='lower left')
pyplot.show()