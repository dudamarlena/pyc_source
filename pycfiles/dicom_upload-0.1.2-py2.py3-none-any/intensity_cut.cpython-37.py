# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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