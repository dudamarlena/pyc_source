# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/paper/fig12_val_set.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 2125 bytes
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
eps = np.finfo(float).eps
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
nResponses = 500
nNodes = 101
FWHM = 8.5
interp = True
wrap = True
heights = [2.0, 2.2, 2.4]
c = 2
y = rft1d.randn1d(nResponses, nNodes, FWHM)
calc = rft1d.geom.ClusterMetricCalculator()
rftcalc = rft1d.prob.RFTCalculator(STAT='Z', nodes=nNodes, FWHM=FWHM)
K0 = np.linspace(eps, 8, 21)
K = [[calc.cluster_extents(yy, h, interp, wrap) for yy in y] for h in heights]
C = np.array([[[sum([kkk >= k0 for kkk in kk]) for kk in k] for k in K] for k0 in K0])
P = np.mean((C >= c), axis=2).T
P0 = np.array([[rftcalc.p.set(c, k0, h) for h in heights] for k0 in K0 / FWHM]).T
pyplot.close('all')
colors = ['b', 'g', 'r']
ax = pyplot.axes([0.17, 0.14, 0.8, 0.84])
for color, p, p0, u in zip(colors, P, P0, heights):
    ax.plot(K0, p, 'o', color=color, markersize=5)
    ax.plot(K0, p0, '-', color=color, label=('$u$ = %.1f' % u))

ax.plot([0, 1], [10, 10], 'k-', label='Theoretical')
ax.plot([0, 1], [10, 10], 'ko-', label='Simulated', markersize=5)
ax.legend()
ax.set_xlabel('$k_\\mathrm{min}$', size=16)
ax.set_ylabel('$P(c | k_\\mathrm{min}) >= 2$', size=16)
ax.set_ylim(0, 0.08)
pyplot.show()