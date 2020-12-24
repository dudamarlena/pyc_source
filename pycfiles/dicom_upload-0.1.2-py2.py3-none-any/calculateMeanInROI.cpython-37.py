# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/calculateMeanInROI.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 647 bytes
import numpy as np

def calculateMeanInROI(data, roi, verbose=False):
    if verbose:
        normarea = roi * data
        meaninroi = normarea.sum() / np.count_nonzero(normarea)
        print('calculateMeanInROI: data.shape', data.shape)
        print('calculateMeanInROI: returning mean', meaninroi)
        print('calculateMeanInROI: normarea.mean()', normarea.mean())
        print('calculateMeanInROI: np.ma.average(data,weights=roi)', np.ma.average(data, weights=roi))
        mx = np.ma.masked_array(data, mask=(np.logical_not(roi)))
        print('calculateMeanInROI: mx.mean()', mx.mean())
    return np.ma.average(data, weights=roi)