# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyspeedup/algorithms/_halfIterate.py
# Compiled at: 2017-02-25 12:54:13
"""
.. moduleauthor:: Chris Dusold <PySpeedup@chrisdusold.com>

"""
import random, numpy

def halfIteration(function, fDomain, fRange=None, threshold=0.01):
    """A function that takes a mapping and uses a local search to find
    a half iteration approximation and returns a function that will
    reproduce the results."""
    if fRange is not None:
        hDomain = (
         min(fDomain[0], fRange[0]), max(fDomain[(-1)], fRange[(-1)]))
        step = float(min(fDomain[1] - fDomain[0], fRange[1] - fRange[0], (hDomain[1] - hDomain[0]) / 10.0))
    else:
        step = float(min(fDomain[1] - fDomain[0], (fDomain[1] - fDomain[0]) / 10.0))
        d = [ fDomain[0] + step * x for x in range(int((fDomain[(-1)] - fDomain[0]) / step) + 1) ]
        f = [ function(x) for x in d ]
        hDomain = (min(fDomain[0], min(f)), max(fDomain[(-1)], max(f)))
    step
    d = [ hDomain[0] + step * x for x in range(int((hDomain[(-1)] - hDomain[0]) / step) + 1) ]
    h = [ x for x in d ]

    def hGet(x):
        return numpy.interp(x, d, h)

    def hSet(x, y):
        h0 = hGet(x)
        hp = y - h0
        i = (x - hDomain[0]) / step
        i0 = int(i)
        hp0 = hp
        h[i0] += hp0
        while abs(hp0) > step * threshold and i0 > 0:
            i0 -= 1
            hp0 *= 0.5
            h[i0] += hp0

        i0 = int(i)
        hp0 = hp
        if i % 1 and i < len(h) - 1:
            i0 += 1
            h[i0] += hp0
        while abs(hp0) > step * threshold and i0 < len(h) - 1:
            i0 += 1
            hp0 *= 0.5
            h[i0] += hp0

    recursiveAve = step
    i = 0
    while recursiveAve > step * threshold:
        x = random.uniform(fDomain[0], fDomain[(-1)])
        y = function(x)
        y0 = hGet(x)
        if y0 > hDomain[1]:
            y0 = hDomain[1]
            hSet(x, y0)
        if y0 < hDomain[0]:
            y0 = hDomain[0]
            hSet(x, y0)
        y1 = hGet(y0)
        yp = y - y1
        y2 = yp / 2 + y1
        hSet(y0, y2)
        recursiveAve += abs(yp)
        recursiveAve /= 2
        i += 1

    return hGet


h = halfIteration(lambda x: x ** 2, (0, 0.1, 10), (0, 100))