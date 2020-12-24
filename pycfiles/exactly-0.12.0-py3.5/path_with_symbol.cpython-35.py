# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/data/path_sdv_impls/path_with_symbol.py
# Compiled at: 2019-12-27 10:07:41
# Size of source mod 2**32: 1001 bytes
from typing import Sequence
from exactly_lib.symbol import lookups
from exactly_lib.symbol.data.path_sdv import PathSdv, PathPartSdv
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.type_system.data import paths
from exactly_lib.type_system.data.path_ddv import PathDdv
from exactly_lib.util.symbol_table import SymbolTable

class PathSdvRelSymbol(PathSdv):

    def __init__(self, path_suffix: PathPartSdv, symbol_reference_of_path: SymbolReference):
        self.path_suffix = path_suffix
        self.symbol_reference_of_path = symbol_reference_of_path

    def resolve(self, symbols: SymbolTable) -> PathDdv:
        base_path = lookups.lookup_and_resolve_path(symbols, self.symbol_reference_of_path.name)
        return paths.stacked(base_path, self.path_suffix.resolve(symbols))

    @property
    def references(self) -> Sequence[SymbolReference]:
        return [self.symbol_reference_of_path] + list(self.path_suffix.references)