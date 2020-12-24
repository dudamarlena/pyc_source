# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\cli\interactive_commands\add_rule_command.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 2862 bytes
__doc__ = '\nModule `chatette_qiu.cli.interactive_commands.add_rule_command`.\nContains the strategy class that represents the interactive mode command\n`add-rule` which allows to add a rule to a unit definition.\n'
from chatette_qiu.cli.interactive_commands.command_strategy import CommandStrategy

class AddRuleCommand(CommandStrategy):
    usage_str = 'add-rule <unit-type> "<unit-name>" "<rule>"'

    def execute(self, facade):
        if len(self.command_tokens) < 4:
            self.print_wrapper.error_log('Missing some arguments\nUsage: ' + self.usage_str)
            return
        else:
            unit_type = CommandStrategy.get_unit_type_from_str(self.command_tokens[1])
            if unit_type is None:
                self.print_wrapper.error_log("Unknown unit type: '" + str(self.command_tokens[1]) + "'.")
                return
            unit_regex = self.get_regex_name(self.command_tokens[2])
            rule_str = CommandStrategy.remove_quotes(self.command_tokens[3])
            if unit_regex is None:
                try:
                    unit_name, variation_name = CommandStrategy.split_exact_unit_name(self.command_tokens[2])
                except SyntaxError:
                    self.print_wrapper.error_log("Unit identifier couldn't be " + 'interpreted. Did you mean to ' + "escape some hashtags '#'?")
                    return
                else:
                    self._add_rule(facade.parser, unit_type, unit_name, variation_name, rule_str)
            else:
                count = 0
                for unit_name in self.next_matching_unit_name(facade.parser, unit_type, unit_regex):
                    self._add_rule(facade.parser, unit_type, unit_name, None, rule_str)
                    count += 1

                if count == 0:
                    self.print_wrapper.write('No ' + unit_type.name + ' matched.')

    def _add_rule(self, parser, unit_type, unit_name, variation_name, rule_str):
        rule_tokens = parser.tokenizer.tokenize(rule_str)
        rule = parser.tokens_to_sub_rules(rule_tokens)
        unit = parser.get_definition(unit_name, unit_type)
        unit.add_rule(rule, variation_name)
        self.print_wrapper.write('Rule successfully added to ' + unit_type.name + " '" + unit_name + "'.")

    def execute_on_unit(self, facade, unit_type, unit_name):
        raise NotImplementedError()

    def finish_execution(self, facade):
        raise NotImplementedError()