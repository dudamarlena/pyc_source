# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/logic/resolving_environment.py
# Compiled at: 2019-12-27 10:07:46
# Size of source mod 2**32: 836 bytes
from exactly_lib.test_case_file_structure.tcds import Tcds
from exactly_lib.type_system.logic.logic_base_class import ApplicationEnvironment
from exactly_lib.util.symbol_table import SymbolTable

class FullResolvingEnvironment(tuple):
    __doc__ = '\n    Everything needed to resolve the applicator of a logic type,\n    from a parsed object.\n    '

    def __new__(cls, symbols: SymbolTable, tcds: Tcds, application_environment: ApplicationEnvironment):
        return tuple.__new__(cls, (symbols, tcds, application_environment))

    @property
    def symbols(self) -> SymbolTable:
        return self[0]

    @property
    def tcds(self) -> Tcds:
        return self[1]

    @property
    def application_environment(self) -> ApplicationEnvironment:
        return self[2]