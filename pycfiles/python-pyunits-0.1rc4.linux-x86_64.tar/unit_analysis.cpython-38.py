# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.0/x64/lib/python3.8/site-packages/pyunits/compound_units/unit_analysis.py
# Compiled at: 2019-11-23 19:40:19
# Size of source mod 2**32: 17235 bytes
from typing import Any, cast, Dict, Iterable, List, Mapping, NoReturn, Tuple, Union
import functools, numpy as np
from ..unitless import Unitless, UnitlessType
from ..unit_interface import UnitInterface
from ..unit_type import UnitType
from ..types import CompoundTypeFactories
from .operations import Operation
CompoundUnitOrType = Union[('compound_unit_type.CompoundUnitType', 'compound_unit.CompoundUnit')]
UnitOrType = Union[(UnitType, UnitInterface)]

def _is_product(to_check: Any) -> bool:
    """
    Checks whether something represents a product of two other units.
    :param to_check: The argument to check
    :return: True if it is a product, false otherwise.
    """
    if getattr(to_check, 'operation', None) == Operation.MUL:
        return True
    return False


def _is_fraction(to_check: Any) -> bool:
    """
    Checks whether something represents one unit divided by another.
    :param to_check: The argument to check.
    :return: True if it is a fraction, false otherwise.
    """
    if getattr(to_check, 'operation', None) == Operation.DIV:
        return True
    return False


def _collapse_unitless(product: Mapping[(UnitType, int)], remove_all: bool=False) -> Tuple[(bool, Dict[(UnitType, int)])]:
    """
    Removes redundant unitless types from a product of unit types.
    :param product: The product of unit types, as a map where each key is one
    of the types being multiplied, and the value is the power for that type.
    :param remove_all: If False, it will always leave at least 1 UnitlessType.
    Otherwise, it is permitted to return an empty dict if it is passed only
    UnitlessTypes.
    :return: A boolean indicating whether the output is different from
    the input, and the same product, but with redundant unitless types removed.
    """
    simplified = {}
    modified = False
    for unit_type, power in product.items():
        if isinstance(unit_type, UnitlessType) and not remove_all:
            if len(product) == 1:
                simplified[unit_type] = 1
                modified = power != 1
            else:
                modified = True
        else:
            simplified[unit_type] = power
    else:
        return (
         modified, simplified)


def _canonicalize_types(products: Iterable[Dict[(UnitType, int)]]) -> Tuple[(bool, List[Dict[(UnitType, int)]])]:
    """
    Sometimes, we might end up with a compound unit type that has multiple
    instances of the same UnitType in it. For instance, consider the type
    in * m. In order to avoid dealing with this nastiness, our policy is to
    choose one "canonical" instance of each UnitType and only use that in the
    CompoundUnit. Given products of UnitTypes that potentially contain
    multiple instances of the same class, this function manipulates them such
    that collectively, they only contains one instance. (It will always use an
    instance that produces the standard unit.)
    For example, as mentioned above, if we pass it {in: 1, m: 1}, it would
    return {m: 1}, assuming meters are defined as the standard unit.
    :param products: The products of UnitTypes to canonicalize.
    :return: Whether the input was modified, and the canonicalized products, in
    the same order as the input.
    """
    type_class_to_instance = {}

    def _collect_canonical(product):
        """
        Helper function that canonicalizes a single product dict.
        :param product: The product to canonicalize.
        :return: True if the input is not already canonical, false otherwise.
        """
        input_is_canonical = True
        for unit_type in product:
            unit_type_class = unit_type.__class__
            if unit_type_class not in type_class_to_instance:
                type_class_to_instance[unit_type_class] = unit_type
            else:
                if unit_type != type_class_to_instance[unit_type_class]:
                    type_class_to_instance[unit_type_class] = unit_type.standard_unit_class()
                    input_is_canonical = False
                return not input_is_canonical

    def _rebuild_product(product):
        """
        Re-makes an existing product using only canonical instances.
        :param product: The product to re-build.
        :return: The re-built product, containing only canonical instances.
        """
        canonical_product = {}
        for unit_type, power in product.items():
            canonical_instance = type_class_to_instance[unit_type.__class__]
            if canonical_instance not in canonical_product:
                canonical_product[canonical_instance] = 0
            canonical_product[canonical_instance] += power
        else:
            return canonical_product

    any_changed = False
    for one_product in products:
        one_not_canonical = _collect_canonical(one_product)
        any_changed = any_changed or one_not_canonical
    else:
        if not any_changed:
            return (any_changed, products)
        canonical_products = []
        for one_product in products:
            one_canonical = _rebuild_product(one_product)
            canonical_products.append(one_canonical)
        else:
            return (
             any_changed, canonical_products)


