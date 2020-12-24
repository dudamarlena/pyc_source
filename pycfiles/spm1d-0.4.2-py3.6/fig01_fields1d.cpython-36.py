# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/paper/fig01_fields1d.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 2388 bytes
import numpy as np
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


fig_width_mm = 240
fig_height_mm = 120
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
seed = [
 18] * 5 + [0]
nResponses = 8
nNodes = 101
W = [0, 5, 10, 20, 50, np.inf]
colors = scalar2color((range(nResponses + 3)), cmap=(cm.PuRd))
Y = []
for s, w in zip(seed, W):
    np.random.seed(s)
    Y.append(rft1d.random.randn1d(nResponses, nNodes, w))

pyplot.close('all')
axx, axy = np.linspace(0.04, 0.69, 3), [0.55, 0.09]
axw, axh = (0.295, 0.44)
AX = [pyplot.axes([xx, yy, axw, axh]) for yy in axy for xx in axx]
ax0, ax1, ax2 = AX[:3]
ax3, ax4, ax5 = AX[3:]
[ax.plot(yy, lw=0.8, color=c) for ax, y in zip(AX, Y) for yy, c in zip(y, colors[3:])]
[ax.hlines(0, 0, 100, color='k', linestyle='-', lw=2) for ax in AX]
pyplot.setp(AX, xlim=(0, 100), ylim=(-4.5, 4.5))
pyplot.setp((AX[:3]), xticklabels=[])
pyplot.setp([ax1, ax2, ax4, ax5], yticklabels=[])
[ax.set_xlabel('Field position  (%)') for ax in AX[3:]]
[ax.text((-0.15), 0.5, '$z$', size=24, transform=(ax.transAxes), rotation=90, va='center') for ax in (ax0, ax3)]
for i, (ax, w) in enumerate(zip(AX, W)):
    if np.isinf(w):
        s = '(%s)  FWHM = $\\infty$' % chr(97 + i)
    else:
        s = '(%s)  FWHM = %d%%' % (chr(97 + i), w)
    ax.text(0.05, 0.9, s, transform=(ax.transAxes), size=12)

pyplot.show()