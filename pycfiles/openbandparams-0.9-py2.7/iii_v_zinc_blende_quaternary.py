# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/iii_v_zinc_blende_quaternary.py
# Compiled at: 2015-11-05 19:16:51
__all__ = [
 'IIIVZincBlendeQuaternary']
from .iii_v_zinc_blende_mixed_alloy import IIIVZincBlendeMixedAlloy
from .algorithms import bisect

class IIIVZincBlendeQuaternary(IIIVZincBlendeMixedAlloy):
    """
    The base class for all III-V zinc blende quaternary alloys.
    """

    def __init__(self, name, elements, ternaries, parameters=None, x=None, y=None, z=None):
        if len(ternaries) == 3 and ternaries[0].elements[0] == ternaries[1].elements[0] and ternaries[0].elements[0] == ternaries[2].elements[0] and ternaries[0].elements[1] == ternaries[1].elements[1] and ternaries[0].elements[2] == ternaries[2].elements[1] and ternaries[1].elements[2] == ternaries[2].elements[2]:
            self._type = 1
            self._element_w = ternaries[0].elements[0]
            self._element_x = ternaries[0].elements[1]
            self._element_y = ternaries[0].elements[2]
            self._element_z = ternaries[1].elements[2]
            self.binaries = (ternaries[0].binaries[0],
             ternaries[0].binaries[1],
             ternaries[1].binaries[1])
            calc_elements = (ternaries[0].elements[0],
             ternaries[0].elements[1],
             ternaries[0].elements[2],
             ternaries[1].elements[2])
        elif len(ternaries) == 3 and ternaries[0].elements[0] == ternaries[1].elements[0] and ternaries[0].elements[1] == ternaries[2].elements[0] and ternaries[1].elements[1] == ternaries[2].elements[1] and ternaries[0].elements[2] == ternaries[1].elements[2] and ternaries[0].elements[2] == ternaries[2].elements[2]:
            self._type = 2
            self._element_x = ternaries[0].elements[0]
            self._element_y = ternaries[2].elements[0]
            self._element_z = ternaries[2].elements[1]
            self._element_w = ternaries[2].elements[2]
            self.binaries = (ternaries[0].binaries[0],
             ternaries[0].binaries[1],
             ternaries[1].binaries[1])
            calc_elements = (ternaries[0].elements[0],
             ternaries[2].elements[0],
             ternaries[2].elements[1],
             ternaries[2].elements[2])
        elif len(ternaries) == 4 and ternaries[0].elements[0] == ternaries[1].elements[0] and ternaries[0].elements[0] == ternaries[2].elements[0] and ternaries[0].elements[1] == ternaries[1].elements[1] and ternaries[0].elements[1] == ternaries[3].elements[0] and ternaries[0].elements[2] == ternaries[2].elements[1] and ternaries[0].elements[2] == ternaries[3].elements[1] and ternaries[1].elements[2] == ternaries[2].elements[2] and ternaries[1].elements[2] == ternaries[3].elements[2]:
            self._type = 3
            self._element_x = ternaries[0].elements[0]
            self._element_1mx = ternaries[0].elements[1]
            self._element_y = ternaries[2].elements[1]
            self._element_1my = ternaries[2].elements[2]
            self.binaries = (ternaries[2].binaries[0],
             ternaries[2].binaries[1],
             ternaries[3].binaries[0],
             ternaries[3].binaries[1])
            calc_elements = (ternaries[0].elements[0],
             ternaries[0].elements[1],
             ternaries[2].elements[1],
             ternaries[2].elements[2])
        else:
            raise ValueError()
        assert elements == calc_elements
        super(IIIVZincBlendeQuaternary, self).__init__(name, elements, parameters=parameters)
        self.ternaries = ternaries
        if x is not None or y is not None or z is not None:
            self._xyz = self._parse_xyz(x, y, z)
        else:
            self._xyz = None
        return

    def __eq__(self, other):
        return (
         type(self) == type(other) and self.name == other.name and self.elements == other.elements,
         self.ternaries == other.ternaries,
         self._parameters == other._parameters,
         self._xyz == other._xyz)

    def _parse_xyz(self, x, y, z):
        if self._type == 1 or self._type == 2:
            if x is not None and y is not None and z is None:
                x = round(float(x), 6)
                y = round(float(y), 6)
                z = round(1.0 - x - y, 6)
            elif x is not None and y is None and z is not None:
                x = round(float(x), 6)
                z = round(float(z), 6)
                y = round(1.0 - x - z, 6)
            elif x is None and y is not None and z is not None:
                y = round(float(y), 6)
                z = round(float(z), 6)
                x = round(1.0 - y - z, 6)
            else:
                raise ValueError()
        elif self._type == 3:
            if x is not None and y is not None and z is None:
                x = round(float(x), 6)
                y = round(float(y), 6)
                z = None
            else:
                raise ValueError()
        else:
            raise RuntimeError()
        if not 0.0 <= x <= 1.0 or not 0.0 <= y <= 1.0 or z is not None and not 0.0 <= z <= 1.0:
            raise ValueError('The alloy fractions must be between 0 and 1')
        return (
         x, y, z)

    def _instance(self, x=None, y=None, z=None):
        instance = IIIVZincBlendeQuaternary(self.name, self.elements, self.ternaries, x=x, y=y, z=z)
        for parameter in self._parameters.values():
            instance.set_parameter(parameter)

        return instance

    def _has_x(self, kwargs):
        """Returns True if x is explicitly defined in kwargs"""
        return 'x' in kwargs or self._element_x in kwargs or self._type == 3 and self._element_1mx in kwargs

    def _get_x(self, kwargs):
        """
        Returns x if it is explicitly defined in kwargs.
        Otherwise, raises TypeError.
        """
        if 'x' in kwargs:
            return round(float(kwargs['x']), 6)
        if self._element_x in kwargs:
            return round(float(kwargs[self._element_x]), 6)
        if self._type == 3 and self._element_1mx in kwargs:
            return round(1.0 - float(kwargs[self._element_1mx]), 6)
        raise TypeError()

    def _has_y(self, kwargs):
        """Returns True if y is explicitly defined in kwargs"""
        return 'y' in kwargs or self._element_y in kwargs or self._type == 3 and self._element_1my in kwargs

    def _get_y(self, kwargs):
        """
        Returns y if it is explicitly defined in kwargs.
        Otherwise, raises TypeError.
        """
        if 'y' in kwargs:
            return round(float(kwargs['y']), 6)
        if self._element_y in kwargs:
            return round(float(kwargs[self._element_y]), 6)
        if self._type == 3 and self._element_1my in kwargs:
            return round(1.0 - float(kwargs[self._element_1my]), 6)
        raise TypeError()

    def _has_z(self, kwargs):
        """
        Returns True if type is 1 or 2 and z is explicitly defined in kwargs.
        """
        return (self._type == 1 or self._type == 2) and ('z' in kwargs or self._element_z in kwargs)

    def _get_z(self, kwargs):
        """
        Returns z if type is 1 or 2 and z is explicitly defined in kwargs.
        Otherwise, raises TypeError.
        """
        if self._type == 1 or self._type == 2:
            if 'z' in kwargs:
                return round(float(kwargs['z']), 6)
            if self._element_z in kwargs:
                return round(float(kwargs[self._element_z]), 6)
        raise TypeError()

    def __call__(self, **kwargs):
        """
        Used to specify the alloy composition.
        """
        if self._has_x(kwargs) and self._has_y(kwargs):
            x = self._get_x(kwargs)
            y = self._get_y(kwargs)
            z = None
        elif self._has_x(kwargs) and self._has_z(kwargs):
            x = self._get_x(kwargs)
            y = None
            z = self._get_z(kwargs)
        elif self._has_y(kwargs) and self._has_z(kwargs):
            x = None
            y = self._get_y(kwargs)
            z = self._get_z(kwargs)
        elif 'a' in kwargs and (self._has_x(kwargs) or self._has_y(kwargs) or self._has_z(kwargs)):
            a = kwargs['a']
            T = kwargs.get('T', 300.0)
            if self._has_x(kwargs):
                x = self._get_x(kwargs)
                if self._type in (1, 2):
                    ymax = round(1.0 - x, 6)
                elif self._type == 3:
                    ymax = 1.0
                else:
                    raise RuntimeError()
                z = None
                a0 = self(x=x, y=0.0).a(T=T)
                a1 = self(x=x, y=ymax).a(T=T)
                amin = min(a0, a1)
                amax = max(a0, a1)
                if not amin <= a <= amax:
                    raise ValueError(('a of {:g} out of range [{:g}, {:g}]').format(a, amin, amax))
                y = bisect(func=lambda y: self(x=x, y=y).a(T=T) - a, a=0, b=ymax)
            elif self._has_y(kwargs):
                y = self._get_y(kwargs)
                if self._type in (1, 2):
                    xmax = round(1.0 - y, 6)
                elif self._type == 3:
                    xmax = 1.0
                else:
                    raise RuntimeError()
                z = None
                a0 = self(x=0.0, y=y).a(T=T)
                a1 = self(x=xmax, y=y).a(T=T)
                amin = min(a0, a1)
                amax = max(a0, a1)
                if not amin <= a <= amax:
                    raise ValueError(('a of {:g} out of range [{:g}, {:g}]').format(a, amin, amax))
                x = bisect(func=lambda x: self(x=x, y=y).a(T=T) - a, a=0, b=xmax)
            elif self._has_z(kwargs):
                y = None
                z = self._get_z(kwargs)
                xmax = round(1.0 - z, 6)
                a0 = self(x=0.0, z=z).a(T=T)
                a1 = self(x=xmax, z=z).a(T=T)
                amin = min(a0, a1)
                amax = max(a0, a1)
                if not amin <= a <= amax:
                    raise ValueError(('a of {:g} out of range [{:g}, {:g}]').format(a, amin, amax))
                x = bisect(func=lambda x: self(x=x, z=z).a(T=T) - a, a=0, b=xmax)
        else:
            raise TypeError('Missing required key word argument.\n' + self._get_usage())
        return self._instance(x=x, y=y, z=z)

    def _get_usage(self):
        if self._type == 1 or self._type == 2:
            return ("The supported kwarg combinations are as follows:\n    - ('x' or '{x}') and ('y' or '{y}')\n    - ('x' or '{x}') and ('z' or '{z}')\n    - ('y' or '{y}') and ('z' or '{z}')\n    - 'a' [and 'T'] and ('x' or '{x}')\n    - 'a' [and 'T'] and ('y' or '{y}')\n    - 'a' [and 'T'] and ('z' or '{z}')").format(x=self._element_x, y=self._element_y, z=self._element_z)
        if self._type == 3:
            return ("The supported kwargs combinations are as follows:\n    - ('x', '{x}' or '{_1mx}') and ('y', '{y}' or '{_1my}')\n    - 'a' [and 'T'] and ('x', '{x}' or '{_1mx}')\n    - 'a' [and 'T'] and ('y', '{y}' or '{_1my}')").format(x=self._element_x, _1mx=self._element_1mx, y=self._element_y, _1my=self._element_1my)
        raise RuntimeError()

    def __repr__(self):
        if self._xyz is None:
            return ('{}').format(self.name)
        else:
            if self._type in (1, 2, 3):
                x, y, _ = self._xyz
                return ('{}({}={}, {}={})').format(self.name, self._element_x, x, self._element_y, y)
            raise RuntimeError()
            return

    def latex(self):
        e = {'A': self.elements[0], 'B': self.elements[1], 'C': self.elements[2], 
           'D': self.elements[3]}
        if self._type == 1:
            if self._xyz is None:
                return ('{A}{B}_{{x}}{C}_{{y}}{D}_{{1-x-y}}').format(**e)
            else:
                x, y, z = self._xyz
                return ('{A}{B}_{{{:g}}}{C}_{{{:g}}}{D}_{{{:g}}}').format(x, y, z, **e)

        elif self._type == 2:
            if self._xyz is None:
                return ('{A}_{{x}}{B}_{{y}}{C}_{{1-x-y}}{D}').format(**e)
            else:
                x, y, z = self._xyz
                return ('{A}_{{{:g}}}{B}_{{{:g}}}{C}_{{{:g}}}{D}').format(x, y, z, **e)

        elif self._type == 3:
            if self._xyz is None:
                return ('{A}_{{x}}{B}_{{1-x}}{C}_{{y}}{D}_{{1-y}}').format(**e)
            else:
                x, y, z = self._xyz
                _1mx = round(1.0 - x, 6)
                _1my = round(1.0 - y, 6)
                return ('{A}_{{{:g}}}{B}_{{{:g}}}{C}_{{{:g}}}{D}_{{{:g}}}').format(x, _1mx, y, _1my, **e)

        else:
            raise RuntimeError()
        return

    def element_fraction(self, element):
        if self._xyz is None:
            raise TypeError('Alloy composition has not been specified.')
        if self._type == 1 or self._type == 2:
            if element == self._element_w:
                return 1
            else:
                if element == self._element_x:
                    return self._x
                if element == self._element_y:
                    return self._y
                if element == self._element_z:
                    return self._z
                return 0

        elif self._type == 3:
            if element == self._element_x:
                return self._x
            else:
                if element == self._element_1mx:
                    return 1 - self._x
                if element == self._element_y:
                    return self._y
                if element == self._element_1my:
                    return 1 - self._y
                return 0

        else:
            raise RuntimeError()
        return

    def _get_bowing(self, name, kwargs):
        p = self.get_parameter(name + '_bowing', default=None)
        if p is None:
            return
        else:
            x, y, z = self._xyz
            return p(x=x, y=y, z=z, **kwargs)

    def _interpolate(self, name, kwargs):
        if self._xyz is None:
            raise TypeError('Alloy composition has not been specified.')
        if self._type == 1 or self._type == 2:
            return self._interpolate1or2(name, kwargs)
        else:
            if self._type == 3:
                return self._interpolate3(name, kwargs)
            raise RuntimeError()
            return

    def _interpolate1or2(self, name, kwargs):
        x, y, z = self._xyz
        u = (1.0 + x - y) / 2.0
        v = (1.0 + y - z) / 2.0
        w = (1.0 + x - z) / 2.0
        t12 = self.ternaries[0](x=u)
        t13 = self.ternaries[1](x=w)
        t23 = self.ternaries[2](x=v)
        p12 = t12.get_parameter(name)
        if p12 is None:
            raise AttributeError(('"{}" is missing a required parameter: "{}".').format(t12.name, name))
        p13 = t13.get_parameter(name)
        if p13 is None:
            raise AttributeError(('"{}" is missing a required parameter: "{}".').format(t13.name, name))
        p23 = t23.get_parameter(name)
        if p23 is None:
            raise AttributeError(('"{}" is missing a required parameter: "{}".').format(t23.name, name))
        v12 = p12(**kwargs)
        v13 = p13(**kwargs)
        v23 = p23(**kwargs)
        weight12 = x * y
        weight13 = x * z
        weight23 = y * z
        num = weight12 * v12 + weight13 * v13 + weight23 * v23
        denom = weight12 + weight13 + weight23
        if denom == 0.0:
            if x == 0.0:
                return v23
            else:
                return v13

        C = self._get_bowing(name, kwargs)
        if C is not None:
            return num / denom - C * x * (1 - x) * y * (1 - y) * z * (1 - z)
        else:
            return num / denom
            return

    def _interpolate3(self, name, kwargs):
        x, y, _ = self._xyz
        t43 = self.ternaries[0](x=x)
        t12 = self.ternaries[1](x=x)
        t23 = self.ternaries[2](x=y)
        t14 = self.ternaries[3](x=y)
        p12 = t12.get_parameter(name)
        if p12 is None:
            raise AttributeError(('"{}" is missing a required parameter: "{}".').format(t12.name, name))
        p23 = t23.get_parameter(name)
        if p23 is None:
            raise AttributeError(('"{}" is missing a required parameter: "{}".').format(t23.name, name))
        p43 = t43.get_parameter(name)
        if p43 is None:
            raise AttributeError(('"{}" is missing a required parameter: "{}".').format(t43.name, name))
        p14 = t14.get_parameter(name)
        if p14 is None:
            raise AttributeError(('"{}" is missing a required parameter: "{}".').format(t14.name, name))
        v12 = p12(**kwargs)
        v23 = p23(**kwargs)
        v43 = p43(**kwargs)
        v14 = p14(**kwargs)
        if x == 0.0:
            return v14
        else:
            if x == 1.0:
                return v23
            else:
                if y == 0.0:
                    return v12
                if y == 1.0:
                    return v43
                xinv = 1.0 - x
                yinv = 1.0 - y
                xweight = x * xinv
                yweight = y * yinv
                num = xweight * (yinv * v12 + y * v43) + yweight * (xinv * v14 + x * v23)
                denom = xweight + yweight
                C = self._get_bowing(name, kwargs)
                if C is not None:
                    return num / denom - C * xweight * yweight
                return num / denom

            return