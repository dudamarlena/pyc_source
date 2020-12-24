# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/codegeneration/gsl_names_converter.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3726 bytes
from pynestml.codegeneration.nest_names_converter import NestNamesConverter
from pynestml.symbols.variable_symbol import VariableSymbol

class GSLNamesConverter(object):
    __doc__ = '\n    A GSL names converter as use to transform names to GNU Scientific Library.\n    '

    @classmethod
    def array_index(cls, symbol):
        """
        Transforms the haded over symbol to a GSL processable format.
        :param symbol: a single variable symbol
        :type symbol: VariableSymbol
        :return: the corresponding string format
        :rtype: str
        """
        return 'State_::' + NestNamesConverter.convert_to_cpp_name(symbol.get_symbol_name())

    @classmethod
    def name(cls, symbol):
        """
        Transforms the haded over symbol to a GSL processable format.
        :param symbol: a single variable symbol
        :type symbol: VariableSymbol
        :return: the corresponding string format
        :rtype: str
        """
        if symbol.is_init_values() and not symbol.is_function:
            return 'ode_state[State_::' + NestNamesConverter.convert_to_cpp_name(symbol.get_symbol_name()) + ']'
        else:
            return NestNamesConverter.name(symbol)

    @classmethod
    def getter(cls, variable_symbol):
        """
        Converts for a handed over symbol the corresponding name of the getter to a gsl processable format.
        :param variable_symbol: a single variable symbol.
        :type variable_symbol: VariableSymbol
        :return: the corresponding representation as a string
        :rtype: str
        """
        return NestNamesConverter.getter(variable_symbol)

    @classmethod
    def setter(cls, variable_symbol):
        """
        Converts for a handed over symbol the corresponding name of the setter to a gsl processable format.
        :param variable_symbol: a single variable symbol.
        :type variable_symbol: VariableSymbol
        :return: the corresponding representation as a string
        :rtype: str
        """
        return NestNamesConverter.setter(variable_symbol)

    @classmethod
    def buffer_value(cls, variable_symbol):
        """
        Converts for a handed over symbol the corresponding name of the buffer to a gsl processable format.
        :param variable_symbol: a single variable symbol.
        :type variable_symbol: VariableSymbol
        :return: the corresponding representation as a string
        :rtype: str
        """
        return NestNamesConverter.buffer_value(variable_symbol)

    @classmethod
    def convert_to_cpp_name(cls, variable_name):
        """
        Converts a handed over name to the corresponding gsl / c++ naming guideline.
        In concrete terms:
            Converts names of the form g_in'' to a compilable C++ identifier: __DDX_g_in
        :param variable_name: a single name.
        :type variable_name: str
        :return: the corresponding transformed name.
        :rtype: str
        """
        return NestNamesConverter.convert_to_cpp_name(variable_name)