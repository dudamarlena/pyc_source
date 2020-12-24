# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/countmemaybe/kminvalues.py
# Compiled at: 2019-12-09 06:49:34
# Size of source mod 2**32: 4371 bytes
__doc__ = '\nThis is a small implemintation of the K-min values algorithm for distinct\nvalue estimation using the alorithm descibed in [1].  Benchmarks on 1.8 GHz\ncore i7 Macbook air yields 4.18 us per insertion and a relative error of\n~1.53% for 160000 16bit integers using k=256 and 32bit murmur hash.\n\nmicha gorelick, mynameisfiber@gmail.com\nhttp://micha.gd/\n\n[1]: http://www.mpi-inf.mpg.de/~rgemulla/publications/beyer07distinct.pdf\n'
import math
from itertools import chain, ifilterfalse, imap
from operator import attrgetter
import mmh3
from blist import sortedlist, sortedset
from .base_dve import BaseDVE
MAX_32BIT_INT = 2147483647

def unique_everseen(iterable, key=None):
    """List unique elements, preserving order. Remember all elements ever seen."""
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element

    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


class KMinValues(BaseDVE):

    def __init__(self, items=[], k=20, hasher=mmh3.hash, hasher_max=MAX_32BIT_INT):
        self.kmin = sortedlist()
        self.k = k
        self.hasher = hasher
        self.hasher_max = hasher_max
        self.update(items)

    def _idx(self, key):
        return self.hasher(str(key)) & self.hasher_max

    def add(self, key):
        idx = self._idx(key)
        if len(self.kmin) < self.k:
            if idx not in self.kmin:
                self.kmin.add(idx)
        elif idx < self.kmin[(-1)]:
            if idx not in self.kmin:
                self.kmin.pop()
                self.kmin.add(idx)

    def _smallest_k(self, *others):
        return min(self.k, *map(attrgetter('k'), others))

    def _direct_sum(self, *others):
        n = 0
        k = (self._smallest_k)(*others)
        X = sortedset(chain(self.kmin, *map(attrgetter('kmin'), others)))[:k]
        for item in self.kmin:
            if item in X and all((item in L.kmin for L in others)):
                n += 1

        return (
         n, X)

    def union(self, *others):
        newk = (self._smallest_k)(*others)
        self.kmin = sortedlist(unique_everseen(chain(self.kmin, *map(attrgetter('kmin'), others))))[:newk]

    def jaccard(self, other, k=0):
        n, X = self._direct_sum(other)
        return n / (1.0 * len(X))

    def cardinality_intersection(self, *others):
        n, X = (self._direct_sum)(*others)
        cardX = self._cardhelp(max(X), len(X))
        return n / (1.0 * len(X)) * cardX

    def cardinality_union(self, *others):
        _, X = (self._direct_sum)(*others)
        cardX = self._cardhelp(max(X), len(X))
        return cardX

    def _cardhelp(self, kmin, k):
        return (k - 1.0) * self.hasher_max / kmin

    def cardinality(self):
        if len(self.kmin) < self.k:
            return len(self.kmin)
        return self._cardhelp(self.kmin[(-1)], self.k)

    def __add__(self, other):
        assert other.k == self.k
        k = self._smallest_k(other)
        nt = KMinValues(k=k)
        nt.kmin = self.kmin
        nt.union(other)
        return nt

    def relative_error(self, confidence=0.98, D=0):
        p = 0
        if D:
            try:
                from scipy import special, optimize
            except ImportError:
                raise Exception('Scipy needed for relative error bounds')

            k = self.k
            u = lambda D, k, e: (k - 1.0) / ((1.0 - e) * D)
            l = lambda D, k, e: (k - 1.0) / ((1.0 + e) * D)
            objective = lambda e, D, k, confidence: special.betainc(k, D - k + 1, u(D, k, e)) - special.betainc(k, D - k + 1, l(D, k, e)) - confidence
            try:
                p = optimize.newton(objective, x0=0.05, args=(D, k, confidence))
            except RuntimeError:
                pass

        else:
            p = math.sqrt(2.0 / (math.pi * (self.k - 2)))
        return p