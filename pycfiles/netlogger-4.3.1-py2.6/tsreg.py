# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/tsreg.py
# Compiled at: 2010-10-11 09:20:27
"""
For a time-series of values with a duration, where the values which
overlap in time are additive, calculate the average total value in
each fixed interval of time. Applications include the summing of
multiple concurrent data transfers over a single path.
"""
from math import ceil, floor

def reg(ts, delta, window):
    """Smooth an irregular univariate time-series 'ts' into regular one
    of size delta. This algorithm is linear in the size of 'ts',
    and uses constant (and small) temporary storage.
    The result vector uses memory O(time-range of ts / delta).

    For example:

    >>> a = ((105, 110, 115), (28, 10, 2), (1, 1, 2))
    >>> for interval in (10, 20, 40):
    ...     r = regularize(a, interval, (100, 140))
    ...     print ', '.join(["%.2f" % x for x in r])
    0.50, 2.40, 1.00, 0.30
    1.45, 0.65
    1.05
    >>> a = ((0,), (7,), (1.0,))
    >>> r = regularize(a, 5, (0,5))
    >>> print ', '.join(["%.2f" % x for x in r])
    1.00
    
    Args:
      - ts (3xN floats): Input matrix, with 3 columns: time(stamp), duration,
        value.
      - delta (float): Interval.
      - window (float,float): Times for start/end of interval. This is
        rounded up to an integer multiple of the interval.
      
    Return:
      N floats) Time, and value for each interval of size
                delta starting from window[0].
    """
    (tm, dur, val) = ts
    t0 = floor(window[0] / delta) * delta
    t1 = ceil(window[1] / delta) * delta
    n = int((t1 - t0) / delta)
    a = [
     0.0] * n
    span = t1 - t0
    for i in xrange(len(tm)):
        offs = tm[i] - t0
        v = float(val[i])
        x1 = int(floor(offs / delta))
        x2 = int(ceil(min(offs + dur[i], span) / delta)) - 1
        if x1 == x2:
            a[x1] += v * min(dur[i], delta) / delta
        else:
            a[x1] += v * ((x1 + 1) * delta - offs) / delta
            for j in xrange(x1 + 1, x2):
                a[j] += v

            a[x2] += v * (offs + dur[i] - x2 * delta) / delta

    return a


if __name__ == '__main__':
    import doctest, sys
    if len(sys.argv) > 1 and sys.argv[1] == '-d':
        doctest.testmod()
    else:
        a = (
         (105, 110, 115), (28, 10, 2), (1, 1, 2))
        for interval in (10, 20, 40):
            r = regularize(a, interval, (100, 140))
            print (', ').join([ '%.2f' % x for x in r ])