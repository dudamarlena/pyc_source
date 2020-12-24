# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/visualization/polyfit.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 519 bytes
import numpy as np

def draw_order3(networks, p1, p2):
    midpoint = (
     p2[0] + 1, p1[1] + 1)
    x = [p1[0], midpoint[0], p1[1]]
    y = [p2[0], midpoint[1], p2[1]]
    z = np.polyfit(x, y, 3)
    f = np.poly1d(z)
    space_x = np.linspace(0, networks, 10)
    space_y = f(space_x)
    return (
     space_x, space_y)


def draw_piramidal(networks, p1, p2):
    midpoint = (
     p2[0] + 1, p1[1] + 1)
    x = [p1[0], midpoint[0], p1[1]]
    y = [p2[0], midpoint[1], p2[1]]
    return (
     x, y)