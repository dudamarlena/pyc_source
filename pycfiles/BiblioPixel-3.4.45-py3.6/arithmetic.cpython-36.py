# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/colors/arithmetic.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 412 bytes


def color_blend(a, b):
    """
    Performs a Screen blend on RGB color tuples, a and b
    """
    return (
     255 - ((255 - a[0]) * (255 - b[0]) >> 8),
     255 - ((255 - a[1]) * (255 - b[1]) >> 8),
     255 - ((255 - a[2]) * (255 - b[2]) >> 8))


def color_scale(color, level):
    """
    Scale RGB tuple by level, 0 - 256
    """
    return tuple([int(i * level) >> 8 for i in list(color)])