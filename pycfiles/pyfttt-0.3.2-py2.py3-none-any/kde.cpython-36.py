# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/probabilistic/kde.py
# Compiled at: 2018-09-28 18:20:43
# Size of source mod 2**32: 1730 bytes
__doc__ = '\nKernel Density Estimation \n'
from pyFTS.common import Transformations
import numpy as np

class KernelSmoothing(object):
    """KernelSmoothing"""

    def __init__(self, h, kernel='epanechnikov'):
        self.h = h
        self.kernel = kernel
        self.transf = Transformations.Scale(min=0, max=1)

    def kernel_function(self, u):
        """
        Apply the kernel

        :param u:
        :return:
        """
        if self.kernel == 'epanechnikov':
            tmp = 0.75 * (1.0 - u ** 2)
            if tmp > 0:
                return tmp
            else:
                return 0
        else:
            if self.kernel == 'gaussian':
                return 1.0 / np.sqrt(2 * np.pi) * np.exp(-0.5 * u ** 2)
            else:
                if self.kernel == 'uniform':
                    return 0.5
                else:
                    if self.kernel == 'triangular':
                        tmp = 1.0 - np.abs(u)
                        if tmp > 0:
                            return tmp
                        else:
                            return 0
                    else:
                        if self.kernel == 'logistic':
                            return 1.0 / (np.exp(u) + 2 + np.exp(-u))
                        if self.kernel == 'cosine':
                            return np.pi / 4.0 * np.cos(np.pi / 2.0 * u)
                    if self.kernel == 'sigmoid':
                        return 2.0 / np.pi * (1.0 / (np.exp(u) + np.exp(-u)))
                if self.kernel == 'tophat':
                    if np.abs(u) < 0.5:
                        return 1
                    else:
                        return 0
            if self.kernel == 'exponential':
                return 0.5 * np.exp(-np.abs(u))

    def probability(self, x, data):
        """
        Probability of the point x on data

        :param x:
        :param data:
        :return:
        """
        l = len(data)
        ndata = self.transf.apply(data)
        nx = self.transf.apply(x)
        p = sum([self.kernel_function((nx - k) / self.h) for k in ndata]) / l * self.h
        return p