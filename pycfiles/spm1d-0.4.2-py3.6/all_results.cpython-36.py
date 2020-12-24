# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/paper/all_results.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 39888 bytes
"""
This script reproduces all figures and all code examples
from the paper. All are listed in the order in which
they appear in the paper.

NOTE 1:
Each code block (e.g. "Figure 1", "Page 8, Example 1")
is standalone. Thus all other blocks can be optionally
commented out to focus on just one code block.

NOTE 2:
Some of the figures in the paper were produced using
simulations with a large number of iterations. In this
script the numbers of iterations are reduced to reduce
processing times. To precisely reproduce the results
from the paper's figures, either:
1. Find the following flags in this script:
   "reproduce the results from the paper"
   and change the parameter as indicated.
or
2. Use the figure-specific scripts provided in:
   ./rft1d/examples/paper/fig*.py
"""
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
seed = [
 18] * 5 + [0]
nResponses = 8
nNodes = 101
W = [0, 5, 10, 20, 50, np.inf]
Y = []
for s, w in zip(seed, W):
    np.random.seed(s)
    Y.append(rft1d.random.randn1d(nResponses, nNodes, w))

pyplot.figure(1, figsize=(12, 6))
axx, axy = np.linspace(0.04, 0.69, 3), [0.55, 0.09]
axw, axh = (0.295, 0.44)
AX = [pyplot.axes([xx, yy, axw, axh]) for yy in axy for xx in axx]
ax0, ax1, ax2 = AX[:3]
ax3, ax4, ax5 = AX[3:]
[ax.plot(yy, lw=0.8, color='b') for ax, y in zip(AX, Y) for yy in y]
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

pyplot.show(block=False)
print('Figure 1 (Page 2):')
print('   [see Figure 1]')
print
import numpy as np
from matplotlib import pyplot
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from spm1d import rft1d
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

pyplot.figure(2, figsize=(12, 6))
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
    ax.plot(y, color=color, lw=2)
    ax.hlines(u, 0, 100, linestyle='--', color='k')
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
print('Figure 2 (Page 3):')
print('   [see Figure 2]')
print
from math import pi, sqrt, log, exp
import numpy as np
from scipy import stats
from matplotlib import pyplot
from spm1d import rft1d

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

pyplot.figure(3)
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
pyplot.show(block=False)
print('Figure 3 (Page 4):')
print('   [see Figure 3]')
print
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
np.random.seed(0)
nNodes = 101
FWHM = [5.0, 10.0, 25.0]
nResponses = 20
heights = np.linspace(1.0, 3.0, 11)
nodes = np.array([True] * nNodes)
nodes[20:35] = False
nodes[60:80] = False
nSegments = rft1d.geom.bwlabel(nodes)[1]
nNodesTotal = nodes.sum()
fieldSize = nNodesTotal - nSegments
y0 = rft1d.randn1d(nResponses, nodes, (FWHM[0]), pad=True)
y1 = rft1d.randn1d(nResponses, nodes, (FWHM[1]), pad=True)
y2 = rft1d.randn1d(nResponses, nodes, (FWHM[2]), pad=True)
pyplot.figure(4, figsize=(10, 4))
axx = np.linspace(0.04, 0.695, 3)
AX = [pyplot.axes([xx, 0.18, 0.29, 0.8]) for xx in axx]
ax0, ax1, ax2 = AX
[ax0.plot(yy, color='b') for yy in y0]
[ax1.plot(yy, color='b') for yy in y1]
[ax2.plot(yy, color='b') for yy in y2]
pyplot.setp(AX, xlim=(0, 100), ylim=(-3.8, 3.8))
pyplot.setp([ax1, ax2], yticklabels=[])
for i, (ax, w) in enumerate(zip(AX, FWHM)):
    s = '(%s)  FWHM = %d%%' % (chr(97 + i), w)
    ax.text(0.05, 0.9, s, transform=(ax.transAxes), size=12)

[ax.set_xlabel('Field position  (%)', size=18) for ax in AX]
ax0.text((-0.15), 0.5, '$z$', size=24, transform=(ax0.transAxes), rotation=90, va='center')
pyplot.show(block=False)
print('Figure 4 (Page 5):')
print('   [see Figure 4]')
print
from math import pi, log, sqrt, exp
import numpy as np
from scipy import stats
from matplotlib import pyplot
from spm1d import rft1d

def here_ec_0d(u, nSegments):
    return nSegments * stats.norm.sf(u)


def here_ec_1d(u, fieldSize, FWHM):
    return float(fieldSize) / W * sqrt(4 * log(2)) / (2 * pi) * exp(-0.5 * (u * u))


def here_ec_actual(yy, u):
    y = yy.copy()
    y[np.isnan(yy)] = -1000000000.0
    b = y > u
    L, n = rft1d.geom.bwlabel(b)
    return n


