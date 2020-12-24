# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jesse/Source/ttkthemes/ttkthemes/_imgops.py
# Compiled at: 2020-02-09 16:41:04
# Size of source mod 2**32: 1119 bytes
"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""

def shift_hue(image, hue):
    """
    Shifts the hue of an image in HSV format.
    :param image: PIL Image to perform operation on
    :param hue: value between 0 and 2.0
    """
    hue = (hue - 1.0) * 180
    img = image.copy().convert('HSV')
    pixels = img.load()
    for i in range(img.width):
        for j in range(img.height):
            h, s, v = pixels[(i, j)]
            h = abs(int(h + hue))
            if h > 255:
                h -= 255
            pixels[(i, j)] = (
             h, s, v)

    return img.convert('RGBA')


def make_transparent(image):
    """Turn all black pixels in an image into transparent ones"""
    data = image.copy().getdata()
    modified = []
    for item in data:
        if _check_pixel(item) is True:
            modified.append((255, 255, 255, 255))
        else:
            modified.append(item)

    image.putdata(modified)
    return image


def _check_pixel(tup):
    """Check if a pixel is black, supports RGBA"""
    return tup[0] == 0 and tup[1] == 0 and tup[2] == 0