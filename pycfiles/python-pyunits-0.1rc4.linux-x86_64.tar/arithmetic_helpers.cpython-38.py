# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.0/x64/lib/python3.8/site-packages/pyunits/arithmetic_helpers.py
# Compiled at: 2019-11-23 19:40:19
# Size of source mod 2**32: 3226 bytes
from .compound_units import unit_analysis
from .numeric_handling import WrapNumeric
from .types import CompoundTypeFactories
from .unit_interface import UnitInterface
from .unitless import Unitless

@WrapNumeric('left', 'right')
def do_mul(compound_type_factories: CompoundTypeFactories, left: UnitInterface, right: UnitInterface) -> UnitInterface:
    """
    Helper that implements the multiplication operation.
    :param compound_type_factories: The factories to use for creating
    CompoundUnitTypes.
    :param left: The left-hand unit to multiply.
    :param right: The right-hand unit to multiply.
    :return: The multiplication of the two units.
    """
    if right.type.is_compatible(left.type):
        left_class = left.type
        right = left_class(right)
    mul_unit_factory = compound_type_factories.mul(left.type, right.type)
    mul_unit = mul_unit_factory.apply_to(left, right)
    return unit_analysis.simplify(mul_unit, compound_type_factories)


@WrapNumeric('left', 'right')
def do_div(compound_type_factories: CompoundTypeFactories, left: UnitInterface, right: UnitInterface) -> UnitInterface:
    """
    Helper that implements the division operation.
    :param compound_type_factories: The factories to use for creating
    CompoundUnitTypes.
    :param left: The left-hand unit to multiply.
    :param right: The right-hand unit to multiply.
    :return: The quotient of the two units. Note that this can be a unitless
    value if the inputs are of the same UnitType.
    """
    if right.type.is_compatible(left.type):
        left_type = left.type
        right = left_type(right)
        return Unitless(left.raw / right.raw)
    div_unit_factory = compound_type_factories.div(left.type, right.type)
    div_unit = div_unit_factory.apply_to(left, right)
    return unit_analysis.simplify(div_unit, compound_type_factories)


@WrapNumeric('left', 'right')
def do_add(left: UnitInterface, right: UnitInterface) -> UnitInterface:
    """
    Helper that implements the addition operation.
    :param left: The left unit to add.
    :param right: The right unit to add.
    :return: The addition of the two units.
    """
    if left.type.is_compatible(Unitless):
        left = right.type(left.raw)
    else:
        if right.type.is_compatible(Unitless):
            right = left.type(left.raw)
    right = left.type(right)
    return left.type(left.raw + right.raw)