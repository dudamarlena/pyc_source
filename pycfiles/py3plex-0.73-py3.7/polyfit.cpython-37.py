# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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