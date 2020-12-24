# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quadratum/transforms.py
# Compiled at: 2018-07-29 13:29:31
# Size of source mod 2**32: 1141 bytes
from . import functional as F
__all__ = [
 'Whiten', 'Invert', 'Dominofy', 'Contain']

class Whiten(object):
    __doc__ = 'Make all transparent pixels white (if there is an alpha channel).'

    def __init__(self):
        pass

    def __call__(self, image):
        return F.whiten(image)


class Invert(object):
    __doc__ = 'Invert RGB values.'

    def __init__(self):
        pass

    def __call__(self, image):
        return F.invert(image)


class Dominofy(object):
    __doc__ = 'Limits the ratio of an image.'

    def __init__(self, threshold=2):
        self.threshold = threshold

    def __call__(self, image):
        return F.dominofy(image, self.threshold)


class Contain(object):
    __doc__ = 'Contains an image into given canvas, like good-old `background-size: contain;` from CSS.'

    def __init__(self, size, fill='white'):
        self.size = size
        if fill in ('white', 'black'):
            self.fill = fill
        else:
            raise ValueError('Invalid fill option.')

    def __call__(self, image):
        return F.contain(image, (self.size), fill=(self.fill))