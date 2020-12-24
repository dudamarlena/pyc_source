# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/matricks/scoring/positional.py
# Compiled at: 2012-04-03 01:57:37
from scorer import *
import math

class Positional(Scorer):
    """Positional Scoring

Score is computed by identifying extrema values and marking their
position in a "shadow" vector that uses the index for maxima and the negated
index for minima.  These vectors can then be passed to the `sorted` python 
built-in funciton and sorted lexicographically to group like profiles
together.

Whether or not a value is an extrema is determined by comparing it to the
mean of the profile to see if it is within some multiple (the `c` argument)
of the standard deviation of the profile.   (Mean and std dev are computed for
each profile before scoring takes place.)

"""

    def __init__(self, mx, C=1, modal=False, prec=None, thresh=None, **kwargs):
        self.mx = mx
        self.C = C
        self.modal = modal == True
        self.prec = int(math.log(len(mx.labels[mx.skipcols:]))) if prec is None else prec
        self.thresh = thresh
        self.position_map = dict(zip(mx.labels, range(len(mx.labels))))
        return

    @staticmethod
    def signum(n):
        if n < 0:
            return 1
        return 2

    def __call__(self, v, skip=1, prec=None):
        vec = sorted([ (self.mx.labels[i], v[i], i) for i in range(len(v)) if isinstance(v[i], (float, int)) ], key=lambda x: x[1], reverse=True)
        top = list()
        if self.modal:
            mode = self.mx.mode(v, prec=self.prec)
            top = [ e for e in vec if e[1] > mode ][:self.C]
        elif self.thresh is not None:
            th = self.thresh([ e[1] for e in vec ], prec=self.prec if prec is None else prec)
            top = filter(lambda e: e[1] > th, vec)
        else:
            (mean, std_dev) = self.mx.std_stats([ vec[i][1] for i in range(len(vec)) ])
            top = [ e for e in vec if e[1] > mean + self.C * std_dev ]
        if len(vec) < 1:
            return
        else:
            top_len = len(top)
            if top_len == 0:
                return tuple([len(v) + 1] * len(v))
            result = tuple([ x[2] for x in top ])
            return sorted(result)