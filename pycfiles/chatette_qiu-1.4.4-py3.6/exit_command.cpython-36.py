# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\cli\interactive_commands\exit_command.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 649 bytes
"""
Module `chatette_qiu.cli.interactive_commands.exit_command`.
Contains the strategy class that represents the interactive mode command
`exit` which exits the interactive mode.
"""
from chatette_qiu.cli.interactive_commands.command_strategy import CommandStrategy

class ExitCommand(CommandStrategy):

    def execute(self, facade):
        pass

    def should_exit(self):
        return True

    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        raise NotImplementedError()

    def finish_execution(self, facade):
        raise NotImplementedError()