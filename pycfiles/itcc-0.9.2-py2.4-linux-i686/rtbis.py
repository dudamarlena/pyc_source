# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/ccs2/rtbis.py
# Compiled at: 2008-04-20 13:19:45
import exceptions

class Error(exceptions.Exception):
    __module__ = __name__


def rtbis(func, x1, x2, xacc):
    """Reference: Numerical Recipes in C, Chapter 9.1, Page 354"""
    f = func(x1)
    fmid = func(x2)
    if not isinstance(f, float) or not isinstance(fmid, float):
        raise Error()
    if f * fmid >= 0:
        raise Error()
    if f < 0.0:
        dx = x2 - x1
        rtb = x1
    else:
        dx = x1 - x2
        rtb = x2
    while True:
        dx *= 0.5
        xmid = rtb + dx
        fmid = func(xmid)
        if not isinstance(fmid, float):
            raise Error()
        if fmid <= 0.0:
            rtb = xmid
        if abs(dx) < xacc or fmid == 0.0:
            return rtb

    raise Error()