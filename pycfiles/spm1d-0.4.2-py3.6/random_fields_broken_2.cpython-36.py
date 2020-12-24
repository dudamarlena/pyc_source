# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/rft1d/examples/random_fields_broken_2.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 1075 bytes
"""
Broken (piecewise continuous) random field generation using
rft1d.random.Generator1D

Note:
When FWHM gets large (2FWHM>nNodes), the data should be padded
using the *pad* keyword.
"""
import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
np.random.seed(12345)
nResponses = 5
nNodes = 101
FWHM = 20.0
nodes = np.array([True] * nNodes)
nodes[20:30] = False
nodes[60:80] = False
generator = rft1d.random.Generator1D(nResponses, nodes, FWHM)
y = generator.generate_sample()
y = generator.generate_sample()
y = generator.generate_sample()
y = generator.generate_sample()
pyplot.close('all')
pyplot.plot(y.T)
pyplot.plot([0, 100], [0, 0], 'k:')
pyplot.xlabel('Field position', size=16)
pyplot.ylabel('z', size=20)
pyplot.title('Broken (piecewise continuous) random fields', size=20)
pyplot.show()