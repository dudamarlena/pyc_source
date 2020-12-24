# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/codegeneration/nest_names_converter.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 4209 bytes
from pynestml.meta_model.ast_variable import ASTVariable
from pynestml.symbols.variable_symbol import VariableSymbol

class NestNamesConverter(object):
    __doc__ = '\n    This class provides several methods which can be used to convert names of objects to the corresponding\n    nest representation.\n    '

    @classmethod
    def name(cls, node):
        """
        Returns for the handed over element the corresponding nest processable string.
        :param node: a single variable symbol or variable
        :type node: VariableSymbol or ASTVariable
        :return: the corresponding string representation
        :rtype: str
        """
        if isinstance(node, VariableSymbol):
            return cls.convert_to_cpp_name(node.get_symbol_name())
        else:
            return cls.convert_to_cpp_name(node.get_complete_name())

    @classmethod
    def getter(cls, variable_symbol):
        """
        Converts for a handed over symbol the corresponding name of the getter to a nest processable format.
        :param variable_symbol: a single variable symbol.
        :type variable_symbol: VariableSymbol
        :return: the corresponding representation as a string
        :rtype: str
        """
        assert isinstance(variable_symbol, VariableSymbol), '(PyNestML.CodeGeneration.NamesConverter) No or wrong type of variable symbol provided (%s)!' % type(variable_symbol)
        return 'get_' + cls.convert_to_cpp_name(variable_symbol.get_symbol_name())

    @classmethod
    def buffer_value(cls, variable_symbol):
        """
        Converts for a handed over symbol the corresponding name of the buffer to a nest processable format.
        :param variable_symbol: a single variable symbol.
        :type variable_symbol: VariableSymbol
        :return: the corresponding representation as a string
        :rtype: str
        """
        assert isinstance(variable_symbol, VariableSymbol), '(PyNestML.CodeGeneration.NamesConverter) No or wrong type of variable symbol provided (%s)!' % type(variable_symbol)
        return variable_symbol.get_symbol_name() + '_grid_sum_'

    @classmethod
    def setter(cls, variable_symbol):
        """
        Converts for a handed over symbol the corresponding name of the setter to a nest processable format.
        :param variable_symbol: a single variable symbol.
        :type variable_symbol: VariableSymbol
        :return: the corresponding representation as a string
        :rtype: str
        """
        assert isinstance(variable_symbol, VariableSymbol), '(PyNestML.CodeGeneration.NamesConverter) No or wrong type of variable symbol provided (%s)!' % type(variable_symbol)
        return 'set_' + cls.convert_to_cpp_name(variable_symbol.get_symbol_name())

    @classmethod
    def convert_to_cpp_name(cls, variable_name):
        """
        Converts a handed over name to the corresponding nest / c++ naming guideline.
        In concrete terms:
            Converts names of the form g_in'' to a compilable C++ identifier: __DDX_g_in
        :param variable_name: a single name.
        :type variable_name: str
        :return: the corresponding transformed name.
        :rtype: str
        """
        differential_order = variable_name.count("'")
        if differential_order > 0:
            return '__' + 'D' * differential_order + '_' + variable_name.replace("'", '')
        else:
            return variable_name