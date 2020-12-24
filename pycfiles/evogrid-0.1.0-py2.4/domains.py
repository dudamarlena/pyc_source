# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/numeric/domains.py
# Compiled at: 2006-08-14 11:05:03
"""Numerical domains"""
from evogrid.numeric.interfaces import IMinMaxDomain
from numpy import array, maximum, minimum, all
from zope.interface import implements
from zope.component import adapts

class HyperCubeDomain(object):
    """Numerical domain bound by min and max values"""
    __module__ = __name__
    implements(IMinMaxDomain)
    min, max = None, None

    def __init__(self, min, max):
        self.min = array(min)
        self.max = array(max)

    def __contains__(self, cs):
        return all(self.ensure_belong(cs) == cs)

    def ensure_belong(self, cs):
        cs = maximum(self.min, cs)
        return minimum(self.max, cs)

    def __repr__(self):
        class_name = self.__class__.__name__
        return '%s(%r, %r)' % (class_name, list(self.min), list(self.max))


class ResolutionDowngraderDomain(object):
    """Adapter to restict domain values to rounded values

    This can be usefull to optimize the efficiency of an evaluation caching
    strategy.
    """
    __module__ = __name__
    implements(IMinMaxDomain)
    adapts(IMinMaxDomain)

    def get_max(self):
        return self._domain.max

    max = property(get_max)

    def get_min(self):
        return self._domain.min

    min = property(get_min)
    _resolution = 1

    def __init__(self, domain, resolution=1):
        self._resolution = resolution
        self._domain = domain
        self._scale = domain.max - domain.min

    def __contains__(self, cs):
        return self.ensure_belong(cs) == cs

    def ensure_belong(self, cs):
        scale = self._scale
        scaled = cs / scale
        cs = scaled.round(self._resolution) * scale
        return self._domain.ensure_belong(cs)

    def __repr__(self):
        class_name = self.__class__.__name__
        return '%s(%r, resolution=%r)' % (class_name, self._domain, self._resolution)