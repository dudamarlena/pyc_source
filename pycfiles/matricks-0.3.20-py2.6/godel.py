# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/matricks/scoring/godel.py
# Compiled at: 2011-05-12 22:58:36
from scorer import *
import math, primes

class GodelPositional(Scorer):
    """Godel Positional Scoring

Score is computed by identifying extrema values and marking their
position in a "shadow" vector the corresponds with a 2 for maxima, a 1
for minima, and 0 for all non-extreme values.
Each position in this vector is
then assigned a unique prime number raised to the power indicated in the
shadow vector for that position.  (Only positions with a 1 or a 2 will 
see any real contribution to the product.  The primes of the non-zero elements
of this vector are multiplied together to create a product that
represents the extrema pattern for each profile.   Profiles may then be sorted
using this product as a sort key, which will result in profiles with greater 
similarity to one another being grouped closer together in the sort.

Whether or not a value is an extrema is determined by comparing it to the
mean of the profile to see if it is within some multiple (the `c` argument)
of the standard deviation of the profile.   (Mean and std dev are computed for
each profile before scoring takes place.)

"""

    def __init__(self, mx, C=1, modal=False, prec=None, **kwargs):
        self.mx = mx
        self.C = C
        self.modal = modal == True
        self.prec = int(math.log(len(mx.labels[mx.skipcols:]))) if prec is None else prec
        self.prime_map = dict(zip(mx.labels[mx.skipcols:], primes.first1000))
        return

    @staticmethod
    def signum(n):
        if n < 0:
            return 1
        return 2

    def __call__(self, v, skip=1):
        vec = sorted([ (self.mx.labels[i], v[i], i) for i in range(len(v)) if isinstance(v[i], (float, int)) ], key=lambda x: x[1], reverse=True)
        top = list()
        if self.modal:
            mode = self.mx.mode(v, prec=self.prec)
            top = [ e for e in vec if e[1] > mode ]
        else:
            (mean, std_dev) = self.mx.std_stats([ vec[i][1] for i in range(len(vec)) ])
            top = [ e for e in vec if e[1] > mean + self.C * std_dev ]
        if len(vec) < 1:
            return None
        else:
            top_len = len(top)
            if top_len == 0:
                return None
            bottom = [ x for x in vec[-top_len:] ]
            result = reduce(lambda x, i: x * self.prime_map[top[i][0]] ** 2 * self.prime_map[bottom[i][0]], range(top_len), 1)
            return result