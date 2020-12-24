# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/getLayerWithLargerROI.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 603 bytes
from __future__ import print_function
import numpy as np

def getLayerWithLargerROI(ROI, verbose=False):
    if verbose:
        print('getLayerWithLargerROI')
        print('len(ROI)', len(ROI))
    nPixelMax = 0
    layerMax = 0
    for layer in xrange(0, len(ROI)):
        thisNPixel = np.sum(np.ravel(ROI[layer]))
        if thisNPixel > nPixelMax:
            nPixelMax = thisNPixel
            layerMax = layer

    if verbose:
        print('getLayerWithLargerROI returning', layerMax, 'which has', nPixelMax, 'pixels')
    return layerMax