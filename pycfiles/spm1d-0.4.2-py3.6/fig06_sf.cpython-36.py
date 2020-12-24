# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/paper/fig06_sf.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1901 bytes
import numpy as np
from scipy import stats
from matplotlib import pyplot, cm
from spm1d import rft1d

def scalar2color(x, cmap=cm.jet, xmin=None, xmax=None):
    x = np.asarray(x, dtype=float)
    if xmin is None:
        xmin = x.min()
    if xmax is None:
        xmax = x.max()
    xn = (x - xmin) / (xmax - xmin)
    xn *= 255
    xn = np.asarray(xn, dtype=int)
    colors = cmap(xn)
    return colors


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
nNodes = 101
WW = [5, 10, 20, 40, 100]
heights = np.linspace(2, 4, 21)
rftcalc = rft1d.prob.RFTCalculator(STAT='Z', nodes=nNodes, FWHM=(WW[0]), withBonf=False)
SFE = []
for W in WW:
    rftcalc.set_fwhm(W)
    sfE = rftcalc.p.upcrossing(heights)
    SFE.append(sfE)

sfN = stats.norm.sf(heights)
pyplot.close('all')
ax = pyplot.axes([0.15, 0.14, 0.82, 0.84])
colors = scalar2color((range(len(WW) + 2)), cmap=(cm.PuRd))
for W, sfE, c in zip(WW, SFE, colors[2:]):
    ax.plot(heights, sfE, '-', color=c, label=('FWHM = %d%%' % W))

ax.plot(heights, sfN, 'k-', lw=3, label='Standard normal')
ax.text(0.5, (-0.15), '$u$', size=20, transform=(ax.transAxes), ha='center')
ax.text((-0.17), 0.5, 'P ($z_{\\mathrm{max}}$ > $u$)', size=18, transform=(ax.transAxes), va='center', rotation=90)
ax.set_ylim(0, 0.35)
ax.legend()
pyplot.show()