np.random.seed(0)
nNodes = 101
FWHM = [5.0, 10.0, 25.0]
nIterations = 100
heights = np.linspace(1.0, 3.0, 11)
nodes = np.array([True] * nNodes)
nodes[20:35] = False
nodes[60:80] = False
nSegments = rft1d.geom.bwlabel(nodes)[1]
nNodesTotal = nodes.sum()
fieldSize = nNodesTotal - nSegments
expectedEC = []
expectedECunbroken = []
for W in FWHM:
    EC0, EC0u = [], []
    for u in heights:
        ec0 = here_ec_0d(u, nSegments)
        ec1 = here_ec_1d(u, fieldSize, W)
        ec0u = here_ec_0d(u, 1)
        ec1u = here_ec_1d(u, fieldSize, W)
        EC0.append(ec0 + ec1)
        EC0u.append(ec0u + ec1u)

    expectedEC.append(EC0)
    expectedECunbroken.append(EC0u)

expectedEC = np.array(expectedEC)
expectedECunbroken = np.array(expectedECunbroken)
EC = []
for W in FWHM:
    y = rft1d.randn1d(nIterations, nodes, W, pad=True)
    ec = np.array([[here_ec_actual(yy, u) for u in heights] for yy in y]).mean(axis=0)
    EC.append(ec)

EC = np.array(EC)
pyplot.figure(5)
ax = pyplot.axes([0.11, 0.14, 0.86, 0.84])
colors = ['b', 'r', 'g']
for color, ec0, ec0u, ec in zip(colors, expectedEC, expectedECunbroken, EC):
    ax.plot(heights, ec0u, '-', lw=1, color=color)
    ax.plot(heights, ec0, ':', lw=2, color=color)
    ax.plot(heights, ec, 'o', color=color, markersize=5)

ax.plot([0, 1], [1000, 1000], 'k-', lw=1, label='Unbroken field')
ax.plot([0, 1], [1000, 1000], 'k:', lw=2, label='Broken field')
ax.plot([0, 1], [1000, 1000], 'ko', label='Simulated (broken field)', markersize=5)
for color, W in zip(colors, FWHM):
    ax.plot([0, 1], [1000, 1000], '-', lw=2, color=color, label=('FWHM = %d' % W))

ax.set_xlim(heights.min(), heights.max())
ax.set_ylim(0, EC.max())
ax.legend()
ax.set_xlabel('$u$', size=18)
ax.set_ylabel('Hadwiger characteristic', size=16)
pyplot.show(block=False)
print('Figure 5 (Page 6):')
print('   [see Figure 5]')
print
from scipy import stats
u = 2.0
p = stats.norm.sf(u)
print('Example 8.1 (Page 8):')
print('   p = stats.norm.sf(u) --> p = %.3f' % p)
print
from spm1d import rft1d
u = 3.0
nNodes = 101
FWHM = 10.0
p = rft1d.norm.sf(u, nNodes, FWHM)
print('Example 8.2 (Page 8):')
print('   p = rft1d.norm.sf(u, nNodes, FWHM) --> p = %.3f' % p)
print
from spm1d import rft1d
u = 3.0
nNodes = 101
FWHM = 10.0
p0 = rft1d.t.sf(u, 8, nNodes, FWHM)
p1 = rft1d.chi2.sf(u, 8, nNodes, FWHM)
p2 = rft1d.f.sf(u, (2, 15), nNodes, FWHM)
p3 = rft1d.T2.sf(u, (2, 15), nNodes, FWHM)
print('Example 8.3 (Page 8):')
print('   p = rft1d.t.sf(u, 8, nNodes, FWHM) --> p = %.3f' % p0)
print('   p = rft1d.chi2.sf(u, 8, nNodes, FWHM) --> p = %.3f' % p1)
print('   p = rft1d.f.sf(u, (2, 15), nNodes, FWHM) --> p = %.3f' % p2)
print('   p = rft1d.T2.sf(u, (2, 15), nNodes, FWHM) --> p = %.3f' % p3)
print
from spm1d import rft1d
alpha = 0.05
u = 3.0
nNodes = 101
FWHM = 10.0
u0 = rft1d.norm.isf(alpha, nNodes, FWHM)
u1 = rft1d.t.isf(alpha, 8, nNodes, FWHM)
u2 = rft1d.chi2.isf(alpha, 8, nNodes, FWHM)
u3 = rft1d.f.isf(alpha, (2, 15), nNodes, FWHM)
u4 = rft1d.T2.isf(alpha, (2, 15), nNodes, FWHM)
print('Example 8.4 (Pages 8-9):')
print('   u = rft1d.t.isf(alpha, 8, nNodes, FWHM) --> u = %.3f' % u0)
print('   u = rft1d.t.isf(alpha, 8, nNodes, FWHM) --> u = %.3f' % u1)
print('   u = rft1d.chi2.isf(alpha, 8, nNodes, FWHM) --> u = %.3f' % u2)
print('   u = rft1d.f.isf(alpha, (2, 15), nNodes, FWHM) --> u = %.3f' % u3)
print('   u = rft1d.T2.isf(alpha, (2, 15), nNodes, FWHM) --> u = %.3f' % u4)
print
import numpy as np
from scipy import stats
from matplotlib import pyplot
from spm1d import rft1d
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
pyplot.figure(6)
ax = pyplot.axes([0.15, 0.14, 0.82, 0.84])
for W, sfE in zip(WW, SFE):
    ax.plot(heights, sfE, '-', label=('FWHM = %d%%' % W))

