# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/twizzle/hashalgos_preset.py
# Compiled at: 2019-06-24 18:49:59
# Size of source mod 2**32: 1971 bytes
"""
This module defines common perceptual image hashing algorithms that can be used as an example
"""
import numpy, cv2

def __resize_image_downscale(aInputImage, lImageWidth, lImageHeight):
    """resizing an image to a given size"""
    return cv2.resize(aInputImage, (lImageWidth, lImageHeight), interpolation=(cv2.INTER_AREA))


def __convert_image_to_grayscale(aInputImage):
    """converting an image to grayscale"""
    return cv2.cvtColor(aInputImage, cv2.COLOR_BGR2GRAY)


def average_hash(image, hash_size=8):
    """
    Average Hash computation

    Implementation follows http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

    Step by step explanation: https://www.safaribooksonline.com/blog/2013/11/26/image-hashing-with-python/
    """
    if hash_size < 0:
        raise ValueError('Hash size must be positive')
    image = __convert_image_to_grayscale(image)
    pixels = __resize_image_downscale(image, hash_size, hash_size)
    avg = pixels.mean()
    diff = pixels > avg
    return diff.flatten()


def dhash(image, hash_size=8):
    """
    Difference Hash computation.

    following http://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html

    computes differences horizontally

    """
    if hash_size < 0:
        raise ValueError('Hash size must be positive')
    image = __convert_image_to_grayscale(image)
    pixels = __resize_image_downscale(image, hash_size + 1, hash_size)
    diff = pixels[:, 1:] > pixels[:, :-1]
    return diff.flatten()