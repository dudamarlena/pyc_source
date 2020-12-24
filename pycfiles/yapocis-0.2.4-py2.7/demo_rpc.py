# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/yapocis/demo_rpc.py
# Compiled at: 2011-08-30 23:33:15
"""
Created on Jul 21, 2011
@summary: Test yapocis kernels
@author: seant
"""
import numpy as np
from utils import imread, toimage
from utils import showArray, showArrayGrad

def test():
    from median import median3x3
    from gradient import gradient
    from hsi import rgb2hsi, hsi2rgb, joinChannels, splitChannels
    image = np.zeros((201, 199), dtype=np.float32)
    width, height = image.shape
    x, y = width / 2, height / 2
    offset = 10
    image[x - offset:x + offset, y - offset:y + offset] = 2
    image += np.random.random_sample(image.shape)
    filtered = median3x3(image, 100)
    showArray('Noisy', image)
    showArray('Filtered', filtered)
    image = np.float32(imread('test.jpg'))
    image /= 256.0
    showArray('Test HSI', image)
    r, g, b = splitChannels(image)
    h, s, i = rgb2hsi(r, g, b)
    showArray('I', i)
    showArray('S', s)
    showArray('H', h)
    g, a = gradient(i, 5)
    showArray('Gradient', g)
    showArray('Angle', a)
    sat = np.ones_like(i)
    gimg = joinChannels(*hsi2rgb(a, sat, g))
    showArray('Color gradient with angle', gimg)
    showArrayGrad('Grad angle', image, a)
    showArrayGrad('Grad vectors', image, a, g)


if __name__ == '__main__':
    test()