# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\bzETL\util\stats.py
# Compiled at: 2013-12-18 14:05:11
from math import sqrt
from .cnv import CNV
from .struct import nvl, Struct, Null
from .logs import Log
DEBUG = True
EPSILON = 1e-06

def stats2z_moment(stats):
    mc0, mc1, mc2, skew, kurt = (
     stats.count, stats.mean, stats.variance, stats.skew, stats.kurtosis)
    mz0 = mc0
    mz1 = mc1 * mc0
    mz2 = (mc2 + mc1 * mc1) * mc0
    mc3 = skew * mc2 ** 1.5
    mz3 = (mc3 + 3 * mc1 * mc2 - mc1 ** 3) * mc0
    mc4 = (kurt + 3.0) * mc2 ** 2.0
    mz4 = (mc4 + 4 * mc1 * mc3 + 6 * mc1 * mc1 * mc2 + mc1 ** 4) * mc0
    m = Z_moment(stats.count, mz1, mz2, mz3, mz4)
    if DEBUG:
        v = z_moment2stats(m, unbiased=False)
        if not closeEnough(v.count, stats.count):
            Log.error('convertion error')
        if not closeEnough(v.mean, stats.mean):
            Log.error('convertion error')
        if not closeEnough(v.variance, stats.variance):
            Log.error('convertion error')
    return m


def closeEnough(a, b):
    if abs(a - b) <= EPSILON * (abs(a) + abs(b) + 1):
        return True
    return False


def z_moment2stats(z_moment, unbiased=True):
    free = 0
    if unbiased:
        free = 1
    N = z_moment.S[0]
    if N == 0:
        return Stats()
    return Stats(count=N, mean=z_moment.S[1] / N if N > 0 else float('nan'), variance=(z_moment.S[2] - z_moment.S[1] ** 2 / N) / (N - free) if N - free > 0 else float('nan'), unbiased=unbiased)


class Stats(Struct):

    def __init__(self, **args):
        Struct.__init__(self)
        if 'count' not in args:
            self.count = 0
            self.mean = 0
            self.variance = 0
            self.skew = 0
            self.kurtosis = 0
        elif 'mean' not in args:
            self.count = args['count']
            self.mean = 0
            self.variance = 0
            self.skew = 0
            self.kurtosis = 0
        elif 'variance' not in args and 'std' not in args:
            self.count = args['count']
            self.mean = args['mean']
            self.variance = 0
            self.skew = 0
            self.kurtosis = 0
        elif 'skew' not in args:
            self.count = args['count']
            self.mean = args['mean']
            self.variance = args['variance'] if 'variance' in args else args['std'] ** 2
            self.skew = 0
            self.kurtosis = 0
        elif 'kurtosis' not in args:
            self.count = args['count']
            self.mean = args['mean']
            self.variance = args['variance'] if 'variance' in args else args['std'] ** 2
            self.skew = args['skew']
            self.kurtosis = 0
        else:
            self.count = args['count']
            self.mean = args['mean']
            self.variance = args['variance'] if 'variance' in args else args['std'] ** 2
            self.skew = args['skew']
            self.kurtosis = args['kurtosis']
        self.unbiased = args['unbiased'] if 'unbiased' in args else not args['biased'] if 'biased' in args else False

    @property
    def std(self):
        return sqrt(self.variance)


class Z_moment(object):
    """
    ZERO-CENTERED MOMENTS
    """

    def __init__(self, *args):
        self.S = tuple(args)

    def __add__(self, other):
        return Z_moment(*map(add, self.S, other.S))

    def __sub__(self, other):
        return Z_moment(*map(sub, self.S, other.S))

    @property
    def tuple(self):
        return self.S

    @property
    def dict(self):
        return {'s' + unicode(i):m for i, m in enumerate(self.S)}

    @staticmethod
    def new_instance(values=None):
        if values == None:
            return Z_moment()
        else:
            values = [ float(v) for v in values if v != None ]
            return Z_moment(len(values), sum([ n for n in values ]), sum([ pow(n, 2) for n in values ]), sum([ pow(n, 3) for n in values ]), sum([ pow(n, 4) for n in values ]))


def add(a, b):
    return nvl(a, 0) + nvl(b, 0)


def sub(a, b):
    return nvl(a, 0) - nvl(b, 0)


def z_moment2dict(z):
    return {'s' + unicode(i):m for i, m in enumerate(z.S)}


setattr(CNV, 'z_moment2dict', staticmethod(z_moment2dict))

def median(values):
    try:
        if not values:
            return Null
        else:
            l = len(values)
            _sorted = sorted(values)
            if l % 2 == 0:
                return (_sorted[(l / 2 - 1)] + _sorted[(l / 2)]) / 2
            return _sorted[(l / 2)]

    except Exception as e:
        Log.error('problem with median', e)