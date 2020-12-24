# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/symbols/predefined_variables.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 4012 bytes
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.symbols.variable_symbol import VariableSymbol, BlockType, VariableType

class PredefinedVariables(object):
    __doc__ = '\n    This class is used to store all predefined variables as generally available. \n    '
    name2variable = {}
    E_CONSTANT = 'e'
    TIME_CONSTANT = 't'

    @classmethod
    def register_variables(cls):
        """
        Registers the predefined variables.
        """
        cls.name2variable = {}
        cls._PredefinedVariables__register_euler_constant()
        cls._PredefinedVariables__register_time_constant()

    @classmethod
    def __register_predefined_type_variables(cls):
        """
        Registers all predefined type variables, e.g., mV and integer.
        """
        for name in PredefinedTypes.get_types().keys():
            symbol = VariableSymbol(name=name, block_type=BlockType.PREDEFINED, is_predefined=True, type_symbol=PredefinedTypes.get_type(name), variable_type=VariableType.TYPE)
            cls.name2variable[name] = symbol

    @classmethod
    def __register_euler_constant(cls):
        """
        Adds the euler constant e.
        """
        symbol = VariableSymbol(name='e', block_type=BlockType.STATE, is_predefined=True, type_symbol=PredefinedTypes.get_real_type(), variable_type=VariableType.VARIABLE)
        cls.name2variable[cls.E_CONSTANT] = symbol

    @classmethod
    def __register_time_constant(cls):
        """
        Adds the time constant t.
        """
        symbol = VariableSymbol(name='t', block_type=BlockType.STATE, is_predefined=True, type_symbol=PredefinedTypes.get_type('ms'), variable_type=VariableType.VARIABLE)
        cls.name2variable[cls.TIME_CONSTANT] = symbol

    @classmethod
    def get_time_constant(cls):
        """
        Returns a copy of the variable symbol representing the time constant t.    
        :return: a variable symbol.
        :rtype: VariableSymbol
        """
        return cls.name2variable[cls.TIME_CONSTANT]

    @classmethod
    def get_euler_constant(cls):
        """
        Returns a copy of the variable symbol representing the euler constant t.    
        :return: a variable symbol.
        :rtype: VariableSymbol
        """
        return cls.name2variable[cls.E_CONSTANT]

    @classmethod
    def get_variable(cls, name):
        """
        Returns the variable symbol belonging to the handed over name if such an element exists.
        :param name: the name of a symbol.
        :type name: str
        :return: a variable symbol if one exists, otherwise none
        :rtype: None or VariableSymbol
        """
        if name in cls.name2variable.keys():
            return cls.name2variable[name]
        else:
            return

    @classmethod
    def get_variables(cls):
        """
        Returns the list of all defined variables.
        :return: a list of variable symbols.
        :rtype: list(VariableSymbol)
        """
        return cls.name2variable