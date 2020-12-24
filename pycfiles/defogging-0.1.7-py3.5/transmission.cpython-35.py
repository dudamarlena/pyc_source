# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\defogging\core\transmission.py
# Compiled at: 2017-08-05 21:15:26
# Size of source mod 2**32: 588 bytes
from numpy import *
from .minfilter import minfilter

def transmission(src, A, r, w):
    """

    :param src: original input image(three channels)
    :param A: airlight(1,1,3)
    :param r: radius of darkchannel
    :param w: t = 1 - w*(I/A)
    :return: dst
    """
    hei, wid = src.shape[0:2]
    tmp = zeros((hei, wid))
    for i in range(hei):
        for j in range(wid):
            tmp[(i, j)] = min(src[i, j, :] / A[0, 0, :])

    min_tmp = minfilter(tmp, r)
    dst = ones((hei, wid)) - min_tmp[:, :]
    dst = vectorize(lambda x: x if x > 0.1 else 0.1)(dst)
    return dst