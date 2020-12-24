# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/proteinko/utils.py
# Compiled at: 2020-04-25 15:29:24
# Size of source mod 2**32: 364 bytes
import numpy as np

def pdf(x, sigma):
    """
    Calculates normal probability density function at x data points. Assumes
    mean of 0 and std provided by sigma parameter.
    :param x: data points
    :param sigma: std
    :return: np.array
    """
    y = np.exp(-x ** 2 / (2 * sigma)) / (sigma * np.sqrt(2 * np.pi))
    y = (y - y.min()) / (y.max() - y.min())
    return y