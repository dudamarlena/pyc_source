# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/symbols/predefined_types.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 8920 bytes
from copy import copy
from astropy.units.core import CompositeUnit
from astropy.units.quantity import Quantity
from pynestml.symbols.predefined_units import PredefinedUnits
from pynestml.symbols.unit_type_symbol import UnitTypeSymbol
from pynestml.symbols.template_type_symbol import TemplateTypeSymbol
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages
from pynestml.utils.type_dictionary import TypeDictionary
from pynestml.utils.unit_type import UnitType

class PredefinedTypes(object):
    __doc__ = "\n    This class represents all types which are predefined in the system.\n    \n    Attributes:\n        name2type     A dict from names of variables to the corresponding type symbols. Type: dict(str->TypeSymbol)\n        REAL_TYPE     The identifier of the type 'real'. Type: str\n        VOID_TYPE     The identifier of the type 'void'. Type: str\n        BOOLEAN_TYPE  The identifier of the type 'boolean'. Type: str\n        STRING_TYPE   The identifier of the type 'string'. Type: str\n        INTEGER_TYPE  The identifier of the type 'integer'. Type: str\n    "
    name2type = {}
    REAL_TYPE = 'real'
    VOID_TYPE = 'void'
    BOOLEAN_TYPE = 'boolean'
    STRING_TYPE = 'string'
    INTEGER_TYPE = 'integer'

    @classmethod
    def register_types(cls):
        """
        Adds a set of primitive and unit data types to the set of predefined types. It assures that those types are
        valid and can be used.
        """
        cls.name2type = TypeDictionary()
        cls._PredefinedTypes__register_units()
        cls._PredefinedTypes__register_real()
        cls._PredefinedTypes__register_void()
        cls._PredefinedTypes__register_boolean()
        cls._PredefinedTypes__register_string()
        cls._PredefinedTypes__register_integer()

    @classmethod
    def __register_units(cls):
        """
        Adds all units as predefined type symbols to the list of available types.
        """
        from pynestml.symbols.predefined_units import PredefinedUnits
        from pynestml.symbols.unit_type_symbol import UnitTypeSymbol
        units = PredefinedUnits.get_units()
        for unitName in units.keys():
            type_symbol = UnitTypeSymbol(unit=units[unitName])
            cls.name2type[unitName] = type_symbol

    @classmethod
    def __register_real(cls):
        """
        Adds the real type symbol to the dict of predefined types.
        """
        from pynestml.symbols.real_type_symbol import RealTypeSymbol
        symbol = RealTypeSymbol()
        cls.name2type[symbol.get_symbol_name()] = symbol

    @classmethod
    def __register_void(cls):
        """
        Adds the void type to the dict of predefined types.
        """
        from pynestml.symbols.void_type_symbol import VoidTypeSymbol
        symbol = VoidTypeSymbol()
        cls.name2type[symbol.get_symbol_name()] = symbol

    @classmethod
    def __register_boolean(cls):
        """
        Adds the boolean type to the dict of predefined types.
        """
        from pynestml.symbols.boolean_type_symbol import BooleanTypeSymbol
        symbol = BooleanTypeSymbol()
        cls.name2type[symbol.get_symbol_name()] = symbol

    @classmethod
    def __register_string(cls):
        """
        Adds the string type to the dict of predefined types.
        """
        from pynestml.symbols.string_type_symbol import StringTypeSymbol
        symbol = StringTypeSymbol()
        cls.name2type[symbol.get_symbol_name()] = symbol

    @classmethod
    def __register_integer(cls):
        """
        Adds the integer type to the dict of predefined types.
        """
        from pynestml.symbols.integer_type_symbol import IntegerTypeSymbol
        symbol = IntegerTypeSymbol()
        cls.name2type[symbol.get_symbol_name()] = symbol

    @classmethod
    def get_types(cls):
        """
        Returns the list of all predefined types.
        :return: a copy of a list of all predefined types.
        :rtype: copy(list(TypeSymbol)
        """
        return cls.name2type

    @classmethod
    def get_buffer_type_if_exists(cls, name):
        result = copy(cls.get_type(name))
        result.is_buffer = True
        return result

    @classmethod
    def get_type(cls, name):
        """
        Return a TypeSymbol for
        -registered types
        -Correct SI Units in name ("ms")
        -Correct Serializations of a UnitRepresentation

        In Case of UNITS always return a TS with serialization as name
        :param name: the name of the symbol. 
        :type name: str or unit
        :return: a single symbol copy or none
        :rtype: type_symbol or None
        """
        if isinstance(name, Quantity) and name.unit == '':
            if name.value == 1.0 or name.value == 1:
                return cls.get_real_type()
            cls.register_unit(name)
            return cls.get_type(str(name))
        else:
            if isinstance(name, CompositeUnit) and len(name.bases) == 0:
                return cls.get_real_type()
            if isinstance(name, CompositeUnit):
                cls.register_unit(name)
                return cls.get_type(str(name))
            if isinstance(name, Quantity):
                cls.register_unit(name.unit)
                return cls.get_type(str(name.unit))
            if name in cls.name2type:
                return cls.name2type[name]
            return

    @classmethod
    def get_real_type(cls):
        """
        Returns a copy of the type symbol of type real.
        :return: a real symbol.
        :rtype: type_symbol
        """
        return cls.name2type[cls.REAL_TYPE]

    @classmethod
    def get_void_type(cls):
        """
        Returns a copy of the type symbol of type void.
        :return: a void symbol.
        :rtype: type_symbol
        """
        return cls.name2type[cls.VOID_TYPE]

    @classmethod
    def get_boolean_type(cls):
        """
        Returns a copy of the type symbol of type boolean.
        :return: a boolean symbol.
        :rtype: type_symbol
        """
        return cls.name2type[cls.BOOLEAN_TYPE]

    @classmethod
    def get_string_type(cls):
        """
        Returns a copy of the type symbol of type string.
        :return: a new string symbol.
        :rtype: type_symbol
        """
        return cls.name2type[cls.STRING_TYPE]

    @classmethod
    def get_integer_type(cls):
        """
        Returns a new type symbol of type integer.
        :return: a new integer symbol.
        :rtype: type_symbol
        """
        return cls.name2type[cls.INTEGER_TYPE]

    @classmethod
    def get_template_type(cls, i):
        """
        Returns a new type symbol for argument type templating. The template types are uniquely identified with an integer number `i` (see TemplateTypeSymbol).
        :return: a new integer symbol.
        :rtype: type_symbol
        """
        return TemplateTypeSymbol(i)

    @classmethod
    def register_type(cls, symbol):
        """
        Registers a new type into the system.
        :param: a single type symbol.
        :type: UnitTypeSymbol
        """
        if not symbol.is_primitive() and symbol.unit.get_name() not in cls.name2type.keys():
            cls.name2type[symbol.unit.get_name()] = symbol
            code, message = Messages.get_new_type_registered(symbol.unit.get_name())
            Logger.log_message(code=code, message=message, log_level=LoggingLevel.INFO)

    @classmethod
    def register_unit(cls, unit):
        """
        Registers a new astropy unit into the system
        :param unit: an astropy Unit object
        :type unit: astropy.units.core.Unit
        """
        unit_type = UnitType(str(unit), unit)
        PredefinedUnits.register_unit(unit_type)
        type_symbol = UnitTypeSymbol(unit=unit_type)
        cls.register_type(type_symbol)