# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/sdv_structure.py
# Compiled at: 2019-12-27 10:07:41
# Size of source mod 2**32: 2410 bytes
from typing import Sequence, Optional
from exactly_lib.section_document.source_location import SourceLocationInfo
from exactly_lib.symbol.object_with_symbol_references import ObjectWithSymbolReferences
from exactly_lib.type_system.value_type import ValueType, TypeCategory
from exactly_lib.util.line_source import LineSequence
from exactly_lib.util.symbol_table import SymbolTableValue, SymbolTable

class SymbolDependentValue(ObjectWithSymbolReferences):
    __doc__ = ' Base class for values in the symbol table used by Exactly. '

    @property
    def type_category(self) -> TypeCategory:
        raise NotImplementedError('abstract method')

    @property
    def value_type(self) -> ValueType:
        raise NotImplementedError('abstract method')

    @property
    def references(self) -> Sequence:
        """
        All :class:`SymbolReference` directly referenced by this object.

        :type: [`SymbolReference`]
        """
        raise NotImplementedError('abstract method')

    def resolve(self, symbols: SymbolTable):
        raise NotImplementedError('abstract method')


def get_references(sdv: SymbolDependentValue) -> Sequence:
    return sdv.references


def get_type_category(sdv: SymbolDependentValue) -> TypeCategory:
    return sdv.type_category


def get_value_type(sdv: SymbolDependentValue) -> ValueType:
    return sdv.value_type


class SymbolContainer(SymbolTableValue):
    __doc__ = '\n    The info about a Symbol Dependent Value that is stored in a symbol table.\n\n    A value together with meta info\n    '

    def __init__(self, value_sdv: SymbolDependentValue, source_location: Optional[SourceLocationInfo]):
        self._sdv = value_sdv
        self._source_location = source_location

    @property
    def source_location(self) -> Optional[SourceLocationInfo]:
        return self._source_location

    @property
    def definition_source(self) -> LineSequence:
        """
        The source code of the definition of the value.

        :rtype None iff the symbol is built in.
        """
        if self._source_location is None:
            return
        return self._source_location.source_location_path.location.source

    @property
    def sdv(self) -> SymbolDependentValue:
        return self._sdv


def container_of_builtin(value_sdv: SymbolDependentValue) -> SymbolContainer:
    return SymbolContainer(value_sdv, None)