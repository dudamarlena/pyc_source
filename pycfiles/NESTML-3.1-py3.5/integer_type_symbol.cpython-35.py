# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/symbols/integer_type_symbol.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 4601 bytes
from pynestml.symbols.type_symbol import TypeSymbol

class IntegerTypeSymbol(TypeSymbol):

    def is_numeric(self):
        return True

    def is_primitive(self):
        return True

    def __init__(self):
        super(IntegerTypeSymbol, self).__init__(name='integer')

    def print_nestml_type(self):
        return 'integer'

    def __mul__(self, other):
        from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
        if other.is_instance_of(ErrorTypeSymbol):
            return other
        if other.is_numeric():
            return other
        return self.binary_operation_not_defined_error('*', other)

    def __mod__(self, other):
        from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
        if other.is_instance_of(ErrorTypeSymbol):
            return other
        if other.is_instance_of(IntegerTypeSymbol):
            return other
        return self.binary_operation_not_defined_error('%', other)

    def __truediv__(self, other):
        from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
        from pynestml.symbols.unit_type_symbol import UnitTypeSymbol
        if other.is_instance_of(ErrorTypeSymbol):
            return other
        if other.is_instance_of(UnitTypeSymbol):
            return self.inverse_of_unit(other)
        if other.is_numeric_primitive():
            return other
        return self.binary_operation_not_defined_error('/', other)

    def __div__(self, other):
        return self.__truediv__(other)

    def __neg__(self):
        return self

    def __pos__(self):
        return self

    def __invert__(self):
        return self

    def __pow__(self, power, modulo=None):
        from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
        from pynestml.symbols.real_type_symbol import RealTypeSymbol
        if power.is_instance_of(ErrorTypeSymbol):
            return power
        if power.is_instance_of(IntegerTypeSymbol):
            return self
        if power.is_instance_of(RealTypeSymbol):
            return power
        return self.binary_operation_not_defined_error('**', power)

    def __add__(self, other):
        from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
        from pynestml.symbols.string_type_symbol import StringTypeSymbol
        from pynestml.symbols.real_type_symbol import RealTypeSymbol
        from pynestml.symbols.unit_type_symbol import UnitTypeSymbol
        if other.is_instance_of(ErrorTypeSymbol):
            return other
        if other.is_instance_of(StringTypeSymbol):
            return other
        if other.is_instance_of(IntegerTypeSymbol):
            return other
        if other.is_instance_of(RealTypeSymbol):
            return other
        if other.is_instance_of(UnitTypeSymbol):
            return self.warn_implicit_cast_from_to(other, self)
        return self.binary_operation_not_defined_error('+', other)

    def __sub__(self, other):
        from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
        from pynestml.symbols.real_type_symbol import RealTypeSymbol
        from pynestml.symbols.unit_type_symbol import UnitTypeSymbol
        if other.is_instance_of(ErrorTypeSymbol):
            return other
        if other.is_instance_of(IntegerTypeSymbol):
            return other
        if other.is_instance_of(RealTypeSymbol):
            return other
        if other.is_instance_of(UnitTypeSymbol):
            return self.warn_implicit_cast_from_to(self, other)
        return self.binary_operation_not_defined_error('-', other)

    def is_castable_to(self, _other_type):
        if super(IntegerTypeSymbol, self).is_castable_to(_other_type):
            return True
        else:
            from pynestml.symbols.real_type_symbol import RealTypeSymbol
            if _other_type.is_instance_of(RealTypeSymbol):
                return True
            return False