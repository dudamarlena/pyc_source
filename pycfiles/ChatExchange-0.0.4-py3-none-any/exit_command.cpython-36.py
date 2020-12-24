# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\cli\interactive_commands\exit_command.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 649 bytes
__doc__ = '\nModule `chatette_qiu.cli.interactive_commands.exit_command`.\nContains the strategy class that represents the interactive mode command\n`exit` which exits the interactive mode.\n'
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