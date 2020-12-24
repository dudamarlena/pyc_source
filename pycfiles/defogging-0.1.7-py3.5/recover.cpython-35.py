# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\defogging\core\recover.py
# Compiled at: 2017-08-05 21:11:49
# Size of source mod 2**32: 681 bytes
from numpy import *

def recover(src, A, trans):
    """
    J = (I(x) - A) / t(x) +A

    --------
    :param src: original input(three channels)
    :param A: airlight(1,1,3)
    :param trans: transmission(one channel only)
    :return: dst
    """
    hei, wid = src.shape[0:2]
    dst = zeros((hei, wid, 3))
    dst[:, :, 0] = divide(src[:, :, 0] - A[(0, 0, 0)], trans[:, :]) + A[(0, 0, 0)]
    dst[:, :, 1] = divide(src[:, :, 1] - A[(0, 0, 1)], trans[:, :]) + A[(0, 0, 1)]
    dst[:, :, 2] = divide(src[:, :, 2] - A[(0, 0, 2)], trans[:, :]) + A[(0, 0, 2)]
    dst = vectorize(lambda x: x if x < 1 else 1)(dst)
    dst = vectorize(lambda x: x if x > 0 else 0)(dst)
    return dst