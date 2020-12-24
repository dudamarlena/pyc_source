# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/paper/fig03_EC.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 2655 bytes
from math import pi, log, sqrt, exp
import numpy as np
from scipy import stats
from matplotlib import pyplot
from spm1d import rft1d
fig_width_mm = 100
fig_height_mm = 80
mm2in = 0.03937007874015748
fig_width = fig_width_mm * mm2in
fig_height = fig_height_mm * mm2in
params = {'backend':'ps',  'axes.labelsize':14,  'font.size':12, 
 'text.usetex':False,  'legend.fontsize':11,  'xtick.labelsize':8, 
 'ytick.labelsize':8,  'font.family':'Times New Roman', 
 'lines.linewidth':0.5, 
 'patch.linewidth':0.25, 
 'figure.figsize':[
  fig_width, fig_height]}
pyplot.rcParams.update(params)

def here_expected_ec_0d(u):
    return stats.norm.sf(u)


def here_expected_ec_1d(Q, FWHM, u):
    return (Q - 1) / FWHM * sqrt(4 * log(2)) / (2 * pi) * exp(-0.5 * (u * u))


def here_ec(b):
    L, n = rft1d.geom.bwlabel(b)
    return n


np.random.seed(0)
nNodes = 101
FWHM = [5, 10, 25]
nIterations = 100
heights = np.linspace(0, 4, 21)
EC = []
for W in FWHM:
    y = rft1d.randn1d(nIterations, nNodes, W, pad=True)
    ec = np.array([[here_ec(yy > u) for u in heights] for yy in y]).mean(axis=0)
    EC.append(ec)

EC = np.array(EC)
E0, E1 = [], []
for W in FWHM:
    e0 = np.array([here_expected_ec_0d(u) for u in heights])
    e1 = np.array([here_expected_ec_1d(nNodes, W, u) for u in heights])
    E0.append(e0)
    E1.append(e1)

pyplot.close('all')
ax = pyplot.axes([0.11, 0.14, 0.86, 0.84])
colors = ['b', 'g', 'r']
for color, e0, e1, ec in zip(colors, E0, E1, EC):
    ax.plot(heights, e1, '--', color=color)
    ax.plot(heights, (e0 + e1), '-', color=color)
    ax.plot(heights, ec, 'o', color=color, markersize=5)

ax.plot([0, 1], [1000, 1000], 'k--', label='$EC$  (Hasofer, 1978)')
ax.plot([0, 1], [1000, 1000], 'k-', label='$HC$  (Worsley, 1995)')
ax.plot([0, 1], [1000, 1000], 'ko', label='Simulated', markersize=5)
for color, W in zip(colors, FWHM):
    ax.plot([0, 1], [1000, 1000], '-', lw=2, color=color, label=('FWHM = %d' % W))

ax.set_ylim(0, 6)
ax.legend()
ax.set_xlabel('$u$', size=18)
ax.set_ylabel('Topological characteristic', size=16)
pyplot.show()