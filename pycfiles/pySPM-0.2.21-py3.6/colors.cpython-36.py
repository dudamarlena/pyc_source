# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pySPM\utils\colors.py
# Compiled at: 2019-05-21 08:54:40
# Size of source mod 2**32: 241 bytes


def hot2val(rgb):
    if type(rgb) in [list, tuple]:
        r, g, b = rgb
    else:
        r = rgb[:, :, 0]
        g = rgb[:, :, 1]
        b = rgb[:, :, 2]
    A = 0.365079
    B = 0.7460321
    return A * (r - 0.0416) / 0.9584 + (B - A) * g + (1 - B) * b