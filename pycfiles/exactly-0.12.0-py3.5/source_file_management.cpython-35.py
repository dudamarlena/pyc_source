# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/actors/source_interpreter/source_file_management.py
# Compiled at: 2019-12-27 10:07:48
# Size of source mod 2**32: 1849 bytes
from exactly_lib.type_system.logic.program.process_execution.command import ProgramAndArguments

class SourceFileManager:
    __doc__ = '\n    Manages generation of a file-name and execution of an existing file.\n    '

    def base_name_from_stem(self, stem: str) -> str:
        raise NotImplementedError()

    def command_and_args_for_executing_script_file(self, script_file_name: str) -> ProgramAndArguments:
        """
        :returns The list of the command and it's arguments for executing the given
        script file (that is a program in the language defined by this object).
        """
        raise NotImplementedError()


class SourceInterpreterSetup:

    def __init__(self, file_manager: SourceFileManager):
        self._SourceInterpreterSetup__file_manager = file_manager

    def base_name_from_stem(self, stem: str) -> str:
        return self._SourceInterpreterSetup__file_manager.base_name_from_stem(stem)

    def command_and_args_for_executing_script_file(self, file_name: str) -> ProgramAndArguments:
        return self._SourceInterpreterSetup__file_manager.command_and_args_for_executing_script_file(file_name)


class StandardSourceFileManager(SourceFileManager):

    def __init__(self, extension_after_dot: str, interpreter: str, command_line_options_before_file_argument: list):
        self.extension_after_dot = extension_after_dot
        self.interpreter = interpreter
        self.command_line_options_before_file_argument = command_line_options_before_file_argument

    def base_name_from_stem(self, stem: str) -> str:
        return stem + '.' + self.extension_after_dot

    def command_and_args_for_executing_script_file(self, script_file_name: str) -> ProgramAndArguments:
        return ProgramAndArguments(self.interpreter, self.command_line_options_before_file_argument + [script_file_name])