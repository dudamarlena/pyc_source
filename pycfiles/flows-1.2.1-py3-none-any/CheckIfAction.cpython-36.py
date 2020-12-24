# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\mastromatteo\Progetti\flows\flows\Actions\CheckIfAction.py
# Compiled at: 2017-03-23 05:15:16
# Size of source mod 2**32: 2367 bytes
"""
CheckIf.py
----------

Copyright 2016 Davide Mastromatteo
License: Apache-2.0
"""
from flows.Actions.Action import Action

class CheckIf(Action):
    __doc__ = '\n    CheckIf Class\n    output values less than an input parameter\n    '
    type = 'check_if'
    separator = ';'
    output = None

    def on_init(self):
        super().on_init()
        if 'separator' in self.configuration:
            self.separator = self.configuration['separator']
        if 'output' in self.configuration:
            self.output = self.configuration['output']

    def on_input_received(self, action_input=None):
        super().on_input_received(action_input)
        operation = str(self.configuration['operation'])
        value = 0
        limit = 0
        if self.separator in action_input.message:
            input_message = action_input.message
            value = int(input_message.split(self.separator)[0])
            limit = int(input_message.split(self.separator)[1])
        else:
            value = int(action_input.message)
            limit = int(self.configuration['limit'])
        if operation == '<':
            if value < limit:
                self.send_output(str(value))
        if operation == '<=':
            if value <= limit:
                self.send_output(str(value))
        if operation == '>':
            if value > limit:
                self.send_output(str(value))
        if operation == '>=':
            if value >= limit:
                self.send_output(str(value))
        if operation == '==':
            if value == limit:
                self.send_output(str(value))
        if operation == '!=':
            if value != limit:
                self.send_output(str(value))
        if operation == '%':
            if value % limit == 0:
                self.send_output(str(value))

    def send_output(self, value):
        if self.output:
            string_to_log = self.output.replace('{value}', value)
            self.send_message(string_to_log)
        else:
            self.send_message(value)