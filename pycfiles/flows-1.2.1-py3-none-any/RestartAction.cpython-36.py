# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\mastromatteo\Progetti\flows\flows\Actions\RestartAction.py
# Compiled at: 2017-03-23 05:01:21
# Size of source mod 2**32: 474 bytes
"""
RestartAction.py
----------------------

Copyright 2016 Davide Mastromatteo
License: Apache-2.0
"""
from flows.Actions.Action import Action
import flows.Global

class RestartAction(Action):
    __doc__ = '\n    RestartAction Class\n    '
    type = 'restart'

    def on_input_received(self, action_input=None):
        super().on_input_received(action_input)
        flows.Global.PROCESS_MANAGER.restart()