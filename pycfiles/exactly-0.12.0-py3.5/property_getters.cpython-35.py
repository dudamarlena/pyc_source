# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/matcher/impls/property_getters.py
# Compiled at: 2019-12-27 10:07:45
# Size of source mod 2**32: 1917 bytes
from typing import Generic, Sequence, TypeVar
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.test_case_file_structure.tcds import Tcds
from exactly_lib.test_case_utils.matcher.property_getter import PropertyGetter, PropertyGetterDdv, PropertyGetterSdv, PropertyGetterAdv
from exactly_lib.test_case_utils.matcher.property_matcher import PROP_TYPE
from exactly_lib.type_system.description.tree_structured import StructureRenderer
from exactly_lib.type_system.logic.logic_base_class import ApplicationEnvironment
from exactly_lib.util.symbol_table import SymbolTable
T = TypeVar('T')

class PropertyGetterAdvConstant(PropertyGetterAdv[(PROP_TYPE, T)]):

    def __init__(self, constant: PropertyGetter[(PROP_TYPE, T)]):
        self._constant = constant

    def applier(self, environment: ApplicationEnvironment) -> PropertyGetter[(PROP_TYPE, T)]:
        return self._constant


class PropertyGetterDdvConstant(Generic[(PROP_TYPE, T)], PropertyGetterDdv[(PROP_TYPE, T)]):

    def __init__(self, constant: PropertyGetter[(PROP_TYPE, T)]):
        self._constant = constant

    def structure(self) -> StructureRenderer:
        return self._constant.structure()

    def value_of_any_dependency(self, tcds: Tcds) -> PropertyGetterAdv[(PROP_TYPE, T)]:
        return PropertyGetterAdvConstant(self._constant)


class PropertyGetterSdvConstant(Generic[(PROP_TYPE, T)], PropertyGetterSdv[(PROP_TYPE, T)]):

    def __init__(self, constant: PropertyGetterDdv[(PROP_TYPE, T)]):
        self._constant = constant

    @property
    def references(self) -> Sequence[SymbolReference]:
        return ()

    def resolve(self, symbols: SymbolTable) -> PropertyGetterDdv[(PROP_TYPE, T)]:
        return self._constant


def sdv_of_constant_primitive(constant: PropertyGetter[(PROP_TYPE, T)]) -> PropertyGetterSdv[(PROP_TYPE, T)]:
    return PropertyGetterSdvConstant(PropertyGetterDdvConstant(constant))