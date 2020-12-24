# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\cli\interactive_commands\rename_command.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 2457 bytes
__doc__ = '\nModule `chatette_qiu.cli.interactive_commands.rename_command`.\nContains the strategy class that represents the interactive mode command\n`rename` which changes the name of a unit (if it exists).\n'
from chatette_qiu.cli.interactive_commands.command_strategy import CommandStrategy

class RenameCommand(CommandStrategy):

    def execute(self, facade):
        """
        Implements the command `rename` which renames a unit
        into something else. Displays an error if the unit wasn't found.
        """
        if len(self.command_tokens) < 4:
            self.print_wrapper.error_log('Missing some arguments\nUsage: ' + 'rename <unit-type> "<old-name>" ' + '"<new-name>"')
            return
        else:
            unit_type = CommandStrategy.get_unit_type_from_str(self.command_tokens[1])
            if unit_type is None:
                self.print_wrapper.error_log("Unknown unit type: '" + str(self.command_tokens[1]) + "'.")
            else:
                old_name = CommandStrategy.remove_quotes(self.command_tokens[2])
                new_name = CommandStrategy.remove_quotes(self.command_tokens[3])
                if new_name == '':
                    self.print_wrapper.error_log('An empty name is not a valid ' + unit_type.name + ' name.')
                    return
                try:
                    facade.parser.rename_unit(unit_type, old_name, new_name)
                    self.print_wrapper.write(unit_type.name.capitalize() + " '" + old_name + "' was successfully " + "renamed to '" + new_name + "'.")
                except KeyError:
                    self.print_wrapper.error_log("Couldn't find a unit named '" + str(old_name) + "'.")
                except ValueError:
                    self.print_wrapper.error_log(unit_type.name.capitalize() + " '" + new_name + "' is already " + 'in use.')

    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        raise NotImplementedError()

    def finish_execution(self, facade):
        raise NotImplementedError()