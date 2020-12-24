# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\cli\interactive_commands\show_command.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 1866 bytes
__doc__ = '\nModule `chatette_qiu.cli.interactive_commands.show_command`.\nContains the strategy class that represents the interactive mode command\n`show` which shows information about a unit definition and lists a bunch of\nits rules (all if possible).\n'
from chatette_qiu.cli.interactive_commands.command_strategy import CommandStrategy

class ShowCommand(CommandStrategy):
    usage_str = 'show <unit-type> "<unit-name>"'
    max_nb_rules_to_display = 12

    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        try:
            unit = facade.parser.get_definition(unit_name, unit_type)
            self.print_wrapper.write(unit.short_desc_str())
            if variation_name is None:
                rules = unit.rules
                self.print_wrapper.write('Rules:')
            else:
                if variation_name not in unit.variations:
                    self.print_wrapper.error_log("Variation '" + variation_name + "' is not defined in " + unit.type + ' ' + unit_name + '.')
                    return
                rules = unit.variations[variation_name]
                self.print_wrapper.write("Rules for variation '" + variation_name + "':")
            for i, rule in enumerate(rules):
                if i >= self.max_nb_rules_to_display:
                    break
                rule_str = ''.join([sub_rule.as_string() for sub_rule in rule])
                self.print_wrapper.write('\t' + rule_str)

            self.print_wrapper.write('')
        except KeyError:
            self.print_wrapper.write(unit_type.name.capitalize() + " '" + unit_name + "' is not defined.")