# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\cli\interactive_commands\generate_command.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 4676 bytes
__doc__ = '\nModule `chatette_qiu.cli.interactive_commands.generate_command`.\nContains the strategy class that represents the interactive mode command\n`generate` which generates units and writes them out formatted using a\ngiven adapter.\n'
from chatette_qiu.cli.interactive_commands.command_strategy import CommandStrategy
from chatette_qiu.adapters.factory import create_adapter

class GenerateCommand(CommandStrategy):
    usage_str = 'generate <adapter> <unit-type> "<unit-name>"'

    def __init__(self, command_str, quiet=False):
        super(GenerateCommand, self).__init__(command_str, quiet)
        self.nb_examples = None

    def execute(self, facade):
        """
        Implements the command `generate` which generates all possible examples
        of a certain unit, formatted according to a certain adapter.
        """
        if len(self.command_tokens) == 1:
            facade.run_generation()
            return
        elif len(self.command_tokens) == 2:
            try:
                facade.run_generation(self.command_tokens[1])
            except ValueError:
                self.print_wrapper.write("Unknown adapter: '" + self.command_tokens[1] + "'")

            return
        else:
            if len(self.command_tokens) < 4:
                self.print_wrapper.error_log('Missing some arguments\nUsage: ' + self.usage_str)
                return
            else:
                adapter_str = self.command_tokens[1]
                try:
                    adapter = create_adapter(adapter_str)
                except ValueError:
                    self.print_wrapper.error_log("Unknown adapter '" + adapter_str + "'.")

                if len(self.command_tokens) == 5:
                    try:
                        self.nb_examples = int(self.command_tokens[(-1)])
                    except ValueError:
                        self.print_wrapper.error_log('The number of examples to be ' + 'generated is invalid: it must ' + 'be an integer (no other ' + 'characters allowed).')
                        return

                unit_type = CommandStrategy.get_unit_type_from_str(self.command_tokens[2])
                if unit_type is None:
                    self.print_wrapper.error_log("Unknown unit type: '" + str(self.command_tokens[2]) + "'.")
                    return
            unit_regex = self.get_regex_name(self.command_tokens[3])
            if unit_regex is None:
                try:
                    unit_name, variation_name = CommandStrategy.split_exact_unit_name(self.command_tokens[3])
                except SyntaxError:
                    self.print_wrapper.error_log("Unit identifier couldn't be " + 'interpreted. Did you mean to ' + "escape some hashtags '#'?")
                    return
                else:
                    self._generate_unit(facade, adapter, unit_type, unit_name, variation_name)
            else:
                count = 0
                for unit_name in self.next_matching_unit_name(facade.parser, unit_type, unit_regex):
                    self._generate_unit(facade, adapter, unit_type, unit_name)
                    count += 1

                if count == 0:
                    self.print_wrapper.write('No ' + unit_type.name + ' matched.')
        self.finish_execution(facade)

    def _generate_unit(self, facade, adapter, unit_type, unit_name, variation_name=None):
        definition = facade.parser.get_definition(unit_name, unit_type)
        examples = definition.generate_nb_examples(self.nb_examples, variation_name)
        self.print_wrapper.write('Generated examples for ' + unit_type.name + " '" + unit_name + "':'")
        for ex in examples:
            if not hasattr(ex, 'name'):
                ex.name = 'INTERACTIVE'
            self.print_wrapper.write(adapter.prepare_example(ex))

        self.print_wrapper.write('')

    def finish_execution(self, facade):
        self.nb_examples = None

    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        raise NotImplementedError()