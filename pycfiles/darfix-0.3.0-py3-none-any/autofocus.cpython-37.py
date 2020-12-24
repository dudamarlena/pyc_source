# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/garrigaf/Documents/git/darfix/build/lib/darfix/core/autofocus.py
# Compiled at: 2019-11-28 10:44:40
# Size of source mod 2**32: 1584 bytes
__authors__ = [
 'J. Garriga']
__license__ = 'MIT'
__date__ = '02/09/2019'
import numpy

def normalized_variance(img):
    """
    Computes the normalized variance autofocus function into the given image.
    """
    img = numpy.asanyarray(img)
    return img.var() / img.mean()