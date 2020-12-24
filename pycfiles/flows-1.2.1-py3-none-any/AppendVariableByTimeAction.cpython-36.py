# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\mastromatteo\Progetti\flows\flows\Actions\AppendVariableByTimeAction.py
# Compiled at: 2017-03-23 05:15:29
# Size of source mod 2**32: 1351 bytes
"""
AppendVariableByTime.py
-----------------------

Copyright 2016 Davide Mastromatteo
License: Apache-2.0
"""
import datetime, collections
from flows.Actions.Action import Action

class AppendVariableByTime(Action):
    __doc__ = '\n    AppendVariableByTime Class\n    returns the input received plus a column and a variable based upon the time of the day\n    '
    type = 'append_variable_by_time'
    separator = ';'
    time_config = ''

    def on_init(self):
        super().on_init()
        if 'separator' in self.configuration:
            self.separator = self.configuration['separator']
        self.time_config = collections.OrderedDict(sorted(self.configuration.items()))

    def on_input_received(self, action_input=None):
        super().on_input_received(action_input)
        now = datetime.datetime.now().time()
        for config in self.time_config:
            if ':' in config:
                limit = datetime.datetime.strptime(config, '%H:%M').time()
                if now >= limit:
                    variable = self.configuration[config]

        msg = str.format('{0}{1}{2}', action_input.message, self.separator, variable)
        self.send_message(msg)