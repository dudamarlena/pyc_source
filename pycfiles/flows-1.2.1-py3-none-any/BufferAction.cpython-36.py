# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\mastromatteo\Progetti\flows\flows\Actions\BufferAction.py
# Compiled at: 2017-03-23 05:15:25
# Size of source mod 2**32: 1369 bytes
"""
BufferAction.py
----------------------------

Copyright 2016 Davide Mastromatteo
"""
import re
from flows.Actions.Action import Action

class BufferAction(Action):
    __doc__ = '\n    BufferAction Class\n    '
    type = 'buffer'
    buffer = None
    regex = ''

    def on_init(self):
        super().on_init()
        if 'regex_new_buffer' not in self.configuration:
            raise ValueError(str.format('The buffer action {0} is not properly configured.The regex_new_buffer parameter is missing', self.name))
        self.buffer = []
        self.regex = self.configuration['regex_new_buffer']

    def on_input_received(self, action_input=None):
        super().on_input_received(action_input)
        match = re.search(self.regex, action_input.message)
        if match is None:
            self.buffer.append(action_input.message)
            return (None, '*')
        else:
            if len(self.buffer) > 0:
                return_value = ''.join(self.buffer)
                self.buffer.clear()
                self.buffer.append(action_input.message)
                self.send_message(return_value)
            else:
                self.buffer.append(action_input.message)