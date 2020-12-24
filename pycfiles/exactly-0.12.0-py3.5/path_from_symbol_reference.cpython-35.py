# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/parse/path_from_symbol_reference.py
# Compiled at: 2019-12-27 10:07:41
# Size of source mod 2**32: 3501 bytes
import pathlib
from typing import Sequence
from exactly_lib.symbol.data.data_type_sdv import DataTypeSdv
from exactly_lib.symbol.data.list_sdv import ListSdv
from exactly_lib.symbol.data.path_sdv import PathSdv, PathPartSdv
from exactly_lib.symbol.data.string_sdv import StringSdv
from exactly_lib.symbol.data.visitor import DataTypeSdvPseudoVisitor
from exactly_lib.symbol.sdv_structure import SymbolContainer
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.test_case_file_structure.path_relativity import RelOptionType
from exactly_lib.type_system.data import paths
from exactly_lib.type_system.data.path_ddv import PathDdv
from exactly_lib.util.symbol_table import SymbolTable

class _SdvThatIsIdenticalToReferencedPathOrWithStringValueAsSuffix(PathSdv):
    __doc__ = '\n    A file-ref from a symbol reference, that can be either a string or a file-ref\n    '

    def __init__(self, path_or_string_symbol: SymbolReference, suffix_sdv: PathPartSdv, default_relativity: RelOptionType):
        self._path_or_string_symbol = path_or_string_symbol
        self._suffix_sdv = suffix_sdv
        self.default_relativity = default_relativity

    def resolve(self, symbols: SymbolTable) -> PathDdv:
        symbol_value_2_path = _DataValueSymbol2PathResolverVisitor(self._suffix_sdv, self.default_relativity, symbols)
        container = symbols.lookup(self._path_or_string_symbol.name)
        assert isinstance(container, SymbolContainer), 'Implementation consistency/SymbolContainer'
        sdv = container.sdv
        assert isinstance(sdv, DataTypeSdv), 'Implementation consistency/DataTypeSdv'
        return symbol_value_2_path.visit(sdv)

    @property
    def references(self) -> Sequence[SymbolReference]:
        return [self._path_or_string_symbol] + self._suffix_sdv.references


class _DataValueSymbol2PathResolverVisitor(DataTypeSdvPseudoVisitor):

    def __init__(self, suffix_sdv: PathPartSdv, default_relativity: RelOptionType, symbols: SymbolTable):
        self.suffix_sdv = suffix_sdv
        self.symbols = symbols
        self.default_relativity = default_relativity

    def visit_path(self, value: PathSdv) -> PathDdv:
        path = value.resolve(self.symbols)
        suffix_str = self.suffix_sdv.resolve(self.symbols).value()
        if not suffix_str:
            return path
        suffix_str = suffix_str.lstrip('/')
        return paths.stacked(path, paths.constant_path_part(suffix_str))

    def visit_string(self, value: StringSdv) -> PathDdv:
        sv = value.resolve(self.symbols)
        first_suffix_str = sv.value_when_no_dir_dependencies()
        following_suffix_str = self.suffix_sdv.resolve(self.symbols).value()
        path_str = first_suffix_str + following_suffix_str
        path_ddv = pathlib.Path(path_str)
        if path_ddv.is_absolute():
            return paths.absolute_file_name(path_str)
        else:
            return paths.of_rel_option(self.default_relativity, paths.constant_path_part(path_str))

    def visit_list(self, value: ListSdv) -> PathDdv:
        raise ValueError('Impossible to convert a list to a path')