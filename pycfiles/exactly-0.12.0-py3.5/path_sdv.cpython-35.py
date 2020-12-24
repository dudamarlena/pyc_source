# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/data/path_sdv.py
# Compiled at: 2019-12-27 10:07:41
# Size of source mod 2**32: 1417 bytes
from typing import Sequence
from exactly_lib.symbol.data.data_type_sdv import DataTypeSdv
from exactly_lib.symbol.object_with_symbol_references import ObjectWithSymbolReferences
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.type_system.data.path_ddv import PathDdv
from exactly_lib.type_system.data.path_part import PathPartDdv
from exactly_lib.type_system.value_type import DataValueType, ValueType
from exactly_lib.util.symbol_table import SymbolTable

class PathSdv(DataTypeSdv):
    __doc__ = "\n    Resolver who's resolved value is of type `ValueType.PATH` / :class:`PathDdv`\n    "

    @property
    def data_value_type(self) -> DataValueType:
        return DataValueType.PATH

    @property
    def value_type(self) -> ValueType:
        return ValueType.PATH

    def resolve(self, symbols: SymbolTable) -> PathDdv:
        raise NotImplementedError('abstract method')

    @property
    def references(self) -> Sequence[SymbolReference]:
        raise NotImplementedError('abstract method')

    def __str__(self):
        return str(type(self))


class PathPartSdv(ObjectWithSymbolReferences):
    __doc__ = '\n    The relative path that follows the root path of the `PathDdv`.\n    '

    def resolve(self, symbols: SymbolTable) -> PathPartDdv:
        raise NotImplementedError()

    @property
    def references(self) -> Sequence[SymbolReference]:
        raise NotImplementedError()