ax.plot(heights, sfN, 'k-', lw=3, label='Standard normal')
ax.text(0.5, (-0.15), '$u$', size=20, transform=(ax.transAxes), ha='center')
ax.text((-0.17), 0.5, 'P ($z_{\\mathrm{max}}$ > $u$)', size=18, transform=(ax.transAxes), va='center', rotation=90)
ax.set_ylim(0, 0.35)
ax.legend()
pyplot.show(block=False)
print('Figure 6 (Page 9):')
print('   [see Figure 6]')
print
import numpy as np
from spm1d import rft1d
nNodes = 101
FWHM = 10.0
heights = np.linspace(2, 4, 51)
sf = rft1d.norm.sf(heights, nNodes, FWHM)
print('Example 9.1 (Page 9):')
print('    sf = rft1d.norm.sf(heights, nNodes, FWHM) --> ndarray (51,)')
print('    [see also Figure 6]')
print
from spm1d import rft1d
alpha = [
 0.001, 0.01, 0.05, 0.1]
nNodes = 101
FWHM = 10.0
u = rft1d.norm.isf(alpha, nNodes, FWHM)
print('Example 9.2 (Page 9):')
print('   u = rft1d.norm.isf(alpha, nNodes, FWHM) --> u = [%.3f, %.3f, %.3f, %.3f]' % tuple(u))
print
from spm1d import rft1d
nNodes = 101
FWHM = 8.0
k = 1.7 / FWHM
u = 3.0
p = rft1d.norm.p_cluster(k, u, nNodes, FWHM)
print('Example 10.1 (Page 10):')
print('   p = rft1d.norm.p_cluster(k, u, nNodes, FWHM) --> p = %.3f' % p)
print
from spm1d import rft1d
c = 2
nNodes = 101
FWHM = 8.0
k = 0.7 / FWHM
u = 3.0
p = rft1d.norm.p_set(c, k, u, nNodes, FWHM)
print('Example 10.2 (Page 10):')
print('   p = rft1d.norm.p_set(c, k, u, nNodes, FWHM) --> p = %.5f' % p)
print
from spm1d import rft1d
STAT = 'T'
df = (1, 19)
nNodes = 101
FWHM = 10.0
calc = rft1d.prob.RFTCalculator(STAT, df, nNodes, FWHM)
print('Example 10.3 (Page 10):')
print('   calc = rft1d.prob.RFTCalculator(STAT, df, nNodes, FWHM) --> an RFTCalculator object')
print
from spm1d import rft1d
STAT = 'T'
df = (1, 19)
nNodes = 101
FWHM = 10.0
calc = rft1d.prob.RFTCalculator(STAT, df, nNodes, FWHM)
u = 3.0
c = calc.expected.number_of_upcrossings(u)
k = calc.expected.resels_per_upcrossing(u)
N = calc.expected.number_of_suprathreshold_nodes(u)
print('Example 10.4 (Page 10):')
print('   c = calc.expected.number_of_upcrossings(u) --> c = %.3f' % c)
print('   k = calc.expected.resels_per_upcrossing(u) --> k = %.3f' % k)
print('   N = calc.expected.number_of_suprathreshold_nodes(u) --> N = %.3f' % N)
print
from spm1d import rft1d
STAT = 'T'
df = (1, 19)
nNodes = 101
FWHM = 10.0
calc = rft1d.prob.RFTCalculator(STAT, df, nNodes, FWHM)
u = 3.0
k = 0.2
c = 2
p0 = calc.p.upcrossing(u)
p1 = calc.p.cluster(k, u)
p2 = calc.p.set(c, k, u)
print('Example 11.1 (Page 11):')
print('   p = calc.p.upcrossing(u) --> p = %.3f' % p0)
print('   p = calc.p.cluster(k, u) --> p = %.3f' % p1)
print('   p = calc.p.sey(c, k, u) --> p = %.3f' % p2)
print
import scipy.optimize
from spm1d import rft1d
STAT = 'Z'
df = None
nNodes = 101
alpha = 0.05
p = lambda x: rft1d.prob.p_bonferroni(STAT, x, df, nNodes)
objective_fn = lambda x: (p(x) - alpha) ** 2
x0 = 5.0
u = scipy.optimize.fmin(objective_fn, x0, disp=0)
print('Example 11.2 (Page 11):')
print('   u = scipy.optimize.fmin(objective_fn, x0) --> u = %.3f' % u)
print
from spm1d import rft1d
u = 3.0
nNodes = 101
FWHM = 1.5
p0 = rft1d.norm.sf(u, nNodes, FWHM, withBonf=False)
p1 = rft1d.norm.sf(u, nNodes, FWHM, withBonf=True)
print('Example 11.3 (Page 11):')
print('   p0 = rft1d.norm.sf(u, nNodes, FWHM, withBonf=False) --> p0 = %.3f' % p0)
print('   p1 = rft1d.norm.sf(u, nNodes, FWHM, withBonf=True) --> p0 = %.3f' % p1)
print
from spm1d import rft1d
u = 3.0
nNodes = 101
FWHM = 5.0
p0 = rft1d.norm.sf(u, nNodes, FWHM, withBonf=False)
p1 = rft1d.norm.sf(u, nNodes, FWHM, withBonf=True)
print('Example 11.4 (Page 12):')
print('   p0 = rft1d.norm.sf(u, nNodes, FWHM, withBonf=False) --> p0 = %.3f' % p0)
print('   p1 = rft1d.norm.sf(u, nNodes, FWHM, withBonf=True) --> p0 = %.3f' % p1)
print
from spm1d import rft1d
y = rft1d.random.randn1d(20, 101, FWHM=10)
print('Example 12.2 (Page 12):')
print('   y = rft1d.random.randn1d(20, 101, FWHM=10) --> ndarray (20 x 101)')
print
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
nNodes = 101
FWHMs = [1, 2, 3]
heights = np.linspace(2.5, 4.0, 21)
rftcalc = rft1d.prob.RFTCalculator(STAT='Z', nodes=nNodes, FWHM=(FWHMs[0]), withBonf=False)
SFE = []
for W in FWHMs:
    rftcalc.set_fwhm(W)
    sfE = rftcalc.p.upcrossing(heights)
    SFE.append(sfE)

