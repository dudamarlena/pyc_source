# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\mastromatteo\Progetti\flows\flows\Actions\HashAction.py
# Compiled at: 2017-03-23 05:01:21
# Size of source mod 2**32: 670 bytes
"""
HashAction.py
-------------

Copyright 2016 Davide Mastromatteo
"""
import hashlib
from flows.Actions.Action import Action

class HashAction(Action):
    __doc__ = '\n    HashAction Class\n    '
    type = 'hash'

    def on_input_received(self, action_input=None):
        super().on_input_received(action_input)
        return_value = ''
        input_message = action_input.message
        md5_object = hashlib.md5()
        md5_object.update(input_message.encode('utf-8'))
        return_value = md5_object.hexdigest()
        self.send_message(return_value)