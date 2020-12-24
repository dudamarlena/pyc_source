# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/program/command/driver_sdvs.py
# Compiled at: 2019-12-27 10:07:44
# Size of source mod 2**32: 1887 bytes
from typing import Sequence
from exactly_lib.symbol.data.path_sdv import PathSdv
from exactly_lib.symbol.data.string_sdv import StringSdv
from exactly_lib.symbol.logic.program.command_sdv import CommandDriverSdv
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.type_system.logic.program import commands
from exactly_lib.type_system.logic.program.command import CommandDriverDdv
from exactly_lib.util.symbol_table import SymbolTable

class CommandDriverSdvForExecutableFile(CommandDriverSdv):

    def __init__(self, executable_file: PathSdv):
        self._executable_file = executable_file

    @property
    def references(self) -> Sequence[SymbolReference]:
        return self._executable_file.references

    @property
    def executable_file(self) -> PathSdv:
        return self._executable_file

    def resolve(self, symbols: SymbolTable) -> CommandDriverDdv:
        return commands.CommandDriverDdvForExecutableFile(self._executable_file.resolve(symbols))


class CommandDriverSdvForSystemProgram(CommandDriverSdv):

    def __init__(self, program: StringSdv):
        self._program = program

    @property
    def references(self) -> Sequence[SymbolReference]:
        return self._program.references

    @property
    def program(self) -> StringSdv:
        return self._program

    def resolve(self, symbols: SymbolTable) -> CommandDriverDdv:
        return commands.CommandDriverDdvForSystemProgram(self._program.resolve(symbols))


class CommandDriverSdvForShell(CommandDriverSdv):

    def __init__(self, command_line: StringSdv):
        self._command_line = command_line

    @property
    def references(self) -> Sequence[SymbolReference]:
        return self._command_line.references

    def resolve(self, symbols: SymbolTable) -> CommandDriverDdv:
        return commands.CommandDriverDdvForShell(self._command_line.resolve(symbols))