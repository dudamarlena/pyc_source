# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/highlight_color.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 937 bytes
import numpy as np

def highlight_color(data, colorrange, verbose=False):
    if verbose:
        print('highlight_color')
    kMax = data.shape[0]
    jMax = data.shape[1]
    iMax = data.shape[2]
    valMin = float(colorrange.split(':')[0])
    valMax = float(colorrange.split(':')[1])
    if valMin > valMax:
        print('warning valMin > valMax')
    referenceValue = 0
    if valMin < 300:
        referenceValue = data[:, :, :, 0].max()
    if verbose:
        print('required minimum:', valMin)
        print('required maximum:', valMax)
    counter = 0
    for k in xrange(0, kMax):
        for j in xrange(0, jMax):
            for i in xrange(0, iMax):
                if data[(k, j, i, 0)] > valMin and data[(k, j, i, 0)] < valMax:
                    data[(k, j, i, 2)] = referenceValue

    if verbose:
        print('highlight_color returning')
        print(counter, 'pixels modified')
    return data