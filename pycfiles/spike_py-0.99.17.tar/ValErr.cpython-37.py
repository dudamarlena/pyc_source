# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/util/ValErr.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 2130 bytes
"""
untitled.py

Created by Marc-André on 2011-03-20.
Copyright (c) 2011 IGBMC. All rights reserved.
"""
from __future__ import print_function

def round(x):
    """takes the nearest integer of a float
    >>> round(0.6)
    1.0
    >>> round(0.4)
    0.0
    >>> round(-0.6)
    -1.0
    >>> round(-0.4)
    0.0
    """
    import math
    return math.floor(x + 0.5)


def ValErr(v, e=0.0):
    """
    nice print of a value with error bars

    values are rounded to significative digits
    >>> print ValErr(1234.567,123.4)
    1230 +/- 123

    can be called with a pair of values or a tuple :
    >>> V=(1234.567,123.4); print ValErr(V)
    1230 +/- 123

    values are rounded to significative digits
    >>> print ValErr(7654.321,1234)
    7700 +/- 1230
    >>> print ValErr(7654.321,123.4)
    7650 +/- 123
    >>> print ValErr(7654.321,12.34)
    7654 +/- 12

    format depends on error
    >>> print ValErr(1234.567,12.34)
    1235 +/- 12
    >>> print ValErr(1234.567,1.234)
    1234.6 +/- 1.2
    >>> print ValErr(1234.567,0.1234)
    1234.57 +/- 0.12
    >>> print ValErr(1234.567,0.01234)
    1234.567 +/- 0.012
    """
    import math
    deb = 0
    if deb:
        print((v, e))
    else:
        if isinstance(v, tuple):
            val, err = v
        else:
            val = v
            err = e
        try:
            dig = math.log10(err)
        except:
            dig = 3

        tweek = 1
        idig = round(dig - tweek + 0.5)
        if deb:
            print(dig, idig)
        err = float(round(err * 10 ** (2 - idig))) / 10 ** (2 - idig)
        if deb:
            print(err)
        if idig > 1:
            format = '%.0f +/- %.0f'
        else:
            if idig <= 1:
                format = '%%.%df +/- %%.%df' % (-idig + 1, -idig + 1)
    if deb:
        print(format)
    if idig > 0:
        val = float(round(val * 10 ** (1 - idig))) / 10 ** (1 - idig)
    return format % (val, err)