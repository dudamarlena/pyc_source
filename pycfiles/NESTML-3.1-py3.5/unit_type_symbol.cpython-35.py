# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/symbols/unit_type_symbol.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 6450 bytes
from pynestml.symbols.type_symbol import TypeSymbol
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import Messages
from pynestml.utils.unit_type import UnitType

class UnitTypeSymbol(TypeSymbol):

    @property
    def astropy_unit(self):
        return self.unit.get_unit()

    def is_numeric(self):
        return True

    def is_primitive(self):
        return False

    def __init__(self, unit):
        assert isinstance(unit, UnitType)
        self.unit = unit
        super(UnitTypeSymbol, self).__init__(name=unit.name)

    def print_nestml_type(self):
        return self.unit.print_unit()

    def equals(self, other=None):
        basic_equals = super(UnitTypeSymbol, self).equals(other)
        if basic_equals is True:
            return self.unit == other.unit
        return False

    def __mul__(self, other):
        from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
        if other.is_instance_of(ErrorTypeSymbol):
            return other
        if other.is_instance_of(UnitTypeSymbol):
            return self.multiply_by(other)
        if other.is_numeric_primitive():
            return self
        return self.binary_operation_not_defined_error('*', other)

    def multiply_by(self, other):
        from pynestml.symbols.predefined_types import PredefinedTypes
        return PredefinedTypes.get_type(self.astropy_unit * other.astropy_unit)

    def __truediv__(self, other):
        from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
        if other.is_instance_of(ErrorTypeSymbol):
            return other
        if other.is_instance_of(UnitTypeSymbol):
            return self.divide_by(other)
        if other.is_numeric_primitive():
            return self
        return self.binary_operation_not_defined_error('/', other)

    def __div__(self, other):
        return self.__truediv__(other)

    def divide_by(self, other):
        from pynestml.symbols.predefined_types import PredefinedTypes
        return PredefinedTypes.get_type(self.astropy_unit / other.astropy_unit)

    def __neg__(self):
        return self

    def __pos__(self):
        return self

    def __invert__(self):
        return self.unary_operation_not_defined_error('~')

    def __pow__(self, power, modulo=None):
        from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
        if isinstance(power, ErrorTypeSymbol):
            return power
        if isinstance(power, int) or isinstance(power, float):
            return self.to_the_power_of(power)
        return self.binary_operation_not_defined_error('**', power)

    def to_the_power_of(self, power):
        from pynestml.symbols.predefined_types import PredefinedTypes
        return PredefinedTypes.get_type(self.astropy_unit ** power)

    def __add__(self, other):
        from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
        from pynestml.symbols.string_type_symbol import StringTypeSymbol
        if other.is_instance_of(ErrorTypeSymbol):
            return other
        if other.is_instance_of(StringTypeSymbol):
            return other
        if other.is_numeric_primitive():
            return self.warn_implicit_cast_from_to(other, self)
        if other.is_instance_of(UnitTypeSymbol):
            return self.add_or_sub_another_unit(other)
        return self.binary_operation_not_defined_error('+', other)

    def __sub__(self, other):
        from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
        if other.is_instance_of(ErrorTypeSymbol):
            return other
        if other.is_numeric_primitive():
            return self.warn_implicit_cast_from_to(other, self)
        if other.is_instance_of(UnitTypeSymbol):
            return self.add_or_sub_another_unit(other)
        return self.binary_operation_not_defined_error('-', other)

    def add_or_sub_another_unit(self, other):
        if self.equals(other):
            return other
        else:
            return self.attempt_magnitude_cast(other)

    def attempt_magnitude_cast(self, other):
        if self.differs_only_in_magnitude(other):
            factor = UnitTypeSymbol.get_conversion_factor(self.astropy_unit, other.astropy_unit)
            other.referenced_object.set_implicit_conversion_factor(factor)
            code, message = Messages.get_implicit_magnitude_conversion(self, other, factor)
            Logger.log_message(code=code, message=message, error_position=self.referenced_object.get_source_position(), log_level=LoggingLevel.WARNING)
            return self
        else:
            return self.binary_operation_not_defined_error('+/-', other)

    @classmethod
    def get_conversion_factor(cls, to, _from):
        """
        Calculates the conversion factor from _convertee_unit to target_unit.
        Behaviour is only well-defined if both units have the same physical base type
        """
        factor = (_from / to).si.scale
        return factor

    def is_castable_to(self, _other_type):
        if super(UnitTypeSymbol, self).is_castable_to(_other_type):
            return True
        from pynestml.symbols.real_type_symbol import RealTypeSymbol
        if _other_type.is_instance_of(RealTypeSymbol):
            return True
        try:
            self.unit.get_unit().to(_other_type.unit.get_unit())
            return True
        except:
            return False