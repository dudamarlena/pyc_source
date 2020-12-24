# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/colorize.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 469 bytes
from matplotlib import pylab as plt
import numpy as np

def colorize(img, color_map='jet', mask=None, verbose=False):
    my_cm = plt.cm.get_cmap(color_map)
    normed_data = (img - np.min(img)) / (np.max(img) - np.min(img))
    rgb_img = my_cm(normed_data)
    if verbose:
        print('colorize output shape', rgb_img.shape)
    if mask is not None:
        for i in range(0, 3):
            rgb_img[:, :, i] -= rgb_img[:, :, i] * np.logical_not(mask)

    return rgb_img