# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d/ex_anova1_circular_field.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 371 bytes
from matplotlib import pyplot
import spm1d
dataset = spm1d.data.uv1d.anova1.Weather()
Y, A = dataset.get_data()
Y0, Y1 = Y[(A == 0)], Y[(A == 2)]
t = spm1d.stats.ttest2(Y0, Y1)
ti = t.inference(0.05, circular=True)
print(ti)
pyplot.close('all')
ti.plot()
ti.plot_p_values()
pyplot.show()