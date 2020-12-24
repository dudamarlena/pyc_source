# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/dlblocks/NumpyUtils.py
# Compiled at: 2018-12-11 12:52:10
import numpy as np

def cutWindows(data, windowSizes, windowOffsets):
    if type(data) is list:
        data = np.array(data)
        isList = True
        windowSizes = tuple([None] + list(windowSizes))
        windowOffsets = tuple([None] + list(windowOffsets))
    else:
        isList = False
    nDims = len(windowSizes)
    assert nDims == len(data.shape)
    assert len(data.shape) == len(windowOffsets)
    return