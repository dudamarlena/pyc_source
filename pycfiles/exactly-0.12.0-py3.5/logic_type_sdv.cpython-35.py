# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/logic/logic_type_sdv.py
# Compiled at: 2019-12-27 10:07:50
# Size of source mod 2**32: 1400 bytes
from abc import ABC, abstractmethod
from typing import Sequence, Generic
from exactly_lib.symbol.logic.matcher import MODEL
from exactly_lib.symbol.sdv_structure import SymbolDependentValue
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.type_system.description.tree_structured import WithTreeStructureDescription
from exactly_lib.type_system.logic.matcher_base_class import MatcherDdv
from exactly_lib.type_system.value_type import TypeCategory, LogicValueType
from exactly_lib.util.symbol_table import SymbolTable

class LogicTypeSdv(SymbolDependentValue, ABC):
    __doc__ = ' Base class for logic values - values that represent functionality/logic.'

    @property
    def type_category(self) -> TypeCategory:
        return TypeCategory.LOGIC

    @property
    def logic_value_type(self) -> LogicValueType:
        raise NotImplementedError('abstract method')

    @property
    def references(self) -> Sequence[SymbolReference]:
        raise NotImplementedError('abstract method')

    def resolve(self, symbols: SymbolTable) -> WithTreeStructureDescription:
        raise NotImplementedError('abstract method')


def get_logic_value_type(sdv: LogicTypeSdv) -> LogicValueType:
    return sdv.logic_value_type


class MatcherTypeSdv(Generic[MODEL], LogicTypeSdv, ABC):

    @abstractmethod
    def resolve(self, symbols: SymbolTable) -> MatcherDdv[MODEL]:
        pass