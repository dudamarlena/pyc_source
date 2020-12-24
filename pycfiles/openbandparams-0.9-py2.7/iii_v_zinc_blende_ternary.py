# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/iii_v_zinc_blende_ternary.py
# Compiled at: 2015-04-09 02:47:55
__all__ = [
 'IIIVZincBlendeTernary']
from .iii_v_zinc_blende_mixed_alloy import IIIVZincBlendeMixedAlloy
from .algorithms import bisect

class IIIVZincBlendeTernary(IIIVZincBlendeMixedAlloy):
    """
    The base class for all III-V zinc blende ternary alloys.
    """

    def __init__(self, name, elements, binaries, parameters=None, x=None):
        if binaries[0].elements[1] == binaries[1].elements[1]:
            self._type = 1
            self._element_x = elements[0]
            self._element_1mx = elements[1]
            self._element_y = elements[2]
        elif binaries[0].elements[0] == binaries[1].elements[0]:
            self._type = 2
            self._element_y = elements[0]
            self._element_x = elements[1]
            self._element_1mx = elements[2]
        else:
            raise ValueError()
        super(IIIVZincBlendeTernary, self).__init__(name, elements, parameters=parameters)
        self.binaries = binaries
        if x is not None:
            self._x = float(x)
        else:
            self._x = None
        return

    def __eq__(self, other):
        return (
         type(self) == type(other) and self.name == other.name and self.elements == other.elements,
         self.binaries == other.binaries,
         self._parameters == other._parameters,
         self._x == other._x)

    def _instance(self, x=None):
        instance = IIIVZincBlendeTernary(self.name, self.elements, self.binaries, x=x)
        for parameter in self._parameters.values():
            instance.set_parameter(parameter)

        return instance

    def __call__(self, **kwargs):
        """
        Used to specify the alloy composition.
        """
        if 'x' in kwargs:
            x = float(kwargs['x'])
        elif self._element_x in kwargs:
            x = float(kwargs[self._element_x])
        elif self._element_1mx in kwargs:
            x = 1.0 - float(kwargs[self._element_1mx])
        elif 'a' in kwargs:
            a = kwargs['a']
            T = kwargs.get('T', 300.0)
            b1a = self.binaries[0].a(T=T)
            b2a = self.binaries[1].a(T=T)
            amin = min(b1a, b2a)
            amax = max(b1a, b2a)
            if a < amin or a > amax:
                raise ValueError('a out of range [%.3f, %.3f]' % (amin, amax))
            x = bisect(func=lambda x: self(x=x).a(T=T) - a, a=0, b=1)
        else:
            raise TypeError('Missing required key word argument.\n' + self._get_usage())
        if not 0.0 <= x <= 1.0:
            raise ValueError('The alloy fraction must be between 0 and 1')
        return self._instance(x=x)

    def _get_usage(self):
        return ("The supported kwarg combinations are as follows:\n    - 'x' or '{A}' or '{B}'\n    - 'a' [and 'T']").format(A=self._element_x, B=self._element_1mx)

    def __repr__(self):
        if self._x is None:
            return ('{}').format(self.name)
        else:
            if self._type == 1 or self._type == 2:
                return ('{}({}={})').format(self.name, self._element_x, self._x)
            raise RuntimeError()
            return

    def latex(self):
        if self._type == 1:
            if self._x is None:
                return ('{A}_{{x}}{B}_{{1-x}}{C}').format(A=self.elements[0], B=self.elements[1], C=self.elements[2])
            else:
                return ('{A}_{{{:g}}}{B}_{{{:g}}}{C}').format(self._x, 1.0 - self._x, A=self.elements[0], B=self.elements[1], C=self.elements[2])

        elif self._type == 2:
            if self._x is None:
                return ('{A}{B}_{{x}}{C}_{{1-x}}').format(A=self.elements[0], B=self.elements[1], C=self.elements[2])
            else:
                return ('{A}{B}_{{{:g}}}{C}_{{{:g}}}').format(self._x, 1.0 - self._x, A=self.elements[0], B=self.elements[1], C=self.elements[2])

        else:
            raise RuntimeError()
        return

    def element_fraction(self, element):
        if self._x is None:
            raise TypeError('Alloy composition has not been specified.')
        if self._type == 1:
            if element == self.elements[0]:
                return self._x
            else:
                if element == self.elements[1]:
                    return 1 - self._x
                if element == self.elements[2]:
                    return 1
                return 0

        elif self._type == 2:
            if element == self.elements[0]:
                return 1
            else:
                if element == self.elements[1]:
                    return self._x
                if element == self.elements[2]:
                    return 1 - self._x
                return 0

        else:
            raise RuntimeError()
        return

    def _get_bowing(self, name, kwargs):
        p = self.get_parameter(name + '_bowing', default=None)
        if p is None:
            return
        else:
            return p(x=self._x, **kwargs)

    def _interpolate(self, name, kwargs):
        if self._x is None:
            raise TypeError('Alloy composition has not been specified.')
        x = self._x
        pA = self.binaries[0].get_parameter(name)
        if pA is None:
            raise AttributeError(('"{}" is missing a required parameter: "{}".').format(self.binaries[0].name, name))
        pB = self.binaries[1].get_parameter(name)
        if pB is None:
            raise AttributeError(('"{}" is missing a required parameter: "{}".').format(self.binaries[1].name, name))
        A = pA(**kwargs)
        B = pB(**kwargs)
        C = self._get_bowing(name, kwargs)
        if C is not None:
            return A * x + B * (1 - x) - C * x * (1 - x)
        else:
            return A * x + B * (1 - x)
            return