def flatten(to_flatten: UnitOrType) -> Tuple[(Dict[(UnitOrType, int)],
 Dict[(UnitOrType, int)])]:
    """
    Decomposes a Unit or UnitType into a set of sub-units or sub-types that make
    up the numerator and denominator. None of these sub-units or sub-types will
    be compound.
    :param to_flatten: The Unit or UnitType to flatten.
    :return: The set of sub-units or sub-types that make up the numerator and
    denominator, with the corresponding power of each one.
    """
    numerator = {}
    denominator = {}
    expandable_numerator = [
     to_flatten]
    expandable_denominator = []

    def flatten_compound(maybe_compound, invert=False):
        """
        Tries to flatten a UnitType.
        :param maybe_compound: The unit to expand, which might be a compound
        unit.
        :param invert: If true, it will be assumed that we are expanding
        something in the denominator, and therefore, should invert the logic
        for deciding which sub-units go in the numerator and which go in the
        denominator.
        :return: True if the unit was a compound unit and was expanded, false
        otherwise.
        """
        as_compound = cast(CompoundUnitOrType, maybe_compound)
        same_side = expandable_numerator
        other_side = expandable_denominator
        if invert:
            same_side = expandable_denominator
            other_side = expandable_numerator
        if _is_product(maybe_compound):
            same_side.append(as_compound.left)
            same_side.append(as_compound.right)
            return True
        if _is_fraction(maybe_compound):
            same_side.append(as_compound.left)
            other_side.append(as_compound.right)
            return True
        return False

    while not expandable_numerator:
        if expandable_denominator:
            if expandable_numerator:
                to_expand = expandable_numerator.pop()
                if not flatten_compound(to_expand):
                    if to_expand not in numerator:
                        numerator[to_expand] = 0
                    numerator[to_expand] += 1
            if expandable_denominator:
                to_expand = expandable_denominator.pop()
                if not flatten_compound(to_expand, invert=True):
                    if to_expand not in denominator:
                        denominator[to_expand] = 0
                    denominator[to_expand] += 1

    return (
     numerator, denominator)


def un_flatten(numerator: Mapping[(UnitType, int)], denominator: Mapping[(UnitType, int)], type_factories: CompoundTypeFactories) -> UnitType:
    """
    Converts flattened sets of numerator and denominator types to a single
    CompoundUnitType.
    :param numerator: The set of numerator types with corresponding powers.
    :param denominator: The set of denominator types with corresponding powers.
    :param type_factories: The factories that we will use for creating new
    CompoundUnitTypes.
    :return: The CompoundUnitType it created.
    """

    def build_product(operands):
        """
        Builds a single CompoundUnitType from a set of types that we want to
        multiply together.
        :param operands: The types that we want to multiply.
        :return: The single CompoundUnitType it created.
        """
        reduced = list(operands)
        while len(reduced) > 1:
            to_reduce = reduced
            reduced = []
            while True:
                if to_reduce:
                    next_reduced = to_reduce.pop()
                    if to_reduce:
                        mul_with = to_reduce.pop()
                        next_reduced = type_factories.mul(next_reduced, mul_with)
                    reduced.append(next_reduced)

        return reduced[0]

    def expand_powers(operands: Mapping[(UnitType, int)]) -> List[UnitType]:
        """
        Expands a set of UnitTypes from a dictionary of types and corresponding
        powers to a list of types where some may appear more than once.
        :param operands: The dictionary mapping UnitTypes to powers.
        :return: A list of the same UnitTypes.
        """
        expanded = []
        for unit_type, power in operands.items():
            expanded.extend([unit_type for _ in range(power)])
        else:
            return expanded

    numerator = expand_powers(numerator)
    denominator = expand_powers(denominator)
    if not numerator:
        prod_numerator = Unitless
    else:
        prod_numerator = build_product(numerator)
    if not denominator:
        return prod_numerator
    prod_denominator = build_product(denominator)
    return type_factories.div(prod_numerator, prod_denominator)