sfB = [rft1d.prob.p_bonferroni('Z', u, None, nNodes) for u in heights]
pyplot.figure(7)
ax = pyplot.axes([0.15, 0.14, 0.82, 0.84])
for W, sfE in zip(FWHMs, SFE):
    ax.plot(heights, sfE, '-', lw=2, label=('FWHM = %d%%' % W))

ax.plot(heights, sfB, 'k--', lw=4, label='Bonferroni')
ax.text(0.5, (-0.15), '$u$', size=20, transform=(ax.transAxes), ha='center')
ax.text((-0.17), 0.5, 'P ($z_{\\mathrm{max}}$ > $u$)', size=18, transform=(ax.transAxes), va='center', rotation=90)
ax.set_xlim(2.7, 3.6)
ax.set_ylim(0, 0.3)
ax.legend()
pyplot.show(block=False)
print('Figure 7 (Page 12):')
print('   [see Figure 7]')
print
import numpy as np
from scipy import optimize
from matplotlib import pyplot
from spm1d import rft1d
nNodes = 101
FWHMs = np.linspace(1, 5, 11)
ALPHAs = [0.001, 0.01, 0.05, 0.1]
ISFbonf = []
for alpha in ALPHAs:
    objfn = lambda x: (rft1d.prob.p_bonferroni('Z', x, None, nNodes) - alpha) ** 2
    x0 = 5.0
    ustar = optimize.fmin(objfn, 5, disp=0)
    ISFbonf.append(float(ustar))

rftcalc = rft1d.prob.RFTCalculator(STAT='Z', nodes=nNodes, FWHM=10, withBonf=False)
ISF = []
for W in FWHMs:
    rftcalc.set_fwhm(W)
    ISF.append([rftcalc.isf(alpha) for alpha in ALPHAs])

ISF = np.asarray(ISF).T
pyplot.figure(8)
ax = pyplot.axes([0.12, 0.14, 0.86, 0.84])
colors = ['b', 'g', 'r', 'orange']
for alpha, isf, isfbonf, color in zip(ALPHAs, ISF, ISFbonf, colors):
    ax.plot(FWHMs, isf, color=color, lw=1)
    ax.plot(FWHMs, ([isfbonf] * len(FWHMs)), '--', color=color, lw=1)

XY = [(0.31, 0.75), (0.35, 0.52), (0.3, 0.35), (0.1, 0.15)]
for xy, alpha, color in zip(XY, ALPHAs, colors):
    ax.text((xy[0]), (xy[1]), ('$\\alpha=%.3f$' % alpha), transform=(ax.transAxes), color=color)

