# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/limb_darkening.py
# Compiled at: 2020-01-13 18:32:58
# Size of source mod 2**32: 3538 bytes
from numpy import asarray, zeros
import math as mt

class LDParameterization(object):
    __slots__ = ('coefs', )
    name = ''
    ncoef = 0

    def __init__(self, coefs=None):
        self.coefs = zeros(self.ncoef) if coefs is None else asarray(coefs)
        assert self.coefs.size == self.ncoef

    def __str__(self):
        return '{} : {}'.format(self.name, self.coefs)

    def __repr__(self):
        return '{} : {}'.format(self.name, self.coefs)

    def map_from(self, other):
        raise NotImplementedError

    @property
    def uniform(self):
        raise NotImplementedError

    @property
    def linear(self):
        raise NotImplementedError

    @property
    def quadratic(self):
        raise NotImplementedError

    @property
    def triangular(self):
        raise NotImplementedError


class UniformLD(LDParameterization):
    __doc__ = 'Uniform limb darkening parameterization\n    '
    __slots__ = ('coefs', )
    name = 'uniform'
    ncoef = 0

    @property
    def uniform(self):
        return self

    @property
    def linear(self):
        return LinearLD([0.0])

    @property
    def quadratic(self):
        return QuadraticLD([0.0, 0.0])

    @property
    def triangular(self):
        return TriangularQLD([0.0, 0.0])


class LinearLD(LDParameterization):
    __doc__ = 'Linear limb darkening parameterization\n    '
    __slots__ = 'coefs'
    name = 'linear'
    ncoef = 1

    def map_from(self, other):
        self.coefs[:] = other.linear.coefs

    @property
    def linear(self):
        return self

    @property
    def quadratic(self):
        return QuadraticLD([self.coefs[0], 0])

    @property
    def triangular(self):
        return self.quadratic.triangular


class QuadraticLD(LDParameterization):
    __doc__ = 'Quadratic limb darkening parameterization\n    '
    __slots__ = ('coefs', )
    name = 'quadratic'
    ncoef = 2

    def map_from(self, other):
        self.coefs[:] = other.quadratic.coefs

    @property
    def quadratic(self):
        return self

    @property
    def triangular(self):
        u, v = self.coefs
        return TriangularQLD([(u + v) ** 2, u / (2 * (u + v))])


class TriangularQLD(QuadraticLD):
    __doc__ = 'Triangular quadratic parametrization by Kipping (2013)\n    \n    Kipping, D. MNRAS, 435 (3) pp. 2152-2160, 2013\n    '
    __slots__ = ('coefs', )
    name = 'triangular quadratic'

    def map_from(self, other):
        self.coefs[:] = other.triangular.coefs

    @property
    def quadratic(self):
        a, b = mt.sqrt(self.coefs[0]), 2 * self.coefs[1]
        return QuadraticLD([a * b, a * (1 - b)])

    @property
    def triangular(self):
        return self