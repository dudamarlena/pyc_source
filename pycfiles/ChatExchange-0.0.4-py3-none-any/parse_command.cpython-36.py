# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\cli\interactive_commands\parse_command.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 1006 bytes
__doc__ = '\nModule `chatette_qiu.cli.interactive_commands.parse_command`.\nContains the strategy class that represents the interactive mode command\n`parse` which parses a new template file.\n'
from chatette_qiu.cli.interactive_commands.command_strategy import CommandStrategy

class ParseCommand(CommandStrategy):

    def execute(self, facade):
        """
        Implements the command `parse`,
        parsing a new template file using the current parser.
        """
        if len(self.command_tokens) <= 1:
            self.print_wrapper.error_log('Missing template file path\nUsage: ' + "'parse <filepath>'")
            return
        filepath = self.command_tokens[1]
        facade.parse_file(filepath)

    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        raise NotImplementedError()

    def finish_execution(self, facade):
        raise NotImplementedError()