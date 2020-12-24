# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/utils/unit_type.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3005 bytes
from astropy.units.core import PrefixUnit, Unit, IrreducibleUnit, CompositeUnit
from astropy.units.quantity import Quantity

class UnitType(object):
    __doc__ = '\n    This class is used to encapsulate the functionality of astropy.units in a new layer which provided additional functionality as required during context checks.\n\n    :attr name: The name of this unit.\n    :type name: str\n    :attr unit: The corresponding astropy Unit.\n    :type unit: astropy.units.core.Unit\n    '

    def __init__(self, name, unit):
        """
        Standard constructor.
        :param name: the name of this unit.
        :type name: str
        :param unit: an astropy Unit object
        :type unit: astropy.units.core.Unit
        """
        assert isinstance(name, str), '(PyNestML.SymbolTable.UnitType) No or wrong type of name provided (%s)!' % type(name)
        if not isinstance(unit, Unit):
            if not isinstance(unit, PrefixUnit):
                if not isinstance(unit, IrreducibleUnit):
                    if not isinstance(unit, CompositeUnit):
                        assert isinstance(unit, Quantity), '(PyNestML.SymbolTable.UnitType) No or wrong type of unit provided (%s)!' % type(unit)
        self.name = name
        self.unit = unit

    def get_name(self):
        """
        Returns the name of this unit.
        :return: the name of the unit.
        :rtype: str
        """
        return self.name

    def get_unit(self):
        """
        Returns the astropy unit of this unit.
        :return: the astropy unit
        :rtype: astropy.units.core.Unit
        """
        return self.unit

    def print_unit(self):
        """
        Returns a string representation of this unit symbol.
        :return: a string representation.
        :rtype: str
        """
        return str(self.get_unit())

    def equals(self, _obj=None):
        """
        Compares this to the handed object and checks if they are semantically equal.
        :param _obj: a single object
        :type _obj: object
        :return: True if equal, otherwise false.
        :rtype: bool
        """
        if not isinstance(_obj, UnitType):
            return False
        return self.get_name() == _obj.get_name() and self.get_unit() == _obj.get_unit()