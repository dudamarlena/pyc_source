# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\cli\interactive_commands\save_command.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 1775 bytes
__doc__ = '\nModule `chatette_qiu.cli.interactive_command.save_command`.\nContains the strategy class that represents the interactive mode command\n`save` which writes a template file that, when parsed, would make a parser\nthat is in the state of the current parser.\n'
from __future__ import print_function
import io
from chatette_qiu.cli.interactive_commands.command_strategy import CommandStrategy

class SaveCommand(CommandStrategy):
    usage_str = 'save <template-file-path>'

    def execute(self, facade):
        if len(self.command_tokens) < 2:
            self.print_wrapper.error_log('Missing some arguments\nUsage: ' + self.usage_str)
            return
        template_filepath = self.command_tokens[1]
        parser = facade.parser
        with io.open(template_filepath, 'w+') as (f):
            for intent_name in parser.intent_definitions:
                intent = parser.intent_definitions[intent_name]
                print((intent.get_template_description()), file=f)

            print(file=f)
            for alias_name in parser.alias_definitions:
                alias = parser.alias_definitions[alias_name]
                print((alias.get_template_description()), file=f)

            print(file=f)
            for slot_name in parser.slot_definitions:
                slot = parser.slot_definitions[slot_name]
                print((slot.get_template_description()), file=f)

        self.print_wrapper.write('Template file successfully written.')

    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        raise NotImplementedError()

    def finish_execution(self, facade):
        raise NotImplementedError()