# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/smoothness_estimation.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 880 bytes
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
np.random.seed(0)
nResponses = 1000
nNodes = 101
FWHM = np.linspace(1, 50, 21)
FWHMe = []
for w in FWHM:
    y = rft1d.random.randn1d(nResponses, nNodes, w, pad=False)
    FWHMe.append(rft1d.geom.estimate_fwhm(y))
    print('Actual FWHM: %06.3f, estimated FWHM: %06.3f' % (w, FWHMe[(-1)]))

pyplot.close('all')
pyplot.plot(FWHM, FWHM, 'k:', label='Actual')
pyplot.plot(FWHM, FWHMe, 'go', label='Estimated')
pyplot.legend(loc='upper left')
pyplot.xlabel('Actual FWHM', size=16)
pyplot.ylabel('Estimated FWHM', size=16)
pyplot.title('FWHM estimation validation', size=20)
pyplot.show()