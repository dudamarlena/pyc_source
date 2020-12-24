# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/program/executable_file.py
# Compiled at: 2019-12-27 10:07:41
# Size of source mod 2**32: 838 bytes
from exactly_lib.symbol.data.list_sdv import ListSdv
from exactly_lib.symbol.data.path_sdv import PathSdv
from exactly_lib.symbol.logic.program.command_sdv import CommandSdv
from exactly_lib.test_case_utils.program.command import command_sdvs

class ExecutableFileWithArgsResolver:

    def __init__(self, executable_file: PathSdv, arguments: ListSdv):
        self._executable_file = executable_file
        self._arguments = arguments

    @property
    def executable_file(self) -> PathSdv:
        return self._executable_file

    @property
    def arguments(self) -> ListSdv:
        return self._arguments

    @property
    def as_command(self) -> CommandSdv:
        return command_sdvs.for_executable_file(self.executable_file).new_with_additional_argument_list(self._arguments)