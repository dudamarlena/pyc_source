# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/symbols/nest_time_type_symbol.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 1456 bytes
from pynestml.symbols.type_symbol import TypeSymbol

class NESTTimeTypeSymbol(TypeSymbol):

    def is_numeric(self):
        return False

    def is_primitive(self):
        return False

    def __init__(self):
        super(NESTTimeTypeSymbol, self).__init__(name='time')

    def print_nestml_type(self):
        return 'time'

    def __add__(self, other):
        from pynestml.symbols.string_type_symbol import StringTypeSymbol
        if other.is_instance_of(StringTypeSymbol):
            return other
        return self.binary_operation_not_defined_error('+', other)

    def is_castable_to(self, _other_type):
        if super(NESTTimeTypeSymbol, self).is_castable_to(_other_type):
            return True
        return False