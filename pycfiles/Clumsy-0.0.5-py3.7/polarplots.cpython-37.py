# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/Clumsy/misc/polarplots.py
# Compiled at: 2018-11-24 16:22:23
# Size of source mod 2**32: 2556 bytes
import numpy as np
from math import pi

def degree_to_rad(angle_degree):
    return angle_degree * pi / 180.0


def rad_to_degree(angle_rad):
    return angle_rad * 180.0 / pi


def get_close_degrees(arr, index, degree_dist=20):
    """
    ------
    INPUTS
    arr: np.array, values of degrees between
    index: int, the value of the array to index at
    degree_dist: int, value of how many degrees there can be between
                 the points to count.

    """
    boolean = [
     np.isclose(arr[index], arr, 0.1, degree_dist)]
    return (arr[boolean], boolean)


def count_45s(arr):
    """
    Go through every 45 degrees of a circle, and count the number
    of events in the array that fall within 20 degrees of the arr
    -----
    INPUTS:
    arr: np.array, an array of your degrees to check over
    -----
    outputs:
    dd: dict, keys are the degrees (e.g. 45), the values are the #
    """
    d = {}
    points = np.arange(-360, 405, 45)
    for degree in points:
        d[degree] = arr[np.isclose(degree, arr, 0.1, 20)].shape[0]

    for k, v in enumerate(sorted(d.keys())):
        convert = 360 + v
        d[convert] = d[convert] + d[v]
        if v == -45:
            break

    dd = {v:d[v] for k, v in enumerate(d) if v >= 0}
    test = zip(degree_to_rad(np.array(dd.keys())), dd.values())
    return (dd, test)


def polar_chart(ts, electrode):
    """
    ts: timeseries
    electrode: int
    """
    a, b = count_45s(rad_to_degree(ts[electrode, 0, :, 5].data))
    try:
        import matplotlib.pyplot as plt
    except Exception as e:
        try:
            print(e)
            return
        finally:
            e = None
            del e

    t = [
     0.0, 3.9269908169872414, 2.356194490192345, 6.283185307179586, 0.7853981633974483,
     4.71238898038469, 3.141592653589793, 1.5707963267948966, 5.497787143782138]
    N = len(t)
    counts = [bb[1] for bb in b]
    radii = np.array(counts)
    ax = plt.subplot(111, projection='polar')
    bars = ax.bar(counts, t)
    plt.show()