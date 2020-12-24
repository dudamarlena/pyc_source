# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats2d/ex2d_ttest2.py
# Compiled at: 2019-08-22 04:44:49
# Size of source mod 2**32: 1223 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
eps = np.finfo(float).eps
dir0 = '/Users/todd/Dropbox/2019Sync/Documents/Projects/projectsOngoing/spm1d/ex2d/'
fname = dir0 + 'data2d.npy'
Y0 = np.load(fname)
y0 = np.array([yy.flatten() for yy in Y0])
J, Q = y0.shape
yA = y0[:10]
yB = y0[10:]
iA = yA.std(axis=0) > eps
iB = yB.std(axis=0) > eps
i = np.logical_and(iA, iB)
y = y0[:, i]
yA = y[:10]
yB = y[10:]
snpm = spm1d.stats.nonparam.ttest2(yA, yB)
snpmi = snpm.inference(0.05, two_tailed=True, iterations=1000)
z = snpmi.z
zstar = snpmi.zstar
z0 = np.zeros(Q)
z0[i] = z
Z0 = np.reshape(z0, Y0.shape[1:])
Z0i = Z0.copy()
Z0i[np.abs(Z0i) < zstar] = 0
ZZ = np.hstack([Z0, Z0i])
pyplot.close('all')
pyplot.figure()
ax = pyplot.axes()
ax.imshow((np.ma.masked_array(ZZ, ZZ == 0)), origin='lower', cmap='jet', vmin=(-15), vmax=15)
ax.set_title('SPM results')
ax.text(16, 10, 'Raw SPM', ha='center')
ax.text(48, 10, 'Inference', ha='center')
cb = pyplot.colorbar(mappable=(ax.images[0]))
cb.set_label('t value')
pyplot.show()