# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/getEntropy.py
# Compiled at: 2018-09-14 09:20:48
# Size of source mod 2**32: 2686 bytes
from __future__ import print_function
import numpy as np
import skimage.filters.rank as skim_entropy
import skimage.morphology as skim_disk
import skimage.morphology as skim_square
from skimage import exposure
from skimage import img_as_uint, img_as_ubyte
try:
    import ROOT
    ROOTfound = True
except ImportError:
    ROOTfound = False
    print('WARNING getEntropy.py: ROOT not found')

import dicom_tools.histFromArray as histFromArray
from dicom_tools.rescale import rescale16bit, rescale8bit

def getEntropy(image, ROI=None, square_size=5, verbose=False):
    image = rescale8bit(image)
    if ROI is None:
        entropyImg = skim_entropy(image, skim_square(square_size))
    else:
        entropyImg = skim_entropy(image, (skim_square(square_size)), mask=ROI)
    return entropyImg


def getEntropyCircleMask(image, ROI=None, circle_radius=5, verbose=False):
    if verbose:
        message = 'getEntropyCircleMask '
        if ROI is not None:
            message += 'ROI length ' + str(len(ROI))
        message += 'circle radius ' + str(circle_radius)
        print(message)
        print('type(image) ', type(image))
        print('type(image[0][0]) ', type(image[0][0]))
    else:
        image = rescale8bit(image, verbose)
        if verbose:
            print('type(image[0][0]) ', type(image[0][0]))
        if ROI is None:
            entropyImg = skim_entropy(image, skim_disk(circle_radius))
        else:
            ROI = ROI.astype(np.bool)
        entropyImg = skim_entropy(image, (skim_disk(circle_radius)), mask=ROI)
    return entropyImg


def make_histo_entropy(data, ROI, suffix='', verbose=False):
    entropy3D = np.zeros(tuple([len(data)]) + data[0, :, :].shape)
    for layer in xrange(0, len(data)):
        entropy3D[layer] = getEntropy(data[layer], ROI[layer])

    if verbose:
        print('getEntropy creating histogram', 'hEntropy' + suffix)
    his = histFromArray(data, name=('hEntropy' + suffix), verbose=verbose)
    allhistos = []
    for i, layer in enumerate(entropy3D):
        if verbose:
            print('getEntropy creating histogram', 'hEntropy' + str(i) + suffix)
        thishisto = histFromArray(layer, name=('hEntropy' + str(i) + suffix))
        if thishisto is not None:
            allhistos.append(thishisto)

    return (his, allhistos)