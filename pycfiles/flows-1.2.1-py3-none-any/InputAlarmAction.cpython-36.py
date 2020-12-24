# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\mastromatteo\Progetti\flows\flows\Actions\InputAlarmAction.py
# Compiled at: 2017-03-23 05:01:21
# Size of source mod 2**32: 1047 bytes
"""
AlarmAction.py
--------------

Use the parameter "date" as following to set an alarm

date = 01/11/2017 18:25

Copyright 2016 Davide Mastromatteo
"""
import datetime
from flows.Actions.Action import Action

class AlarmAction(Action):
    __doc__ = '\n    AlarmAction Class\n    '
    type = 'alarm'
    next = None

    def on_init(self):
        super().on_init()
        if 'date' not in self.configuration:
            raise ValueError(str.format('The alarm action {0} is not properly configured.The Date parameter is missing', self.name))
        date = self.configuration['date']
        self.next = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M')

    def on_cycle(self):
        super().on_cycle()
        now = datetime.datetime.now()
        now = now.replace(second=0, microsecond=0)
        if now >= self.next:
            self.next = None
            self.send_message('ALARM')