@functools.singledispatch
def simplify(to_simplify: Any, type_factories: CompoundTypeFactories) -> NoReturn:
    """
    Takes an input, and puts it in the simplest possible form. For instance,
    we pass it CompoundUnitType representing (m * s) / s ^ 2, it would return a
    CompoundUnitType representing m / s. This works for both units and types.

    A note about conversions: This function is happy to perform implicit
    conversions. For instance, it will successfully simplify something like
    (N * m) / (in * s), because we have an implicit conversion from in to m.
    However, if this is a UnitType, equivalent instances of the simplified and
    non-simplified versions will have different raw values. This is something
    to be aware of when simplifying UnitTypes.

    If it is a Unit that is being simplified instead, these conversions are
    performed automatically, and the result will have the correct raw value.
    :param to_simplify: The UnitType to simplify.
    :param type_factories: The factories that we will use for creating new
    CompoundUnitTypes.
    :return: If no simplification can be performed, it simply returns the input.
    Otherwise, it returns a new, equivalent UnitType or Unit in the simplest
    form possible.
    """
    raise NotImplementedError('simplify() is not implemented for {}.'.format(to_simplify))


@simplify.register(UnitType)
def simplify_type(to_simplify: UnitType, type_factories: CompoundTypeFactories) -> UnitType:
    numerator, denominator = flatten(to_simplify)
    collapsed_num_changed, numerator = _collapse_unitless(numerator)
    collapsed_denom_changed, denominator = _collapse_unitless(denominator, remove_all=True)
    canonical_changed, as_canonical = _canonicalize_types((
     numerator, denominator))
    numerator, denominator = as_canonical
    any_changed = collapsed_num_changed or collapsed_denom_changed or canonical_changed
    redundant_types = []
    for divisor in denominator:
        if divisor in numerator:
            redundant_types.append(divisor)
    else:
        if not redundant_types:
            if not any_changed:
                return to_simplify

    for unit_type in redundant_types:
        decrease_by = min(numerator[unit_type], denominator[unit_type])
        denominator[unit_type] -= decrease_by
        if denominator[unit_type] == 0:
            denominator.pop(unit_type)
        numerator[unit_type] -= decrease_by
        if numerator[unit_type] == 0:
            numerator.pop(unit_type)
        return un_flatten(numerator, denominator, type_factories)


@simplify.register(UnitInterface)
def simplify_unit(to_simplify: UnitInterface, type_factories: CompoundTypeFactories) -> UnitInterface:
    numerator, denominator = flatten(to_simplify)
    types_to_classes = {}
    combined = numerator.copy()
    combined.update(denominator)
    for unit in combined:
        if unit.type_class not in types_to_classes:
            types_to_classes[unit.type_class] = set()
        types_to_classes[unit.type_class].add(unit.type)
    else:

        def should_standardize(_unit):
            """
        Comparison function that defines when a unit should be standardized.
        This should only be done when we have multiple unit classes that all
        share the same unit type. (Two instances of the same unit class should
        not prompt standardization.)
        :param _unit: The unit to consider.
        :return: Whether that unit should be standardized.
        """
            return len(types_to_classes[unit.type_class]) > 1

        raw_value = np.asarray(1.0)
        for unit, power in numerator.items():
            to_mul = unit
            if should_standardize(unit):
                to_mul = unit.to_standard()
            raw_value *= to_mul.raw ** power
        else:
            for unit, power in denominator.items():
                to_div = unit
                if should_standardize(unit):
                    to_div = unit.to_standard()
                raw_value /= to_div.raw ** power
            else:
                simple_type = simplify(to_simplify.type, type_factories)
                return simple_type(raw_value)