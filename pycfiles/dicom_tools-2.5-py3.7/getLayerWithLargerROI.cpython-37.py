# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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