# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/utils/image.py
# Compiled at: 2020-02-10 09:12:42
# Size of source mod 2**32: 4773 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '25/02/2019'
import numpy, logging, enum
from numpy.linalg import inv
_logger = logging.getLogger(__file__)
try:
    import scipy.ndimage as shift_scipy
    has_scipy_shift = True
except ImportError:
    has_scipy_shift = False
    _logger.info('no scipy.ndimage.shift detected, will use numpy.fft instead')

def shift_img(data: numpy.ndarray, dx: float, dy: float, cval: float=0.0) -> numpy.ndarray:
    """
    Apply simple 2d image shift in 'constant mode'.

    :param data:
    :type data: numpy.ndarray
    :param dx: x translation to be applied
    :type dx: float
    :param dy: y translation to be applied
    :type dy: float
    :param float cval: value to replace the shifted values

    :return: shifted image
    :rtype: numpy.ndarray
    """
    assert data.ndim is 2
    assert dx is not None
    assert dy is not None
    _logger.debug('apply shift dx=%s, dy=%s ' % (dx, dy))
    if has_scipy_shift:
        return shift_scipy(input=data, shift=(dy, dx), order=3, mode='constant',
          cval=cval)
    ynum, xnum = data.shape
    print(data.shape)
    xmin = int(-numpy.fix(xnum / 2))
    xmax = int(numpy.ceil(xnum / 2) - 1)
    ymin = int(-numpy.fix(ynum / 2))
    ymax = int(numpy.ceil(ynum / 2) - 1)
    nx, ny = numpy.meshgrid(numpy.linspace(xmin, xmax, xnum), numpy.linspace(ymin, ymax, ynum))
    ny = numpy.asarray(ny, numpy.float32)
    nx = numpy.asarray(nx, numpy.float32)
    res = abs(numpy.fft.ifft2(numpy.fft.fft2(data) * numpy.exp(complex(0.0, 2.0) * numpy.pi * (-dy * ny / ynum + -dx * nx / xnum))))
    if dx > 0:
        res[:, 0:int(numpy.ceil(dx))] = cval
    else:
        if dx < 0:
            res[:, xnum + int(numpy.ceil(dx)):] = cval
        return res


class ImageScaleMethod(enum.Enum):
    RAW = 'raw'
    MEAN = 'mean'
    MEDIAN = 'median'


def scale_img2_to_img1(img_1, img_2, method=ImageScaleMethod.MEAN):
    """
    scale image2 relative to image 1 in such a way they have same min and
    max. Scale will be apply from and to 'data' / raw data

    :param img_1: reference image
    :type: numpy.array
    :param numpy.array img_2: image to scale
    :type: numpy.array
    :param method: method to apply scaling
    :type: ImageScaleMethod
    :return:
    """
    if not method in ImageScaleMethod:
        raise AssertionError
    elif not img_1.ndim == 2:
        raise AssertionError
    else:
        assert img_2.shape == img_1.shape
        min1 = img_2.min()
        max1 = img_2.max()
        min0 = img_1.min()
        max0 = img_1.max()
        if method is ImageScaleMethod.RAW:
            a = (min0 - max0) / (min1 - max1)
            b = (min1 * max0 - min0 * max1) / (min1 - max1)
            return a * img_2 + b
            if method is ImageScaleMethod.MEAN:
                me0 = img_1.mean()
                me1 = img_2.mean()
        elif method is ImageScaleMethod.MEDIAN:
            me0 = img_1.median()
            me1 = img_2.median()
        else:
            raise ValueError('method not managed', method)
    vec0 = numpy.mat([[min0], [me0], [max0]])
    matr = numpy.mat([[min1 * min1, min1, 1.0],
     [
      me1 * me1, me1, 1.0],
     [
      max1 * max1, max1, 1.0]])
    vec1 = inv(matr) * vec0
    return float(vec1[0]) * (img_2 * img_2) + float(vec1[1]) * img_2 + float(vec1[2])