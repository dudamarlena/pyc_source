# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d_roi/ex_hotellings_paired_Pataky2014.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 769 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
dataset = spm1d.data.mv1d.hotellings_paired.Pataky2014cop()
YA, YB = dataset.get_data()
print(dataset)
roi = np.array([False] * YA.shape[1])
roi[50:80] = True
alpha = 0.05
T2 = spm1d.stats.hotellings_paired(YA, YB, roi=roi)
T2i = T2.inference(0.05)
pyplot.close('all')
ax0 = pyplot.subplot(221)
ax1 = pyplot.subplot(222)
ax3 = pyplot.subplot(224)
ax0.plot((YA[:, :, 0].T), 'k', label='slow')
ax0.plot((YB[:, :, 0].T), 'r', label='fast')
ax1.plot(YA[:, :, 1].T, 'k')
ax1.plot(YB[:, :, 1].T, 'r')
T2i.plot(ax=ax3)
pyplot.show()