# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/rescale.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1918 bytes
from __future__ import print_function
import numpy as np
from skimage import exposure
from skimage import img_as_ubyte, img_as_uint

def rescale16bit(imgIn, verbose=False):
    if imgIn.min() < 0:
        imgIn += abs(imgIn.min())
    imgOut = exposure.rescale_intensity(imgIn, in_range='uint16', out_range='uint16')
    if imgOut.min() < 0:
        print('rescale16bit: WARNING imgOut has negative value')
    imgOut = imgOut.astype(np.uint16)
    out = img_as_uint(imgOut)
    if verbose:
        print('rescale16bit')
        print('type(image) ', type(out))
        print('type(image[0][0]) ', type(out[0][0]))
    return out


def rescale8bit(imgIn, verbose=False):
    if imgIn.min() < 0:
        imgIn += abs(imgIn.min())
    imgOut = exposure.rescale_intensity(imgIn, in_range='uint16', out_range='uint8')
    if imgOut.min() < 0:
        print('rescale8bit: WARNING imgOut has negative value')
    imgOut = imgOut.astype(np.uint8)
    out = img_as_ubyte(imgOut)
    if verbose:
        print('rescale8bit')
        print('type(image) ', type(out))
        print('type(image[0][0]) ', type(out[0][0]))
    return out