ax.plot(FWHMs, ([100] * len(FWHMs)), 'k-', lw=1, label='RFT')
ax.plot(FWHMs, ([100] * len(FWHMs)), 'k--', lw=1, label='Bonferroni')
ax.legend()
ax.text(0.5, (-0.15), 'FWHM  (%)', size=16, transform=(ax.transAxes), ha='center')
ax.text((-0.14), 0.5, '$z^*$', size=20, transform=(ax.transAxes), va='center', rotation=90)
ax.set_ylim(2.5, 5)
pyplot.show(block=False)
print('Figure 8 (Page 13):')
print('   [see Figure 8]')
print
from spm1d import rft1d
y = rft1d.randn1d(20, 101, FWHM=10)
print('Example 13.1 (Page 13):')
print('   y = rft1d.randn1d(20, 101, FWHM=10) --> ndarray (20 x 101)')
print
import numpy as np
from spm1d import rft1d
np.random.seed(0)
yA = rft1d.randn1d(5, 101, FWHM=10)
yB = rft1d.randn1d(5, 101, FWHM=10)
np.random.seed(0)
yC = rft1d.randn1d(5, 101, FWHM=10)
bool0 = np.all(yA == yB)
bool1 = np.all(yA == yC)
print('Example 13.2 (Page 13):')
print('   np.all(yA == yB) --> %s' % bool0)
print('   np.all(yA == yC) --> %s' % bool1)
print
import numpy as np
from spm1d import rft1d
b = np.array([True] * 101)
b[20:30] = False
b[60:80] = False
y = rft1d.randn1d(20, b, FWHM=10)
print('Example 13.3 (Page 13):')
print('   y = rft1d.randn1d(20, b, FWHM=10) --> ndarray (20 x 101) {broken fields}')
print
import numpy as np
from scipy import stats
from matplotlib import pyplot
from spm1d import rft1d
np.random.seed(0)
nResponses = 500
nNodes = 101
WW = [5, 10, 20, 40]
heights = np.linspace(2, 4, 21)
SF = []
for W in WW:
    y = rft1d.random.randn1d(nResponses, nNodes, W, pad=True)
    sf = np.array([(y.max(axis=1) > h).mean() for h in heights])
    SF.append(sf)

calc = rft1d.prob.RFTCalculator(STAT='Z', nodes=nNodes, FWHM=(WW[0]), withBonf=False)
SFE = []
for W in WW:
    calc.set_fwhm(W)
    sfE = calc.sf(heights)
    SFE.append(sfE)

sfN = stats.norm.sf(heights)
pyplot.figure(9)
ax = pyplot.axes([0.15, 0.14, 0.82, 0.84])
colors = ['b', 'g', 'r', 'orange']
for W, sf, sfE, c in zip(WW, SF, SFE, colors):
    ax.plot(heights, sf, 'o', color=c, markersize=5, label=('FWHM = %d%%' % W))
    ax.plot(heights, sfE, '-', color=c)

ax.plot((heights[[0, -1]]), [2, 2], 'k-', label='Theoretical')
ax.plot(heights, sfN, 'k-', lw=3, label='Standard normal')
ax.text(0.5, (-0.15), '$u$', size=20, transform=(ax.transAxes), ha='center')
ax.text((-0.17), 0.5, 'P ($z_{\\mathrm{max}}$ > $u$)', size=18, transform=(ax.transAxes), va='center', rotation=90)
ax.set_ylim(0, 0.35)
ax.legend()
pyplot.show(block=False)
print('Figure 9 (Page 14):')
print('   [see Figure 9]')
print
import numpy as np
from spm1d import rft1d
nNodes = 101
FWHM = 10.0
y = rft1d.randn1d(1000, nNodes, FWHM)
ymax = y.max(axis=1)
u = 3.0
p_simulated = (ymax > u).mean()
p_expected = rft1d.norm.sf(u, nNodes, FWHM)
print('Example 14.1 (Page 14):')
print('   p_simulated = %.5f' % p_simulated)
print('   p_expected  = %.5f' % p_expected)
print
import numpy as np
from spm1d import rft1d
nNodes = 101
FWHM = 10.0
u = 3.0
calc = rft1d.geom.ClusterMetricCalculator()
interp = True
wrap = False
y = rft1d.randn1d(1000, nNodes, FWHM)
kmax = [calc.max_cluster_extent(yy, u, interp, wrap) for yy in y]
k0_nodes = 2.0
k0_resels = k0_nodes / FWHM
p_simulated = (np.array(kmax) >= k0_nodes).mean()
p_expected = rft1d.norm.p_cluster(k0_resels, u, nNodes, FWHM)
print('Example 14.2 (Pages 14-15):')
print('   p_simulated = %.5f' % p_simulated)
print('   p_expected  = %.5f' % p_expected)
print
import numpy as np
from spm1d import rft1d
nNodes = 101
FWHM = 10.0
u = 3.0
kmin_resels = 2.0 / FWHM
c = 2
calc = rft1d.geom.ClusterMetricCalculator()
interp = True
wrap = False
y = rft1d.randn1d(1000, nNodes, FWHM)
n = [calc.nUpcrossingsByExtent(yy, u, kmin_resels, interp, wrap) for yy in y]
p_simulated = (np.array(n) >= c).mean()
p_expected = rft1d.norm.p_set(c, kmin_resels, u, nNodes, FWHM)
print('Example 15.1 (Pages 15-16):')
print('   p_simulated = %.5f' % p_simulated)
print('   p_expected  = %.5f' % p_expected)
print
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
np.random.seed(0)
nNodes = 101
W = 20
h = 0.55
y = rft1d.random.randn1d(1, nNodes, W, pad=True)
pyplot.figure(10, figsize=(10, 4))
color0 = (0.24, 0.41, 0.72)
color1 = (0.74, 0.76, 0.89)
ax0 = pyplot.axes([0.06, 0.14, 0.44, 0.84])
ax1 = pyplot.axes([0.55, 0.14, 0.44, 0.84])
AX = (ax0, ax1)
for ax in [ax0, ax1]:
    ax.plot(y, color='k', lw=2)
    ax.hlines(0, 0, 100, color='k', linestyle='-', lw=0.5)
    ax.hlines(h, 0, 100, color=color0, linestyle='--')

