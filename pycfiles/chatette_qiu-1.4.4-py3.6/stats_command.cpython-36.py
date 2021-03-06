# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\cli\interactive_commands\stats_command.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 804 bytes
"""
Module `chatette_qiu.cli.interactive_commands.stats_command`.
Contains the strategy class that represents the interactive mode command
`stats` which shows statistics about the parsing.
"""
from chatette_qiu.cli.interactive_commands.command_strategy import CommandStrategy

class StatsCommand(CommandStrategy):

    def execute(self, facade):
        """Implements the command `stats`, printing parsing statistics."""
        self.print_wrapper.write('Statistics:')
        stats = facade.get_stats_as_str()
        self.print_wrapper.write(stats)

    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        raise NotImplementedError()

    def finish_execution(self, facade):
        raise NotImplementedError()