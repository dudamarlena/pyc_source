# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats1d_roi/ex_hotellings2_Besier2009muscleforces.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 525 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
dataset = spm1d.data.mv1d.hotellings2.Besier2009muscleforces()
YA, YB = dataset.get_data()
print(dataset)
roi = np.array([False] * YA.shape[1])
roi[70:] = True
alpha = 0.05
T2 = spm1d.stats.hotellings2(YA, YB, roi=roi)
T2i = T2.inference(0.05)
print(T2i)
pyplot.close('all')
T2i.plot()
pyplot.show()