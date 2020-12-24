# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\mastromatteo\Progetti\flows\flows\Actions\SubstringAction.py
# Compiled at: 2017-03-23 05:01:21
# Size of source mod 2**32: 1636 bytes
"""
SubstringAction.py
------------------

Copyright 2016 Davide Mastromatteo
"""
from flows.Actions.Action import Action

class SubstringAction(Action):
    __doc__ = '\n    SubstringAction Class\n    '
    type = 'substring'
    from_index = 0
    to_index = 0
    separator = ''
    item = 0
    substring_type = 'cut'

    def on_init(self):
        super().on_init()
        if 'from' in self.configuration:
            self.from_index = int(self.configuration['from'])
            if self.from_index < 0:
                self.from_index = 0
        if 'to' in self.configuration:
            self.to_index = int(self.configuration['to'])
        if 'separator' in self.configuration:
            self.separator = self.configuration['separator'].strip()
        if 'item' in self.configuration:
            self.item = int(self.configuration['item']) - 1
        if 'subtype' in self.configuration:
            self.substring_type = self.configuration['subtype']

    def on_input_received(self, action_input=None):
        super().on_input_received(action_input)
        if action_input.sender == self.name:
            return
        return_value = ''
        input_string = action_input.message
        if self.substring_type == 'cut':
            return_value = input_string[self.from_index:self.to_index]
        if self.substring_type == 'split':
            return_value = input_string.split(self.separator)[self.item]
        self.send_message(return_value)