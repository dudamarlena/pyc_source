# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/vision/track/interpolation.py
# Compiled at: 2011-01-27 19:32:26
from ..annotations import *

def Linear(source, target):
    """
    Performs basic linear interpolation in between a source and a target.
    """
    if target.frame <= source.frame:
        raise ValueError(('Target frame must be greater than source frame (source = {0}, target = {1})').format(source.frame, target.frame))
    fdiff = float(target.frame - source.frame)
    xtlr = (target.xtl - source.xtl) / fdiff
    ytlr = (target.ytl - source.ytl) / fdiff
    xbrr = (target.xbr - source.xbr) / fdiff
    ybrr = (target.ybr - source.ybr) / fdiff
    results = []
    for i in range(source.frame, target.frame + 1):
        off = i - source.frame
        xtl = source.xtl + xtlr * off
        ytl = source.ytl + ytlr * off
        xbr = source.xbr + xbrr * off
        ybr = source.ybr + ybrr * off
        results.append(Box(xtl, ytl, xbr, ybr, i, source.lost, source.occluded))

    return results


def LinearFill(path, method=Linear):
    """
    Takes a sparse path and performs linear interpolation between the points.
    """
    result = []
    for (x, y) in zip(path, path[1:]):
        result.extend(method(x, y)[:-1])

    result.append(path[(-1)])
    return result