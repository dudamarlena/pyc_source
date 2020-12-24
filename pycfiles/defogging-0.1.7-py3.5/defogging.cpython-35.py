# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\defogging\defogging.py
# Compiled at: 2017-08-16 04:08:28
# Size of source mod 2**32: 602 bytes
import sys
from PIL import Image
from numpy import *
from .core.recover import recover
from .core.airlight import airlight
from .core.guidedfilter import guidedfilter
from .core.transmission import transmission

def defogging(src):
    L = array(Image.fromarray(uint8(src * 255)).convert('L')).astype(float) / 255
    hei, wid = src.shape[0:2]
    A = airlight(src, L, 0.2)
    trans = transmission(src, A, round(0.02 * min(hei, wid)), 0.95)
    trans_refined = guidedfilter(trans, L, 30, 1e-06)
    dst = recover(src, A, trans_refined)
    return dst