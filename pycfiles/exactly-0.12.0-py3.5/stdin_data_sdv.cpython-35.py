# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/logic/program/stdin_data_sdv.py
# Compiled at: 2019-12-27 10:07:44
# Size of source mod 2**32: 1255 bytes
from typing import Sequence
from exactly_lib.symbol.data.string_or_path import StringOrPathSdv
from exactly_lib.symbol.object_with_symbol_references import references_from_objects_with_symbol_references
from exactly_lib.symbol.object_with_typed_symbol_references import ObjectWithTypedSymbolReferences
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.type_system.logic.program.stdin_data import StdinDataDdv
from exactly_lib.util.symbol_table import SymbolTable

class StdinDataSdv(ObjectWithTypedSymbolReferences):

    def __init__(self, fragments: Sequence[StringOrPathSdv]):
        self._fragments = fragments

    def new_accumulated(self, stdin_data_sdv: 'StdinDataSdv') -> 'StdinDataSdv':
        assert isinstance(stdin_data_sdv, StdinDataSdv)
        fragments = tuple(self._fragments) + tuple(stdin_data_sdv._fragments)
        return StdinDataSdv(fragments)

    @property
    def references(self) -> Sequence[SymbolReference]:
        return references_from_objects_with_symbol_references(self._fragments)

    def resolve_value(self, symbols: SymbolTable) -> StdinDataDdv:
        return StdinDataDdv([f.resolve(symbols) for f in self._fragments])


def no_stdin() -> StdinDataSdv:
    return StdinDataSdv(())