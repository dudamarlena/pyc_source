# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/fractal.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1648 bytes
from matplotlib import pylab as plt
import numpy as np
from scipy import stats

class fractal:

    def __init__(self, verbose=False):
        self.verbose = verbose

    def frattali(self, roi):
        assex = []
        assey = []
        bx = roi[:, 1].size
        by = roi[1, :].size
        for size in range(2, 15):
            px = int(bx / size)
            py = int(by / size)
            count1 = 0
            nx = 0
            ny = 0
            for ny in range(0, py):
                for nx in range(0, px):
                    if np.count_nonzero(roi[nx * size:(nx + 1) * size, ny * size:(ny + 1) * size]) > 0:
                        count1 = count1 + 1

            assex.append(np.log(1.0 / size))
            assey.append(np.log(count1))

        nassex = np.array(assex)
        nassey = np.array(assey)
        slope, intercept, r_value, p_value, std_err = stats.linregress(nassex, nassey)
        return slope