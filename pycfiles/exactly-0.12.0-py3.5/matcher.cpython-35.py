# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/logic/matcher.py
# Compiled at: 2019-12-27 10:07:42
# Size of source mod 2**32: 670 bytes
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Sequence
from exactly_lib.symbol.object_with_typed_symbol_references import ObjectWithTypedSymbolReferences
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.type_system.logic.matcher_base_class import MatcherDdv
from exactly_lib.util.symbol_table import SymbolTable
MODEL = TypeVar('MODEL')

class MatcherSdv(Generic[MODEL], ObjectWithTypedSymbolReferences, ABC):

    @property
    @abstractmethod
    def references(self) -> Sequence[SymbolReference]:
        pass

    @abstractmethod
    def resolve(self, symbols: SymbolTable) -> MatcherDdv[MODEL]:
        pass