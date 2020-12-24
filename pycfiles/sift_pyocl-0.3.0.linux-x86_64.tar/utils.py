# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kieffer/workspace/sift_pyocl/build/lib.linux-x86_64-2.7/sift_pyocl/utils.py
# Compiled at: 2014-10-24 01:43:39
from __future__ import division
__authors__ = [
 'Jérôme Kieffer']
__contact__ = 'jerome.kieffer@esrf.eu'
__license__ = 'MIT'
__copyright__ = 'European Synchrotron Radiation Facility, Grenoble, France'
__date__ = '2013-06-13'
__status__ = 'beta'
__license__ = '\nPermission is hereby granted, free of charge, to any person\nobtaining a copy of this software and associated documentation\nfiles (the "Software"), to deal in the Software without\nrestriction, including without limitation the rights to use,\ncopy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the\nSoftware is furnished to do so, subject to the following\nconditions:\n\nThe above copyright notice and this permission notice shall be\nincluded in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,\nEXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES\nOF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND\nNONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT\nHOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,\nWHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING\nFROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR\nOTHER DEALINGS IN THE SOFTWARE.\n\n'
from math import ceil
import numpy

def calc_size(shape, blocksize):
    """
    Calculate the optimal size for a kernel according to the workgroup size
    """
    if '__len__' in dir(blocksize):
        return tuple(int(i) + int(j) - 1 & ~(int(j) - 1) for i, j in zip(shape, blocksize))
    else:
        return tuple(int(i) + int(blocksize) - 1 & ~(int(blocksize) - 1) for i in shape)


def kernel_size(sigma, odd=False, cutoff=4):
    """
    Calculate the optimal kernel size for a convolution with sigma

    @param sigma: width of the gaussian
    @param odd: enforce the kernel to be odd (more precise ?)
    """
    size = int(ceil(2 * cutoff * sigma + 1))
    if odd and size % 2 == 0:
        size += 1
    return size


def sizeof(shape, dtype='uint8'):
    """
    Calculate the number of bytes needed to allocate for a given structure

    @param shape: size or tuple of sizes
    @param dtype: data type
    """
    itemsize = numpy.dtype(dtype).itemsize
    cnt = 1
    if '__len__' in dir(shape):
        for dim in shape:
            cnt *= dim

    else:
        cnt = int(shape)
    return cnt * itemsize


def _gcd(a, b):
    """Calculate the greatest common divisor of a and b"""
    while b:
        a, b = b, a % b

    return a


def matching_correction(matching):
    """
    Given the matching between two list of keypoints, 
    return the linear transformation to correct kp2 with respect to kp1
    """
    N = matching.shape[0]
    X = numpy.zeros((2 * N, 6))
    X[::2, 2:] = (1, 0, 0, 0)
    X[::2, 0] = matching.x[:, 0]
    X[::2, 1] = matching.y[:, 0]
    X[1::2, 0:3] = (0, 0, 0)
    X[1::2, 3] = matching.x[:, 0]
    X[1::2, 4] = matching.y[:, 0]
    X[1::2, 5] = 1
    y = numpy.zeros((2 * N, 1))
    y[::2, 0] = matching.x[:, 1]
    y[1::2, 0] = matching.y[:, 1]
    A = numpy.dot(X.transpose(), X)
    sol = numpy.dot(numpy.linalg.inv(A), numpy.dot(X.transpose(), y))
    return sol


def bin2RGB(img):
    """
    Perform a 2x2 binning of the image
    """
    dtype = img.dtype
    if dtype == numpy.uint8:
        out_dtype = numpy.int32
    else:
        out_dtype = dtype
    shape = img.shape
    if len(shape) == 3:
        new_shape = (
         shape[0] // 2, shape[1] // 2, shape[2])
        new_img = img
    else:
        new_shape = (
         shape[0] // 2, shape[1] // 2, 1)
        new_img = img.reshape((shape[0], shape[1], 1))
    out = numpy.zeros(new_shape, dtype=out_dtype)
    out += new_img[::2, ::2, :]
    out += new_img[1::2, ::2, :]
    out += new_img[1::2, 1::2, :]
    out += new_img[::2, 1::2, :]
    out /= 4
    if len(shape) != 3:
        out.shape = (
         new_shape[0], new_shape[1])
    if dtype == numpy.uint8:
        return out.astype(dtype)
    else:
        return out