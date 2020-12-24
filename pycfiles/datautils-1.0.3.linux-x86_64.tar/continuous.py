# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/graham/.virtualenvs/temcagt/lib/python2.7/site-packages/datautils/grouping/continuous.py
# Compiled at: 2013-12-13 14:50:04
import logging
from base import Group

def pylinspace(start, end, n):
    d = (end - start) / (n - 1.0)
    return [ start + d * i for i in xrange(n) ]


try:
    import numpy
    minmax = lambda vs: (numpy.min(vs), numpy.max(vs))
    linspace = numpy.linspace
except ImportError as E:
    logging.warning('Failed to import numpy[%s] using slower minmax()' % E)
    minmax = lambda vs: (min(vs), max(vs))
    linspace = numpy.linspace

class ContinuousGroup(Group):

    def find_levels(self, values, key=None, **kwargs):
        self.levels = find_levels(values, key, **kwargs)


def right_level_test(start, end):

    def f(v):
        return v > start and v <= end

    return f


def left_level_test(start, end):

    def f(v):
        return v >= start and v < end

    return f


def both_level_test(start, end):

    def f(v):
        return v >= start and v <= end

    return f


def neither_level_test(start, end):

    def f(v):
        return v > start and v < end


def level_test(start, end, inclusive):
    if inclusive == 'left':
        return left_level_test(start, end)
    if inclusive == 'right':
        return right_level_test(start, end)
    if inclusive == 'both':
        return both_level_test(start, end)
    if inclusive == 'neither':
        return neither_level_test(start, end)
    raise ValueError("Invalid inclusive[%s] must be 'right'/'left'" % inclusive)


def name_function(ftype):
    if ftype == 'start':
        return lambda s, e: s
    if ftype == 'end':
        return lambda s, e: e
    if ftype == 'middle':
        return lambda s, e: (s + e) / 2.0
    if ftype == 'string':
        return lambda s, e: '(%g, %g)' % (s, e)


def find_levels(values, key=None, n=None, inclusive='histogram', names='start', overlap=0.0):
    vs = values if key is None else map(key, values)
    n = len(vs) ** 0.5 if n is None else n
    vmin, vmax = minmax(vs)
    dv = (vmax - vmin) / n
    overlap = dv * overlap / 2.0
    bounds = linspace(vmin, vmax, n + 1)
    to_name = name_function(names)
    if inclusive == 'histogram':
        lvls = {}
        for s, e in zip(bounds[:-2], bounds[1:-1]):
            s -= overlap
            e += overlap
            lvls[to_name(s, e)] = left_level_test(s, e)

        s, e = bounds[-2:]
        s -= overlap
        e += overlap
        lvls[to_name(s, e)] = both_level_test(s, e)
        return lvls
    else:
        return dict([ (to_name(s - overlap, e + overlap), level_test(s - overlap, e + overlap, inclusive)) for s, e in bounds
                    ])
        return