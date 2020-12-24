# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/logic/program/command_sdv.py
# Compiled at: 2019-12-27 10:07:48
# Size of source mod 2**32: 2703 bytes
from typing import Sequence
from exactly_lib.symbol.data.list_sdv import ListSdv
from exactly_lib.symbol.logic.program.arguments_sdv import ArgumentsSdv
from exactly_lib.symbol.object_with_symbol_references import references_from_objects_with_symbol_references
from exactly_lib.symbol.path_resolving_environment import PathResolvingEnvironmentPreOrPostSds
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.symbol.utils import DirDepValueResolver
from exactly_lib.test_case_utils.program.command import arguments_sdvs
from exactly_lib.type_system.logic.program.command import CommandDdv, CommandDriverDdv
from exactly_lib.type_system.logic.program.process_execution.command import Command
from exactly_lib.util.symbol_table import SymbolTable

class CommandDriverSdv(DirDepValueResolver[CommandDriverDdv]):

    def resolve(self, symbols: SymbolTable) -> CommandDriverDdv:
        raise NotImplementedError('abstract method')

    @property
    def references(self) -> Sequence[SymbolReference]:
        raise NotImplementedError('abstract method')


class CommandSdv(DirDepValueResolver[CommandDdv]):
    __doc__ = '\n    This class works a bit like a immutable builder of Command - new arguments\n    may be appended to form a new object representing a different command.\n\n    This is the way more complex commands are built from simpler ones.\n    '

    def __init__(self, command_driver: CommandDriverSdv, arguments: ArgumentsSdv):
        self._driver = command_driver
        self._arguments = arguments

    def new_with_additional_arguments(self, additional_arguments: ArgumentsSdv) -> 'CommandSdv':
        """
        Creates a new SDV with additional arguments appended at the end of
        current argument list.
        """
        return CommandSdv(self._driver, self._arguments.new_accumulated(additional_arguments))

    def new_with_additional_argument_list(self, additional_arguments: ListSdv) -> 'CommandSdv':
        return self.new_with_additional_arguments(arguments_sdvs.new_without_validation(additional_arguments))

    def resolve(self, symbols: SymbolTable) -> CommandDdv:
        return CommandDdv(self._driver.resolve(symbols), self._arguments.resolve(symbols))

    def resolve_of_any_dep(self, environment: PathResolvingEnvironmentPreOrPostSds) -> Command:
        return self.resolve(environment.symbols).value_of_any_dependency(environment.tcds)

    @property
    def references(self) -> Sequence[SymbolReference]:
        return references_from_objects_with_symbol_references([
         self._driver,
         self._arguments])