ind = range(25, 38)
ax1.plot(ind, (y[ind]), 'o', markersize=6, markerfacecolor=color1, markeredgecolor=color0)
ax1.plot(ind, ([h] * len(ind)), 'o', markersize=6, markerfacecolor=color1, markeredgecolor=color0)
for i in ind:
    ax1.plot([i, i], [h, y[i]], '0.7')

ax1.text(31, 0.58, 'extent (nodes)', color='w', ha='center', size=14)
ax0.text(72, 0.4, 'threshold  $u$', color=color0, size=12)
ax0.plot((y.argmax()), (y.max()), 'o', markersize=5, markerfacecolor='w', markeredgecolor=color0)
ax1.plot((y.argmax()), (y.max()), 'o', markersize=12, markerfacecolor='w', markeredgecolor=color0)
ax0.plot(([48] * 2), [0, y.max()], '-', lw=3, marker='<', color=color0)
ax0.text(52, (y.max()), 'maximum height  $z_{\\mathrm{max}}$', color=color0, size=12)
ax1.hlines(h, 0, 100, color=color0, linestyle='-', lw=3)
ax1.plot([24.1, 37.9], ([0.519] * 2), '^-', lw=3, color=color0)
ax1.text(31, 0.49, 'extent (interpolated)', color=color0, ha='center', size=14)
[ax.set_xlabel('Field position  (%)') for ax in AX]
ax0.text((-0.15), 0.5, '$z$', size=24, transform=(ax0.transAxes), rotation=90, va='center')
pyplot.setp(ax0, xlim=(0, 100), ylim=(-1.2, 1.2))
pyplot.setp(ax1, xlim=(23, 39), ylim=(0.47, 0.92))
ax0.text(0.04, 0.91, '(a) Upcrossing', transform=(ax0.transAxes))
ax1.text(0.04, 0.91, '(b) Upcrossing  (zoomed)', transform=(ax1.transAxes))
pyplot.show(block=False)
print('Figure 10 (Page 15):')
print('   [see Figure 10]')
print
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
eps = np.finfo(float).eps
np.random.seed(0)
nResponses = 1000
nNodes = 101
FWHM = 10.0
interp = True
wrap = True
heights = [2.2, 2.4, 2.6, 2.8]
y = rft1d.randn1d(nResponses, nNodes, FWHM)
calc = rft1d.geom.ClusterMetricCalculator()
rftcalc = rft1d.prob.RFTCalculator(STAT='Z', nodes=nNodes, FWHM=FWHM)
K0 = np.linspace(eps, 15, 21)
K = np.array([[calc.max_cluster_extent(yy, h, interp, wrap) for yy in y] for h in heights])
P = np.array([(K >= k0).mean(axis=1) for k0 in K0]).T
P0 = np.array([[rftcalc.p.cluster(k0, h) for k0 in K0 / FWHM] for h in heights])
pyplot.figure(11)
colors = ['b', 'g', 'r', 'orange']
labels = ['$u$ = %.1f' % h for h in heights]
ax = pyplot.axes([0.17, 0.14, 0.8, 0.84])
for color, p, p0, label in zip(colors, P, P0, labels):
    ax.plot(K0, p, 'o', color=color, markersize=5)
    ax.plot(K0, p0, '-', color=color, label=label)

ax.plot([0, 1], [10, 10], 'k-', label='Theoretical')
ax.plot([0, 1], [10, 10], 'ko-', label='Simulated', markersize=5)
ax.legend()
ax.set_xlabel('$x$', size=16)
ax.set_ylabel('$P(k_{max}) > x$', size=16)
ax.set_ylim(0, 0.25)
pyplot.show(block=False)
print('Figure 11 (Page 16):')
print('   [see Figure 11]')
print
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
eps = np.finfo(float).eps
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
pyplot.figure(12)
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
pyplot.show(block=False)
print('Figure 12 (Page 17):')
print('   [see Figure 12]')
print
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from spm1d import rft1d
weather = rft1d.data.weather()
yA, yB = weather['Atlantic'], weather['Continental']
yA = gaussian_filter1d(yA, 8.0, axis=1, mode='wrap')
yB = gaussian_filter1d(yB, 8.0, axis=1, mode='wrap')
mA, mB = yA.mean(axis=0), yB.mean(axis=0)
rA, rB = yA - mA, yB - mB
r = np.vstack([rA, rB])
FWHM = rft1d.geom.estimate_fwhm(r)
print('Example 17.1 (Page 17):')
print('   Estimated smoothness:  FWHM = %.1f' % FWHM)
print
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from matplotlib import pyplot
from spm1d import rft1d
weather = rft1d.data.weather()
y0 = weather['Atlantic']
y1 = weather['Pacific']
y2 = weather['Continental']
y3 = weather['Arctic']
y0 = gaussian_filter1d(y0, 8.0, axis=1, mode='wrap')
y1 = gaussian_filter1d(y1, 8.0, axis=1, mode='wrap')
y2 = gaussian_filter1d(y2, 8.0, axis=1, mode='wrap')
y3 = gaussian_filter1d(y3, 8.0, axis=1, mode='wrap')
pyplot.figure(13)
labels = ['Atlantic', 'Pacific', 'Continental', 'Artic']
colors = ['r', 'g', 'b', 'k']
ax = pyplot.axes([0.13, 0.15, 0.84, 0.83])
for y, color, label in zip((y0, y1, y2, y3), colors, labels):
    h = ax.plot((y.T), color=color)
    h[0].set_label(label)

