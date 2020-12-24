# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\defogging\core\minfilter.py
# Compiled at: 2017-08-13 06:12:29
# Size of source mod 2**32: 411 bytes
from numpy import *
from defogging.utils.padding import padding

def minfilter(src, r):
    """

    :param src: input(one channel only)
    :param r: window radius
    :return: dst
    """
    hei, wid = src.shape[0:2]
    dst = zeros((hei, wid))
    src_pad = padding(src, r)
    for i in range(hei):
        for j in range(wid):
            dst[(i, j)] = amin(src_pad[i:i + 2 * r + 1, j:j + 2 * r + 1])

    return dst