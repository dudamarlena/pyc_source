# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.0/x64/lib/python3.8/site-packages/pyunits/compound_units/compound_unit_type.py
# Compiled at: 2019-11-23 19:40:19
# Size of source mod 2**32: 7575 bytes
from typing import cast, FrozenSet, Tuple, Union
from loguru import logger
from ..exceptions import UnitError
from ..types import UnitValue
from ..unit_interface import UnitInterface
from ..unit_type import UnitType
from .compound_unit import CompoundUnit
from .div_unit import DivUnit
from .mul_unit import MulUnit
from .operations import Operation

class CompoundUnitType(UnitType):
    __doc__ = '\n    Unit type that represents the multiplication of two units.\n    '
    OPERATION_TO_CLASS = {Operation.MUL: MulUnit, Operation.DIV: DivUnit}

    def _init_new(self, operation, left_unit_class, right_unit_class):
        """
        :param operation: The operation performed by the compound unit.
        :param left_unit_class: The class of the first unit to multiply.
        :param right_unit_class: The class of the second unit to multiply.
        """
        self._CompoundUnitType__enforce_compatibility_rules(operation, left_unit_class, right_unit_class)
        self._CompoundUnitType__operation = operation
        self._CompoundUnitType__left_unit_class = left_unit_class
        self._CompoundUnitType__right_unit_class = right_unit_class
        logger.debug('Creating new unit type {} with sub-units {} and {}.', operation.name, left_unit_class.__class__.__name__, right_unit_class.__class__.__name__)
        super()._init_new(self.OPERATION_TO_CLASS[operation])

    @classmethod
    def _pre_hash(cls, operation: Operation, left_unit_class: UnitType, right_unit_class: UnitType) -> Tuple[(Operation,
 Union[(FrozenSet[UnitType],
  Tuple[(UnitType, UnitType)])])]:
        """
        Transforms the arguments passed to get() before they are hashed, mainly
        so that equivalent product types hash to the same thing. See _init_new()
        for documentation on the parameters.
        :return: A tuple containing the arguments, with the left and right
        sub-types possibly in a set to indicate their lack of ordering.
        """
        sub_types = (
         left_unit_class, right_unit_class)
        if operation == Operation.MUL:
            sub_types = frozenset(sub_types)
        return (operation, sub_types)

    @staticmethod
    def __enforce_compatibility_rules(operation: Operation, left_type: UnitType, right_type: UnitType) -> None:
        """
        Enforces rules about the compatibility of the two sub-units. These are
        mostly there to stop us from creating nonsensical units like in / m.
        :param operation: The operation to perform.
        :param left_type: The left subtype.
        :param right_type: The right subtype.
        """
        will_accept = True
        if left_type.is_compatible(right_type):
            if operation == Operation.DIV:
                will_accept = False
            else:
                if left_type != right_type:
                    will_accept = False
        if not will_accept:
            raise UnitError('Sub-units {} and {} should not be compatible with each-other.'.format(left_type.__class__.__name__, right_type.__class__.__name__))

    @property
    def left(self) -> UnitType:
        """
        :return: The first UnitType to multiply.
        """
        return self._CompoundUnitType__left_unit_class

    @property
    def right(self) -> UnitType:
        """
        :return: The second UnitType to multiply.
        """
        return self._CompoundUnitType__right_unit_class

    @property
    def operation(self) -> Operation:
        """
        :return: The operation being applied.
        """
        return self._CompoundUnitType__operation

    def apply_to(self, left_unit, right_unit):
        """
        Applies the compound operation to two units.
        :param left_unit: The first unit to multiply.
        :param right_unit: The second unit to multiply.
        :return: A Unit representing the multiplication of the two.
        """
        left_unit = self._CompoundUnitType__left_unit_class(left_unit)
        right_unit = self._CompoundUnitType__right_unit_class(right_unit)
        compound_unit = super().__call__(left_unit, right_unit)
        return cast(CompoundUnit, compound_unit)

    def __call__(self, value):
        """
        Creates a new compound unit of this type.
        :param value: The same value, in other units, or as a raw Numpy array.
        :return: The Unit object.
        """
        if isinstance(value, UnitInterface):
            if not self.is_compatible(value.type):
                raise UnitError('A compound unit with operation {} must be initialized with another, not {}.'.format(self.operation, value.__class__.__name__))
            value = cast(CompoundUnit, value)
            return self.apply_to(value.left, value.right)
        left_unit = self._CompoundUnitType__left_unit_class(value)
        right_unit = self._CompoundUnitType__right_unit_class(1)
        compound_unit = super().__call__(left_unit, right_unit)
        return cast(CompoundUnit, compound_unit)

    def standard_unit_class(self) -> 'CompoundUnitType':
        """
        See superclass for documentation.
        """
        left_standard_class = self.left.standard_unit_class()
        right_standard_class = self.right.standard_unit_class()
        return self.get(self.operation, left_standard_class, right_standard_class)

    def is_compatible(self, other: UnitType) -> bool:
        """
        See superclass for documentation.
        """
        if not isinstance(other, CompoundUnitType):
            return False
        sub_units_compatible = other.left.is_compatible(self.left) and other.right.is_compatible(self.right)
        if self.operation == Operation.MUL:
            sub_units_compatible |= other.right.is_compatible(self.left) and other.left.is_compatible(self.right)
        return other.operation == self.operation and sub_units_compatible