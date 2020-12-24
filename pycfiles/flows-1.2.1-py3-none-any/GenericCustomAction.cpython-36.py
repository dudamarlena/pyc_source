# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\mastromatteo\Progetti\flows\flows\Actions\GenericCustomAction.py
# Compiled at: 2017-03-23 05:01:21
# Size of source mod 2**32: 1070 bytes
"""
GenericCustomAction.py
----------------------

Copyright 2016 Davide Mastromatteo
License: Apache-2.0
"""
from flows.Actions.Action import Action

class GenericCustomAction(Action):
    __doc__ = '\n    GenericCustomAction Class\n    '
    type = 'generic'

    def on_init(self):
        super().on_init()

    def on_stop(self):
        return super().on_stop()

    def on_cycle(self):
        super().on_cycle()

    def on_input_received(self, action_input=None):
        super().on_input_received(action_input)
        to_return = action_input.message[::-1]
        self.send_message(to_return)