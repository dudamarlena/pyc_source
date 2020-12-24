# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/image/transforms/colorspace.py
# Compiled at: 2019-07-26 11:54:24
# Size of source mod 2**32: 1500 bytes
import cv2
from ..io import imread

def bgr2gray(img, keepdim=False):
    """Convert a BGR image to grayscale image.

    Args:
        img (ndarray): The input image.
        keepdim (bool): If False (by default), then return the grayscale image
            with 2 dims, otherwise 3 dims.

    Returns:
        ndarray: The converted grayscale image.
    """
    out_img = cv2.cvtColor(imread(img), cv2.COLOR_BGR2GRAY)
    if keepdim:
        out_img = out_img[(Ellipsis, None)]
    return out_img


def gray2bgr(img):
    """Convert a grayscale image to BGR image.

    Args:
        img (ndarray or str): The input image.

    Returns:
        ndarray: The converted BGR image.
    """
    img = imread(img)
    img = img[(Ellipsis, None)] if img.ndim == 2 else img
    out_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return out_img


def convert_color_factory(src, dst):
    code = getattr(cv2, 'COLOR_{}2{}'.format(src.upper(), dst.upper()))

    def convert_color(img):
        out_img = cv2.cvtColor(imread(img), code)
        return out_img

    convert_color.__doc__ = 'Convert a {0} image to {1} image.\n\n    Args:\n        img (ndarray or str): The input image.\n\n    Returns:\n        ndarray: The converted {1} image.\n    '.format(src.upper(), dst.upper())
    return convert_color


bgr2rgb = convert_color_factory('bgr', 'rgb')
rgb2bgr = convert_color_factory('rgb', 'bgr')
bgr2hsv = convert_color_factory('bgr', 'hsv')
hsv2bgr = convert_color_factory('hsv', 'bgr')