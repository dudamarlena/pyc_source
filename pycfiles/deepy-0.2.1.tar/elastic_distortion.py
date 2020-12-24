# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/utils/elastic_distortion.py
# Compiled at: 2016-04-20 00:05:45
"""
This code is copied from https://github.com/vsvinayak/mnist-helper.
It requires Scipy to perform convolve2d.
Default parameters are modified.
"""
import numpy as np, math
from scipy.signal import convolve2d
from deepy.utils import global_rand

def create_2d_gaussian(dim, sigma):
    """
    This function creates a 2d gaussian kernel with the standard deviation
    denoted by sigma

    :param dim: integer denoting a side (1-d) of gaussian kernel
    :param sigma: floating point indicating the standard deviation

    :returns: a numpy 2d array
    """
    if dim % 2 == 0:
        raise ValueError('Kernel dimension should be odd')
    kernel = np.zeros((dim, dim), dtype=np.float16)
    center = dim / 2
    variance = sigma ** 2
    coeff = 1.0 / (2 * variance)
    for x in range(0, dim):
        for y in range(0, dim):
            x_val = abs(x - center)
            y_val = abs(y - center)
            numerator = x_val ** 2 + y_val ** 2
            denom = 2 * variance
            kernel[(x, y)] = coeff * np.exp(-1.0 * numerator / denom)

    return kernel / sum(sum(kernel))


def elastic_distortion(image, kernel_dim=21, sigma=6, alpha=30, negated=True):
    """
    This method performs elastic transformations on an image by convolving
    with a gaussian kernel.
    :param image: a numpy nd array
    :kernel_dim: dimension(1-D) of the gaussian kernel
    :param sigma: standard deviation of the kernel
    :param alpha: a multiplicative factor for image after convolution
    :param negated: a flag indicating whether the image is negated or not
    :returns: a nd array transformed image
    """
    if not negated:
        image = 255 - image
    if kernel_dim % 2 == 0:
        raise ValueError('Kernel dimension should be odd')
    result = np.zeros(image.shape)
    displacement_field_x = np.array([ [ global_rand.random_integers(-1, 1) for x in xrange(image.shape[0]) ] for y in xrange(image.shape[1])
                                    ]) * alpha
    displacement_field_y = np.array([ [ global_rand.random_integers(-1, 1) for x in xrange(image.shape[0]) ] for y in xrange(image.shape[1])
                                    ]) * alpha
    kernel = create_2d_gaussian(kernel_dim, sigma)
    displacement_field_x = convolve2d(displacement_field_x, kernel)
    displacement_field_y = convolve2d(displacement_field_y, kernel)
    for row in xrange(image.shape[1]):
        for col in xrange(image.shape[0]):
            low_ii = row + int(math.floor(displacement_field_x[(row, col)]))
            high_ii = row + int(math.ceil(displacement_field_x[(row, col)]))
            low_jj = col + int(math.floor(displacement_field_y[(row, col)]))
            high_jj = col + int(math.ceil(displacement_field_y[(row, col)]))
            if low_ii < 0 or low_jj < 0 or high_ii >= image.shape[1] - 1 or high_jj >= image.shape[0] - 1:
                continue
            res = image[(low_ii, low_jj)] / 4 + image[(low_ii, high_jj)] / 4 + image[(high_ii, low_jj)] / 4 + image[(high_ii, high_jj)] / 4
            result[(row, col)] = res

    return result