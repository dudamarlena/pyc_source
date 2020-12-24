# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/codegeneration/pynestml_2_nest_type_converter.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2667 bytes
from pynestml.symbols.type_symbol import TypeSymbol
from pynestml.symbols.real_type_symbol import RealTypeSymbol
from pynestml.symbols.boolean_type_symbol import BooleanTypeSymbol
from pynestml.symbols.integer_type_symbol import IntegerTypeSymbol
from pynestml.symbols.string_type_symbol import StringTypeSymbol
from pynestml.symbols.void_type_symbol import VoidTypeSymbol
from pynestml.symbols.unit_type_symbol import UnitTypeSymbol
from pynestml.symbols.nest_time_type_symbol import NESTTimeTypeSymbol
from pynestml.symbols.error_type_symbol import ErrorTypeSymbol

class PyNestml2NestTypeConverter(object):
    __doc__ = '\n    This class contains a single operation as used to convert nestml types to nest centerpieces.\n    '

    @classmethod
    def convert(cls, type_symbol):
        """
        Converts the name of the type symbol to a corresponding nest representation.
        :param type_symbol: a single type symbol
        :type type_symbol: TypeSymbol
        :return: the corresponding string representation.
        :rtype: str
        """
        assert isinstance(type_symbol, TypeSymbol)
        if type_symbol.is_buffer:
            return 'nest::RingBuffer'
        if isinstance(type_symbol, RealTypeSymbol):
            return 'double'
        if isinstance(type_symbol, BooleanTypeSymbol):
            return 'bool'
        if isinstance(type_symbol, IntegerTypeSymbol):
            return 'long'
        if isinstance(type_symbol, StringTypeSymbol):
            return 'std::string'
        if isinstance(type_symbol, VoidTypeSymbol):
            return 'void'
        if isinstance(type_symbol, UnitTypeSymbol):
            return 'double'
        if isinstance(type_symbol, NESTTimeTypeSymbol):
            return 'nest::Time'
        if isinstance(type_symbol, ErrorTypeSymbol):
            return 'ERROR'
        raise Exception('Unknown NEST type')