ax.legend(loc='lower center')
ax.set_xlabel('Day', size=16)
ax.set_ylabel('Temperature', size=16)
ax.set_ylim(-45, 25)
pyplot.show(block=False)
print('Figure 13 (Page 18):')
print('   [see Figure 13]')
print
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
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

We = np.array(We)
pyplot.figure(14)
ax = pyplot.axes([0.11, 0.14, 0.86, 0.84])
ax.plot(W, W, 'k-', lw=2, label='Actual')
ax.errorbar(W, We.mean(axis=1), yerr=We.std(ddof=1, axis=1), fmt='bo', ecolor='b', label='Estimated')
ax.legend(loc='upper left')
ax.set_xlabel('Actual  FWHM  (%)')
ax.set_ylabel('Estimated  FWHM  (%)')
pyplot.setp(ax, xlim=(0, 54), ylim=(0, 54))
pyplot.show(block=False)
print('Figure 14 (Page 18):')
print('   [see Figure 14]')
print
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
import scipy.stats
from matplotlib import pyplot
from spm1d import rft1d
weather = rft1d.data.weather()
yA, yB = weather['Atlantic'], weather['Continental']
yA = gaussian_filter1d(yA, 8.0, axis=1, mode='wrap')
yB = gaussian_filter1d(yB, 8.0, axis=1, mode='wrap')
nA, nB = yA.shape[0], yB.shape[0]
mA, mB = yA.mean(axis=0), yB.mean(axis=0)
sA, sB = yA.std(ddof=1, axis=0), yB.std(ddof=1, axis=0)
s = np.sqrt(((nA - 1) * sA * sA + (nB - 1) * sB * sB) / (nA + nB - 2))
t = (mA - mB) / (s * np.sqrt(1.0 / nA + 1.0 / nB))
rA, rB = yA - mA, yB - mB
r = np.vstack([rA, rB])
FWHM = rft1d.geom.estimate_fwhm(r)
alpha = 0.05
df = nA + nB - 2
Q = yA.shape[1]
tstar = rft1d.t.isf(alpha, df, Q, FWHM)
calc = rft1d.geom.ClusterMetricCalculator()
k = calc.cluster_extents(t, tstar, interp=True)
k_resels = [kk / FWHM for kk in k]
nClusters = len(k)
rftcalc = rft1d.prob.RFTCalculator(STAT='T', df=(1, df), nodes=Q, FWHM=FWHM)
Pset = rftcalc.p.set(nClusters, min(k_resels), tstar)
Pcluster = [rftcalc.p.cluster(kk, tstar) for kk in k_resels]
pyplot.figure(15)
ax = pyplot.axes([0.08, 0.15, 0.89, 0.83])
ax.plot(t, 'k', lw=3, label='t field')
ax.plot([0, Q], ([tstar] * 2), 'r--', label='Critical threshold')
ax.legend(loc='upper left')
ax.text(10, 2.8, ('p = %.3f' % Pcluster[0]), size=10)
ax.text(275, 3.5, ('p = %.3f' % Pcluster[1]), size=10)
ax.text(280, 2.1, ('$\\alpha$ = %.3f' % alpha), color='r')
ax.set_xlabel('Day', size=16)
ax.set_ylabel('t value', size=16)
pyplot.show(block=False)
print('Figure 15 & Example 19.1 (Sections 5.3-5.4, Pages 19-20):')
print('   [see Figure 15]')
print('   Critical t value (1D RFT):  t = %.3f' % tstar)
print('   Critical t value (0D):  t = %.3f' % scipy.stats.t.isf(alpha, df))
print('   Probability (set-level):  p = %.6f' % Pset)
print('   Probability (cluster-level):  p = %.3f, %.3f' % tuple(Pcluster))
print
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
import scipy.stats
from matplotlib import pyplot
from spm1d import rft1d
weather = rft1d.data.weather()
yA, yB = weather['Atlantic'], weather['Continental']
yA = gaussian_filter1d(yA, 8.0, axis=1, mode='wrap')
yB = gaussian_filter1d(yB, 8.0, axis=1, mode='wrap')
nA, nB = yA.shape[0], yB.shape[0]
mA, mB = yA.mean(axis=0), yB.mean(axis=0)
sA, sB = yA.std(ddof=1, axis=0), yB.std(ddof=1, axis=0)
s = np.sqrt(((nA - 1) * sA * sA + (nB - 1) * sB * sB) / (nA + nB - 2))
t = (mA - mB) / (s * np.sqrt(1.0 / nA + 1.0 / nB))
rA, rB = yA - mA, yB - mB
r = np.vstack([rA, rB])
FWHM = rft1d.geom.estimate_fwhm(r)
alpha = 0.05
df = nA + nB - 2
Q = yA.shape[1]
tstar = rft1d.t.isf(alpha, df, Q, FWHM)
calc = rft1d.geom.ClusterMetricCalculator()
k = calc.cluster_extents(t, tstar, interp=True)
kcirc = sum(k) / FWHM
ccirc = 1
rftcalc = rft1d.prob.RFTCalculator(STAT='T', df=(1, df), nodes=Q, FWHM=FWHM)
Psetcirc = rftcalc.p.set(ccirc, kcirc, tstar)
Pclustercirc = rftcalc.p.cluster(kcirc, tstar)
pyplot.figure(16)
ax = pyplot.axes([0.08, 0.15, 0.89, 0.83])
ax.plot(t, 'k', lw=3, label='t field')
ax.plot([0, Q], ([tstar] * 2), 'r--', label='Critical threshold')
ax.legend(loc='upper left')
ax.text(120, 4.0, 'p = %.6f' % Pclustercirc)
ax.plot([30, 110], [3, 4], 'k:')
ax.plot([190, 310], [4, 3.5], 'k:')
ax.plot([30, 310], [3, 3.5], 'ko')
ax.text(280, 2.1, ('$\\alpha$ = %.3f' % alpha), color='r')
ax.set_xlabel('Day', size=16)
ax.set_ylabel('t value', size=16)
pyplot.show(block=False)
print('Figure 16 (Page 20):')
print('   [see Figure 16]')
print('   Critical t value (1D RFT):  t = %.3f' % tstar)
print('   Critical t value (0D):  t = %.3f' % scipy.stats.t.isf(alpha, df))
print('   Probability (set-level, circular):  p = %.6f' % Psetcirc)
print('   Probability (cluster-level, circular):  p = %.6f' % Pclustercirc)
print
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from matplotlib import pyplot
from spm1d import rft1d
weather = rft1d.data.weather()
yA, yB = weather['Atlantic'], weather['Continental']
yA = gaussian_filter1d(yA, 8.0, axis=1, mode='wrap')
yB = gaussian_filter1d(yB, 8.0, axis=1, mode='wrap')
nA, nB = yA.shape[0], yB.shape[0]
N = nA + nB

