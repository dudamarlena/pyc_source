# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/normality/paper/appendix_FigA4.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 1915 bytes
import numpy as np
from matplotlib import pyplot
import spm1d
np.random.seed(1)
y0 = spm1d.data.uv1d.normality.NormalityAppendixDataset('A7').Y
y1 = spm1d.data.uv1d.normality.NormalityAppendixDataset('A8').Y
y2 = spm1d.data.uv1d.normality.NormalityAppendixDataset('A9').Y
WW = [10, 25, 50]
K2 = [spm1d.stats.normality.dagostinoK2(yy) for yy in [y0, y1, y2]]
P = [spm1d.stats.normality.shapirowilk(yy)[1] for yy in [y0, y1, y2]]
logP = -np.log10(P)
pyplot.close('all')
figw = 8
figh = figw / 1.6
pyplot.figure(figsize=(figw, figh))
axw = axh = 0.27
axx, axy = np.linspace(0.07, 0.71, 3), np.linspace(0.72, 0.09, 3)
AX = np.array([[pyplot.axes([xx, yy, axw, axh]) for xx in axx] for yy in axy])
[ax.plot((yy.T), 'k', lw=0.2) for ax, yy in zip(AX[0], [y0, y1, y2])]
[ax.plot((k2.z), color='b', lw=3) for ax, k2 in zip(AX[1], K2)]
[ax.plot(p, 'g', lw=2) for ax, p in zip(AX[2], logP)]
[pyplot.setp((ax.get_xticklabels() + ax.get_yticklabels()), size=8) for ax in AX.flatten()]
pyplot.setp((AX[0]), ylim=(-4.9, 4.9))
pyplot.setp((AX[1]), ylim=(0, 15))
pyplot.setp((AX[2]), ylim=(0, 2.8))
pyplot.setp((AX[:2]), xticklabels=[])
pyplot.setp((AX[:, 1:]), yticklabels=[])
[ax.set_xlabel('Time  (%)', size=14) for ax in AX[2]]
ylabels = ('', '$K^2$', '$-\\log_{10}(p)$')
[ax.set_ylabel(label, size=14) for ax, label in zip(AX[:, 0], ylabels)]
[ax.text(0.25, 0.85, ('Dataset A%d' % (i + 7)), size=10, ha='center', bbox=dict(color='0.85'), transform=(ax.transAxes)) for i, ax in enumerate(AX[0])]
[ax.text(0.55, 0.85, ('FWHM = %d' % w), size=10, ha='left', transform=(ax.transAxes)) for i, (ax, w) in enumerate(zip(AX[0], WW))]
pyplot.show()