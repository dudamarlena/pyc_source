# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/paper/fig14_fwhm_estimation.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1697 bytes
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
fig_width_mm = 100
fig_height_mm = 80
mm2in = 0.03937007874015748
fig_width = fig_width_mm * mm2in
fig_height = fig_height_mm * mm2in
params = {'backend':'ps',  'axes.labelsize':14,  'font.size':12, 
 'text.usetex':False,  'legend.fontsize':12,  'xtick.labelsize':8, 
 'ytick.labelsize':8,  'font.family':'Times New Roman', 
 'lines.linewidth':0.5, 
 'patch.linewidth':0.25, 
 'figure.figsize':[
  fig_width, fig_height]}
pyplot.rcParams.update(params)
np.random.seed(0)
nResponses = 10
nNodes = 101
nIterations = 50
W = np.linspace(1, 50, 15)
We = []
for w in W:
    we = []
    for i in range(nIterations):
        y = rft1d.random.randn1d(nResponses, nNodes, w)
        we.append(rft1d.geom.estimate_fwhm(y))

    We.append(we)
    print('Actual FWHM: %06.3f, estimated FWHM: %06.3f' % (w, np.mean(We[(-1)])))

We = np.array(We)
pyplot.close('all')
ax = pyplot.axes([0.11, 0.14, 0.86, 0.84])
ax.plot(W, W, 'k-', lw=2, label='Actual')
ax.errorbar(W, We.mean(axis=1), yerr=We.std(ddof=1, axis=1), fmt='bo', ecolor='b', label='Estimated')
ax.legend(loc='upper left')
ax.set_xlabel('Actual  FWHM  (%)')
ax.set_ylabel('Estimated  FWHM  (%)')
pyplot.setp(ax, xlim=(0, 54), ylim=(0, 54))
pyplot.show()