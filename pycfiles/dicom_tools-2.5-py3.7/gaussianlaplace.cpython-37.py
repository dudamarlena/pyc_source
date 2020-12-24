# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/gaussianlaplace.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 686 bytes
import numpy as np
from scipy.ndimage.filters import gaussian_laplace

def GaussianLaplaceFilter(data, sigma, verbose=False):
    result = np.zeros(data.shape)
    for layer in xrange(0, len(data)):
        image = data[layer]
        prova = gaussian_laplace(image, sigma, (result[layer]), mode='constant', cval=0.0)
        result[layer] = (result[layer] + abs(result[layer].min())) * 100

    return result