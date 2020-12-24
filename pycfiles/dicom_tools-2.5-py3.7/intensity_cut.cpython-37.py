# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/intensity_cut.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 322 bytes
from __future__ import print_function
import numpy as np

def intensity_cut(data, ROI, icut, verbose=False):
    nFette = len(data)
    for layer in xrange(0, nFette):
        if ROI[layer].any():
            imax = np.max(data[layer] * ROI[layer])
            data[layer][data[layer] < icut * imax] = 0

    return data