# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/numeric/providers.py
# Compiled at: 2006-08-11 18:29:42
"""Numerical replicator providers"""
from evogrid.interfaces import IProvider
from evogrid.numeric.interfaces import IMinMaxDomain
from evogrid.numeric.domains import HyperCubeDomain
from evogrid.numeric.replicators import VectorReplicator
from itertools import izip
from numpy import array
from numpy.random import uniform
from zope.interface import implements

class UniformReplicatorGenerator(object):
    """Randomly generate vector-based replicators replicator"""
    __module__ = __name__
    implements(IProvider)

    def __init__(self, min=None, max=None, dom=None):
        if min is None or max is None:
            if IMinMaxDomain.providedBy(dom):
                min, max = dom.min, dom.max
            else:
                raise ValueError('min and max must be specified')
        self._min = min
        self._max = max
        self._dom = dom or HyperCubeDomain(min, max)
        return

    def next(self):
        ranges = izip(self._min, self._max)
        cs = array([ uniform(min, max) for (min, max) in ranges ])
        return VectorReplicator(cs=cs, dom=self._dom)

    def __iter__(self):
        return self