# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/schema/transform/type.py
# Compiled at: 2018-12-02 18:39:57
# Size of source mod 2**32: 2845 bytes
from decimal import Decimal as DecimalType
from .base import Concern, Transform, Attribute, CallbackTransform

class Boolean(Transform):
    __doc__ = 'Convert boolean values.\n\t\n\tIntelligently handles boolean and non-string values, returning as-is and passing to the bool builtin resspectively.\n\t\n\tThis process is case-insensitive.  Acceptable values:\n\t\n\tTruthy: true, t, yes, y, on, 1, literal True\n\tFalsy: false, f, no, n, off, 0, literal False\n\t'
    use = Attribute(default=0)
    none = Attribute(default=True)
    truthy = Attribute(default=('true', 't', 'yes', 'y', 'on', '1', True))
    falsy = Attribute(default=('false', 'f', 'no', 'n', 'off', '0', False))

    def native(self, value, context=None):
        """Convert a foreign value to a native boolean."""
        value = super().native(value, context)
        if self.none:
            if value is None:
                return
        try:
            value = value.lower()
        except AttributeError:
            return bool(value)
        else:
            if value in self.truthy:
                return True
            if value in self.falsy:
                return False
            raise Concern('Unable to convert {0!r} to a boolean value.', value)

    def foreign(self, value, context=None):
        """Convert a native value to a textual boolean."""
        if self.none:
            if value is None:
                return ''
        try:
            value = self.native(value, context)
        except Concern:
            value = bool(value.strip() if (self.strip and hasattr(value, 'strip')) else value)

        if value in self.truthy or value:
            return self.truthy[self.use]
        return self.falsy[self.use]


boolean = Boolean()

class WebBoolean(Boolean):
    __doc__ = 'Some web frameworks and widget systems handle checkboxes by having a hidden form field and a checkbox.\n\t\n\tIf the checkbox is unchecked, you get the "default" value as the only value.  If the checkbox is checked, you end\n\tup with two values, one for the hidden field (False) and one for the checkbox (True); in this situation we only\n\ttake the last value defined.\n\t'
    none = Attribute(default=False)
    use = Attribute(default=(-1))
    falsy = Attribute(default=('', 'false', 'f', 'no', 'n', 'off', '0', False))

    def native(self, value, context=None):
        if isinstance(value, (tuple, list)):
            value = value[(-1)]
        return super().native(value, context)


web_boolean = WebBoolean()

class Integer(CallbackTransform):
    ingress = int
    egress = str


integer = Integer()

class Decimal(CallbackTransform):
    ingress = DecimalType
    egress = str


decimal = Decimal()

class Number(CallbackTransform):
    egress = str

    @staticmethod
    def ingress(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            pass

        try:
            return float(value)
        except (TypeError, ValueError):
            pass

        raise Concern('Unable to convert {0!r} to a number.', value)


number = Number()