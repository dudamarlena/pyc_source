# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.6-intel-2.7/spherogram/links/torus.py
# Compiled at: 2017-05-26 08:26:49
from .links import Crossing, Link

def torus_knot(name, method='calc'):
    """
    Returns a (p,q)-torus knot, as an instance of the Link class.
    """
    p, q = map(int, name[2:-1].split(','))
    if p == 0 or q == 0:
        raise Exception('Torus_knot(p,q) requires p, q, non-zero.')
    else:
        to_mirror = False
    if p < 0 or q < 0:
        p = abs(p)
        q = abs(q)
    if p < 0 and q < 0:
        p = abs(p)
        q = abs(q)
        to_mirror = True
    if p == 2:
        our_crossings = list()
        for i in range(q):
            our_crossings.append(Crossing(i))

        if q > 1:
            our_crossings[0][0] = our_crossings[(q - 1)][1]
            our_crossings[0][3] = our_crossings[(q - 1)][2]
            our_crossings[0][1] = our_crossings[1][0]
            our_crossings[0][2] = our_crossings[1][3]
            for i in range(1, q - 1):
                our_crossings[i][1] = our_crossings[(i + 1)][0]
                our_crossings[i][2] = our_crossings[(i + 1)][3]

            if to_mirror:
                return Link(our_crossings).mirror()
            return Link(our_crossings)
        if q == 1:
            our_crossings[0][0] = our_crossings[0][1]
            our_crossings[0][2] = our_crossings[0][3]
            if to_mirror:
                return Link(our_crossings).mirror()
            return Link(our_crossings)
    if p != 2:
        our_crossings = dict()
        for i in range(q):
            for j in range(p - 1):
                our_crossings[(i, j)] = Crossing((i, j))

        our_crossings[(0, 0)][3] = our_crossings[(q - 1, 0)][2]
        our_crossings[(0, p - 2)][0] = our_crossings[(q - 1, p - 2)][1]
        for i in range(p - 2):
            our_crossings[(0, i)][0] = our_crossings[(q - 1, i + 1)][2]

        if q > 1:
            for i in range(q - 1):
                our_crossings[(i, 0)][2] = our_crossings[(i + 1, 0)][3]
                our_crossings[(i, p - 2)][1] = our_crossings[(i + 1, p - 2)][0]

            for i in range(p - 2):
                for j in range(q):
                    our_crossings[(j, i)][1] = our_crossings[(j, i + 1)][3]

            for i in range(1, p - 1):
                for j in range(q - 1):
                    our_crossings[(j, i)][2] = our_crossings[(j + 1, i - 1)][0]

        crossings_list = list(our_crossings.values())
        if to_mirror:
            return Link(crossings_list).mirror()
        return Link(crossings_list)