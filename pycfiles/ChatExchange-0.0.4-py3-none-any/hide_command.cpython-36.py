# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\cli\interactive_commands\hide_command.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 2962 bytes
__doc__ = '\nModule `chatette_qiu.cli.interactive_commands.hide_command`.\nContains the strategy class that represents the interactive mode command\n`hide` which hides unit definitions (storing them somewhere to be able to\nunhide them later).\n'
from chatette_qiu.cli.interactive_commands.command_strategy import CommandStrategy

class HideCommand(CommandStrategy):
    usage_str = 'hide <unit-type> "<unit-name>"'
    stored_units = {'alias':dict(),  'slot':dict(),  'intent':dict()}
    stored_variations = {'alias':dict(),  'slot':dict(),  'intent':dict()}

    def __init__(self, command_str, quiet=False):
        super(HideCommand, self).__init__(command_str, quiet)
        self._units_to_delete = []
        self._var_to_delete = []

    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        try:
            unit = facade.parser.get_definition(unit_name, unit_type)
            if variation_name is None:
                self.stored_units[unit_type.name][unit_name] = unit
                self._units_to_delete.append((unit_type, unit_name))
                self.print_wrapper.write(unit_type.name.capitalize() + " '" + unit_name + "' was successfully hidden.")
            else:
                if variation_name not in unit.variations:
                    self.print_wrapper.error_log("Couldn't find variation '" + variation_name + "' in " + unit_type.name + " '" + unit_name + "'.")
                    return
                else:
                    self._var_to_delete.append((unit_type, unit_name, variation_name))
                    rules = unit.variations[variation_name]
                    if unit_name not in self.stored_variations[unit_type.name]:
                        self.stored_variations[unit_type.name][unit_name] = {variation_name: rules}
                    else:
                        self.stored_variations[unit_type.name][unit_name][variation_name] = rules
                self.print_wrapper.write("Variation '" + variation_name + "' of " + unit_type.name + " '" + unit_name + "' was successfully hidden.")
        except KeyError:
            self.print_wrapper.write(unit_type.name.capitalize() + " '" + unit_name + "' was not defined.")

    def finish_execution(self, facade):
        for unit_type, unit_name in self._units_to_delete:
            facade.parser.delete(unit_type, unit_name)

        self._units_to_delete = []
        for unit_type, unit_name, variation_name in self._var_to_delete:
            facade.parser.delete(unit_type, unit_name, variation_name)

        self._var_to_delete = []