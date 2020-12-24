# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.0/x64/lib/python3.8/site-packages/pyunits/compound_units/compound_unit.py
# Compiled at: 2019-11-23 19:40:19
# Size of source mod 2**32: 4038 bytes
from typing import cast
import abc, functools
from ..arithmetic_helpers import do_mul, do_div, do_add
from ..types import CompoundTypeFactories, UnitValue
from ..unit_base import UnitBase
from ..unit_interface import UnitInterface
from .operations import Operation
from .unit_analysis import simplify
from . import compound_unit_type

class CompoundUnit(UnitBase, abc.ABC):
    __doc__ = '\n    A base class for compound units.\n    '

    def __init__(self, unit_type, left_unit, right_unit):
        """
        :param unit_type: The associated UnitType for this unit.
        :param left_unit:  The first unit value to multiply.
        :param right_unit: The second unit value to multiply.
        """
        super().__init__(unit_type)
        self._CompoundUnit__left_unit = left_unit
        self._CompoundUnit__right_unit = right_unit

    def __get_type_factories(self) -> CompoundTypeFactories:
        """
        Helper function that creates the proper CompoundTypeFactories
        record for this class.
        :return: The CompoundTypeFactories that it created.
        """
        mul_type = functools.partial(self.type.get, Operation.MUL)
        div_type = functools.partial(self.type.get, Operation.DIV)
        return CompoundTypeFactories(mul=mul_type, div=div_type)

    def __mul__(self, other: UnitValue) -> UnitInterface:
        return do_mul(self._CompoundUnit__get_type_factories(), self, other)

    def __truediv__(self, other: UnitValue) -> UnitInterface:
        return do_div(self._CompoundUnit__get_type_factories(), self, other)

    def __rtruediv__(self, other: UnitValue) -> UnitInterface:
        return do_div(self._CompoundUnit__get_type_factories(), other, self)

    def __add__(self, other: UnitValue) -> UnitInterface:
        return do_add(self, other)

    def is_standard(self) -> bool:
        """
        See superclass for documentation.
        """
        return self.left.is_standard() and self.right.is_standard()

    def to_standard(self) -> UnitInterface:
        """
        See superclass for documentation.
        """
        standard_left = self._CompoundUnit__left_unit.to_standard()
        standard_right = self._CompoundUnit__right_unit.to_standard()
        standard_compound_type = self.type.standard_unit_class()
        standard_compound_type = cast('compound_unit_type.CompoundUnitType', standard_compound_type)
        standard = standard_compound_type.apply_to(standard_left, standard_right)
        return simplify(standard, self._CompoundUnit__get_type_factories())

    def cast_to(self, out_type: 'compound_unit_type.CompoundUnitType') -> 'CompoundUnit':
        """
        See superclass for documentation.
        """
        left_out_class = out_type.left
        right_out_class = out_type.right
        left_casted = self._CompoundUnit__left_unit.cast_to(left_out_class)
        right_casted = self._CompoundUnit__right_unit.cast_to(right_out_class)
        return out_type.apply_to(left_casted, right_casted)

    @property
    def left(self) -> UnitInterface:
        """
        :return: The unit that is the left-hand operand.
        """
        return self._CompoundUnit__left_unit

    @property
    def right(self) -> UnitInterface:
        """
        :return: The unit that is the right-hand operand.
        """
        return self._CompoundUnit__right_unit

    @property
    def operation(self) -> Operation:
        """
        :return: The operation performed by this unit.
        """
        my_type = cast(compound_unit_type.CompoundUnitType, self.type)
        return my_type.operation