# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d/ex_anova1_posthoc.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 1296 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
dataset = spm1d.data.uv1d.anova1.SpeedGRFcategorical()
Y, A = dataset.get_data()
Y1, Y2, Y3 = [Y[(A == u)] for u in np.unique(A)]
F = spm1d.stats.anova1(Y, A, equal_var=True)
Fi = F.inference(0.05)
alpha = 0.05
nTests = 3
p_critical = spm1d.util.p_critical_bonf(alpha, nTests)
t12 = spm1d.stats.ttest2(Y1, Y2, equal_var=False)
t13 = spm1d.stats.ttest2(Y1, Y3, equal_var=False)
t23 = spm1d.stats.ttest2(Y2, Y3, equal_var=False)
t12i = t12.inference(alpha=p_critical, two_tailed=True)
t13i = t13.inference(alpha=p_critical, two_tailed=True)
t23i = t23.inference(alpha=p_critical, two_tailed=True)
pyplot.close('all')
pyplot.subplot(221)
Fi.plot()
Fi.plot_threshold_label(bbox=dict(facecolor='w'))
pyplot.ylim(-1, 500)
pyplot.title('Main test')
pyplot.subplot(222)
t12i.plot()
pyplot.title('Posthoc:  1 vs. 2')
pyplot.ylim(-40, 40)
pyplot.subplot(223)
t23i.plot()
pyplot.title('Posthoc:  2 vs. 3')
pyplot.ylim(-40, 40)
pyplot.subplot(224)
t13i.plot()
pyplot.title('Posthoc:  1 vs. 3')
pyplot.ylim(-40, 40)
pyplot.show()