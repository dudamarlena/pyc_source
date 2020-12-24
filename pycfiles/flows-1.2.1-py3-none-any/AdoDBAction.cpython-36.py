# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\mastromatteo\Progetti\flows\flows\Actions\AdoDBAction.py
# Compiled at: 2017-03-23 05:15:35
# Size of source mod 2**32: 1179 bytes
import adodbapi
from flows.Actions.Action import Action

class AdoDBAction(Action):
    __doc__ = '\n    AdoDBAction Class\n    '
    type = 'adodb'
    conn = None
    query = None
    separator = ';'

    def on_init(self):
        super().on_init()
        connstring = self.configuration['connstring']
        self.conn = adodbapi.connect(connstring)
        self.query = self.configuration['query']
        if 'separator' in self.configuration:
            self.separator = self.configuration['separator']

    def on_stop(self):
        super().on_stop()
        self.conn.close()

    def on_input_received(self, action_input=None):
        super().on_input_received(action_input)
        if self.conn is not None:
            if self.query is not None:
                cursor = self.conn.cursor()
                cursor.execute(self.query)
                row = cursor.fetchone()
                return_value = self.separator.join(map(str, row))
                self.send_message(return_value)