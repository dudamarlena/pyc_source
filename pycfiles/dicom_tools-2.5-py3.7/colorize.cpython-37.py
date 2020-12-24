# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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