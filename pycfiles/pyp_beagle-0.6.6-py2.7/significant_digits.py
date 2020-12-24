# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyp_beagle/significant_digits.py
# Compiled at: 2019-07-16 04:25:49


def float_nsf(q, n):
    """
    Truncate a float to n significant figures.  May produce overflow in 
    very last decimal place when q < 1.  This can be removed by an extra 
    formatted print. 
    Arguments:
      q : a float
      n : desired number of significant figures
    Returns:
    Float with only n s.f. and trailing zeros, but with a possible small overflow.
    """
    import numpy as np
    sgn = np.sign(q)
    q = abs(q)
    n = int(np.log10(q / 10.0))
    if q < 1.0:
        val = q / 10 ** (n - 1)
    else:
        val = q / 10 ** n
    return str(sgn * int(val) * 10.0 ** n)


def to_precision(x, p):
    """
    returns a string representation of x formatted with a precision of p

    Based on the webkit javascript implementation taken from here:
    https://code.google.com/p/webkit-mirror/source/browse/JavaScriptCore/kjs/number_object.cpp
    """
    import math
    x = float(x)
    if x == 0.0:
        return '0.' + '0' * (p - 1)
    out = []
    if x < 0:
        out.append('-')
        x = -x
    e = int(math.log10(x))
    tens = math.pow(10, e - p + 1)
    n = math.floor(x / tens)
    if n < math.pow(10, p - 1):
        e = e - 1
        tens = math.pow(10, e - p + 1)
        n = math.floor(x / tens)
    if abs((n + 1.0) * tens - x) <= abs(n * tens - x):
        n = n + 1
    if n >= math.pow(10, p):
        n = n / 10.0
        e = e + 1
    m = '%.*g' % (p, n)
    if 0 == 1 and (e < -2 or e >= p):
        out.append(m[0])
        if p > 1:
            out.append('.')
            out.extend(m[1:p])
        out.append('e')
        if e > 0:
            out.append('+')
        out.append(str(e))
    elif e == p - 1:
        out.append(m)
    elif e >= 0:
        out.append(m[:e + 1])
        if e + 1 < len(m):
            out.append('.')
            out.extend(m[e + 1:])
    else:
        out.append('0.')
        out.extend(['0'] * -(e + 1))
        out.append(m)
    return ('').join(out)