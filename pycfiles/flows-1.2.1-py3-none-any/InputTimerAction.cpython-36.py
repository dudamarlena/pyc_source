# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\mastromatteo\Progetti\flows\flows\Actions\InputTimerAction.py
# Compiled at: 2017-03-23 05:01:21
# Size of source mod 2**32: 862 bytes
"""
TimerAction.py
--------------

Copyright 2016 Davide Mastromatteo
"""
import threading
from flows.Actions.Action import Action

class TimerAction(Action):
    __doc__ = '\n    TimerAction Class\n    '
    type = 'timer'
    timeout = 0
    next_timer = None

    def run_operation(self):
        self.send_message('TIMER : ' + self.name)
        if self.is_running:
            self.start_timer()

    def start_timer(self):
        self.next_timer = threading.Timer(self.timeout, self.run_operation)
        self.next_timer.start()

    def on_stop(self):
        if self.next_timer is not None:
            self.next_timer.cancel()
        super().on_stop()

    def on_init(self):
        super().on_init()
        self.timeout = int(self.configuration['delay'])
        self.start_timer()