# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d_roi/ex_anova3.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 857 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
dataset = spm1d.data.uv1d.anova3.SPM1D_ANOVA3_2x2x2()
Y, A, B, C = dataset.get_data()
roi = np.array([False] * Y.shape[1])
roi[60:] = True
alpha = 0.05
FF = spm1d.stats.anova3(Y, A, B, C, equal_var=True, roi=roi)
FFi = [F.inference(alpha) for F in FF]
pyplot.close('all')
titles = ['Main effect A',
 'Main effect B',
 'Main effect C',
 'Interaction AB',
 'Interaction AC',
 'Interaction BC',
 'Interaction ABC']
for i, Fi in enumerate(FFi):
    ax = pyplot.subplot(3, 3, i + 1)
    Fi.plot()
    ax.text(0.1, 0.85, (titles[i]), transform=(ax.transAxes))

pyplot.show()