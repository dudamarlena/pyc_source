# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/image/transforms/normalize.py
# Compiled at: 2019-07-26 11:51:21
# Size of source mod 2**32: 413 bytes
import numpy as np
from .colorspace import bgr2rgb, rgb2bgr
from ..io import imread

def imnormalize(img, mean, std, to_rgb=True):
    img = imread(img).astype(np.float32)
    if to_rgb:
        img = bgr2rgb(img)
    return (img - mean) / std


def imdenormalize(img, mean, std, to_bgr=True):
    img = imread(img) * std + mean
    if to_bgr:
        img = rgb2bgr(img)
    return img