# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\cli\interactive_commands\exist_command.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 1388 bytes
__doc__ = '\nModule `chatette_qiu.cli.interactive_commands.exist_command`.\nContains the strategy class that represents the interactive mode command\n`exist` which verifies whether a unit is declared or not.\n'
from chatette_qiu.cli.interactive_commands.command_strategy import CommandStrategy

class ExistCommand(CommandStrategy):
    usage_str = 'exist <unit-type> "<unit-name>"'

    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        try:
            unit = facade.parser.get_definition(unit_name, unit_type)
            self.print_wrapper.write(unit.short_desc_str())
            if variation_name is not None:
                if variation_name in unit.variations:
                    self.print_wrapper.write("Variation '" + variation_name + "' is defined for this " + unit.type + '.')
                else:
                    self.print_wrapper.write("Variation '" + variation_name + "' is not defined for this " + unit.type + '.')
        except KeyError:
            self.print_wrapper.write(unit_type.name.capitalize() + " '" + unit_name + "' is not defined.")

        self.print_wrapper.write('')