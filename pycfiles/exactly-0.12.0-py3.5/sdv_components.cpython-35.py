# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/matcher/impls/sdv_components.py
# Compiled at: 2020-01-31 11:01:49
# Size of source mod 2**32: 1528 bytes
from typing import Sequence, Callable, Generic
from exactly_lib.symbol.logic.matcher import MatcherSdv, MODEL
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.type_system.logic.matcher_base_class import MatcherDdv, MatcherWTraceAndNegation
from exactly_lib.util.symbol_table import SymbolTable
from . import ddv_components

class MatcherSdvFromParts(Generic[MODEL], MatcherSdv[MODEL]):

    def __init__(self, references: Sequence[SymbolReference], make_ddv: Callable[([SymbolTable], MatcherDdv[MODEL])]):
        self._make_ddv = make_ddv
        self._references = references

    def resolve(self, symbols: SymbolTable) -> MatcherDdv[MODEL]:
        return self._make_ddv(symbols)

    @property
    def references(self) -> Sequence[SymbolReference]:
        return self._references

    def __str__(self):
        return str(type(self))


class MatcherSdvFromConstantDdv(Generic[MODEL], MatcherSdv[MODEL]):

    def __init__(self, ddv: MatcherDdv[MODEL]):
        self._ddv = ddv

    def resolve(self, symbols: SymbolTable) -> MatcherDdv[MODEL]:
        return self._ddv

    @property
    def references(self) -> Sequence[SymbolReference]:
        return []

    def __str__(self):
        return str(type(self)) + "'" + str(self._ddv) + "'"


def matcher_sdv_from_constant_primitive(primitive: MatcherWTraceAndNegation[MODEL]) -> MatcherSdv[MODEL]:
    return MatcherSdvFromConstantDdv(ddv_components.MatcherDdvFromConstantPrimitive(primitive))