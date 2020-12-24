# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\cli\interactive_commands\delete_command.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 1286 bytes
__doc__ = '\nModule `chatette_qiu.cli.interactive_commands.delete_command`.\nContains the strategy class that represents the interactive mode command\n`delete` which deletes a unit declaration from the parser.\n'
from chatette_qiu.cli.interactive_commands.command_strategy import CommandStrategy

class DeleteCommand(CommandStrategy):
    usage_str = 'delete <unit-type> "<unit-name>"'

    def __init__(self, command_str, quiet=False):
        super(DeleteCommand, self).__init__(command_str, quiet)
        self._units_to_delete = []

    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        self._units_to_delete.append((unit_type, unit_name, variation_name))
        self.print_wrapper.write(unit_type.name.capitalize() + " '" + unit_name + "' was successfully deleted.")

    def finish_execution(self, facade):
        for unit_type, unit_name, variation_name in self._units_to_delete:
            try:
                facade.parser.delete(unit_type, unit_name, variation_name)
            except KeyError:
                self.print_wrapper.write(unit_type.name.capitalize() + " '" + unit_name + "' was not defined.")

        self._units_to_delete = []