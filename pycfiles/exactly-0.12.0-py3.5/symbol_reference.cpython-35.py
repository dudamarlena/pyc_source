# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/matcher/impls/symbol_reference.py
# Compiled at: 2019-12-27 10:07:45
# Size of source mod 2**32: 1626 bytes
from typing import Sequence
from exactly_lib.symbol import lookups
from exactly_lib.symbol.logic.matcher import MatcherSdv, MODEL
from exactly_lib.symbol.restriction import ValueTypeRestriction
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.type_system.logic.matcher_base_class import MatcherDdv
from exactly_lib.type_system.value_type import ValueType
from exactly_lib.util.symbol_table import SymbolTable

class MatcherReferenceSdv(MatcherSdv[MODEL]):
    __doc__ = '\n    A :class:`MatcherSdv` that is a reference to a symbol\n    '
    _TYPE_LOOKUP = {ValueType.LINE_MATCHER: lookups.lookup_line_matcher, 
     ValueType.FILE_MATCHER: lookups.lookup_file_matcher, 
     ValueType.FILES_MATCHER: lookups.lookup_files_matcher, 
     ValueType.STRING_MATCHER: lookups.lookup_string_matcher}

    def __init__(self, name_of_referenced_sdv: str, value_type: ValueType):
        self._name_of_referenced_sdv = name_of_referenced_sdv
        self._value_type = value_type
        self._references = [
         SymbolReference(name_of_referenced_sdv, ValueTypeRestriction(value_type))]

    def resolve(self, symbols: SymbolTable) -> MatcherDdv[MODEL]:
        lookup_fun = self._TYPE_LOOKUP[self._value_type]
        sdv = lookup_fun(symbols, self._name_of_referenced_sdv)
        return sdv.resolve(symbols)

    @property
    def references(self) -> Sequence[SymbolReference]:
        return self._references

    def __str__(self):
        return str(type(self)) + "'" + str(self._name_of_referenced_sdv) + "'"