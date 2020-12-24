# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/paper/fig02_EC_HC.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 3951 bytes
import numpy as np
from matplotlib import pyplot
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from spm1d import rft1d
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

def plot_filled(y, ax, thresh=None, plot_thresh=True, color='k', lw=2, facecolor='0.8', two_tailed=False, thresh_color='k'):
    y = np.asarray(y, dtype=float)
    x = np.arange(y.size)
    if thresh is None:
        thresh = 0
    else:
        x0, y0, ind0 = x.copy(), y.copy(), np.arange(y.size)
        if two_tailed:
            L, n = rft1d.geom.bwlabel(np.abs(y) > thresh)
        else:
            L, n = rft1d.geom.bwlabel(y > thresh)
        ax.plot(x0, y0, color=color, lw=lw)
        if n > 0:
            polyg = []
            for i in range(n):
                ind = ind0[(L == i + 1)].tolist()
                x = x0[(L == i + 1)].tolist()
                y = y0[(L == i + 1)].tolist()
                csign = np.sign(y[0])
                x = [
                 x[0]] + x + [x[(-1)]]
                y = [csign * thresh] + y + [csign * thresh]
                if ind[0] != ind0[0]:
                    dx = x0[ind[0]] - x0[(ind[0] - 1)]
                    dy = (csign * thresh - y0[ind[0]]) / (y0[ind[0]] - y0[(ind[0] - 1)])
                    x[0] += dy * dx
                if ind[(-1)] != ind0[(-1)]:
                    dx = x0[(ind[(-1)] + 1)] - x0[ind[(-1)]]
                    dy = (csign * thresh - y0[ind[(-1)]]) / (y0[(ind[(-1)] + 1)] - y0[ind[(-1)]])
                    x[(-1)] += dy * dx
                polyg.append(Polygon(np.array((x, y)).T))

            patches = PatchCollection(polyg, edgecolors=None)
            ax.add_collection(patches)
            pyplot.setp(patches, facecolor=facecolor, edgecolor=facecolor)
        pyplot.setp(ax, xlim=(x0.min(), x0.max()))
        if thresh is not None:
            if plot_thresh:
                h = [
                 ax.hlines(thresh, x0.min(), x0.max())]
                if two_tailed:
                    h.append(ax.hlines(-thresh, x0.min(), x0.max()))
                pyplot.setp(h, color=thresh_color, lw=1, linestyle='--')


seeds = [
 100, 103, 201, 603, 201, 203]
pads = [True, True, True, False, True, False]
U = [1.5, 0.9, 1.0, 0.6, 0.0, 0.9]
nResponses = 1
nNodes = 101
W = 15
Y = []
for seed, pad in zip(seeds, pads):
    np.random.seed(seed)
    y = rft1d.random.randn1d(1, nNodes, W, pad=pad)
    Y.append(y)

pyplot.close('all')
color = (0.24, 0.41, 0.72)
axx, axy = np.linspace(0.04, 0.69, 3), [0.55, 0.09]
axw, axh = (0.295, 0.44)
AX = [pyplot.axes([xx, yy, axw, axh]) for yy in axy for xx in axx]
ax0, ax1, ax2 = AX[:3]
ax3, ax4, ax5 = AX[3:]
XPOS = [
 10, 80, 10, 82, 40, 45]
YPOS = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
for ax, y, u, xpos, ypos in zip(AX, Y, U, XPOS, YPOS):
    plot_filled(y, ax, thresh=u, plot_thresh=True, color=color, lw=2, facecolor=color, two_tailed=False, thresh_color='k')
    ax.text(xpos, u + ypos, '$u$ = %.1f' % u)

pyplot.setp(AX, xlim=(0, 100), ylim=(-2.5, 4.0))
pyplot.setp((AX[:3]), xticklabels=[])
pyplot.setp([ax1, ax2, ax4, ax5], yticklabels=[])
[ax.set_xlabel('Field position  (%)') for ax in AX[3:]]
[ax.text((-0.15), 0.5, '$z$', size=24, transform=(ax.transAxes), rotation=90, va='center') for ax in (ax0, ax3)]
EC = [
 1, 1, 0, 2, 1, 1]
HC = [1, 1, 1, 2, 2, 2]
for i, (ax, ec, hc) in enumerate(zip(AX, EC, HC)):
    s = '(%s)  EC=%d, HC=%d' % (chr(97 + i), ec, hc)
    ax.text(0.05, 0.9, s, transform=(ax.transAxes), size=12)

pyplot.show()