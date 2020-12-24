# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/string_transformer/sdvs.py
# Compiled at: 2019-12-27 10:07:41
# Size of source mod 2**32: 2446 bytes
from typing import Sequence
from exactly_lib.symbol import lookups
from exactly_lib.symbol.logic.string_transformer import StringTransformerSdv
from exactly_lib.symbol.restriction import ValueTypeRestriction
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.type_system.logic import string_transformer_ddvs
from exactly_lib.type_system.logic.string_transformer import StringTransformer, StringTransformerDdv
from exactly_lib.type_system.value_type import ValueType
from exactly_lib.util.symbol_table import SymbolTable

class StringTransformerSdvConstant(StringTransformerSdv):
    __doc__ = '\n    A :class:`LinesTransformerSdv` that is a constant :class:`LinesTransformer`\n    '

    def __init__(self, value: StringTransformer):
        self._value = string_transformer_ddvs.StringTransformerConstantDdv(value)

    def resolve(self, symbols: SymbolTable) -> StringTransformerDdv:
        return self._value

    @property
    def references(self) -> Sequence[SymbolReference]:
        return []

    def __str__(self):
        return str(type(self)) + "'" + str(self._value) + "'"


class StringTransformerSdvConstantOfDdv(StringTransformerSdv):
    __doc__ = '\n    A :class:`StringTransformerSdv` that is a constant :class:`StringTransformerDdv`\n    '

    def __init__(self, ddv: StringTransformerDdv):
        self._ddv = ddv

    def resolve(self, symbols: SymbolTable) -> StringTransformerDdv:
        return self._ddv

    @property
    def references(self) -> Sequence[SymbolReference]:
        return []

    def __str__(self):
        return str(type(self)) + "'" + str(self._ddv) + "'"


class StringTransformerSdvReference(StringTransformerSdv):
    __doc__ = '\n    A :class:`StringTransformerSdv` that is a reference to a symbol\n    '

    def __init__(self, name_of_referenced_sdv: str):
        self._name_of_referenced_sdv = name_of_referenced_sdv
        self._references = [
         SymbolReference(name_of_referenced_sdv, ValueTypeRestriction(ValueType.STRING_TRANSFORMER))]

    def resolve(self, symbols: SymbolTable) -> StringTransformerDdv:
        sdv = lookups.lookup_string_transformer(symbols, self._name_of_referenced_sdv)
        return sdv.resolve(symbols)

    @property
    def references(self) -> Sequence[SymbolReference]:
        return self._references

    def __str__(self):
        return str(type(self)) + "'" + str(self._name_of_referenced_sdv) + "'"