def here_tstat2(yA, yB):
    nA, nB = yA.shape[0], yB.shape[0]
    mA, mB = yA.mean(axis=0), yB.mean(axis=0)
    sA, sB = yA.std(ddof=1, axis=0), yB.std(ddof=1, axis=0)
    s = np.sqrt(((nA - 1) * sA * sA + (nB - 1) * sB * sB) / (nA + nB - 2))
    t = (mA - mB) / (s * np.sqrt(1.0 / nA + 1.0 / nB))
    return t


t0 = here_tstat2(yA, yB)
np.random.seed(0)
nIter = 1000
T = []
y = np.vstack((yA, yB))
for iii in range(nIter):
    ind = np.random.permutation(N)
    i0, i1 = ind[:nA], ind[nA:]
    yyA, yyB = y[i0], y[i1]
    T.append(here_tstat2(yyA, yyB).max())

alpha = 0.05
tstar = np.percentile(T, 100 * (1 - alpha))
calc = rft1d.geom.ClusterMetricCalculator()
k0 = calc.cluster_extents(t0, tstar, interp=True)
nIter = 1000
K = []
for iii in range(nIter):
    ind = np.random.permutation(N)
    i0, i1 = ind[:nA], ind[nA:]
    yyA, yyB = y[i0], y[i1]
    t = here_tstat2(yyA, yyB)
    k = calc.cluster_extents(t, tstar, interp=True)
    K.append(max(k))

K = np.array(K)
Pcluster = [(K >= kk).mean() for kk in k0]
pyplot.figure(17)
ax = pyplot.axes([0.08, 0.15, 0.89, 0.83])
ax.plot(t0, 'k', lw=3, label='t field')
ax.plot([0, t.size], ([tstar] * 2), 'r--', label='Critical threshold')
ax.legend(loc='upper left')
ax.text(10, 2.8, ('p = %.3f' % Pcluster[0]), size=10)
ax.text(275, 3.5, ('p = %.3f' % Pcluster[1]), size=10)
ax.text(280, 1.8, ('$\\alpha$ = %.3f' % alpha), color='r')
ax.set_xlabel('Day', size=16)
ax.set_ylabel('t value', size=16)
pyplot.show(block=False)
print('Figure 17 (Page 21):')
print('   [see Figure 17]')
print('   Critical t value (non-parametric):  t = %.3f' % tstar)
print('   Probability (cluster-level):  p = %.3f, %.3f' % tuple(Pcluster))
print
print('\n\n\nSCRIPT FINISHED.')