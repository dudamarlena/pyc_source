# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/s_tui/sources/hook.py
# Compiled at: 2019-12-27 09:31:39
# Size of source mod 2**32: 1887 bytes
from datetime import datetime, timedelta

class Hook:
    __doc__ = "\n    Event handler that invokes an arbitrary callback when invoked.\n    If the timeout_milliseconds argument is greater than 0,\n    the hook will be suspended for n milliseconds after it's being invoked.\n    "

    def __init__(self, callback, timeout_milliseconds=0, *callback_args):
        self.callback = callback
        self.timeout_milliseconds = timeout_milliseconds
        self.callback_args = callback_args
        self.ready_time = datetime.now()

    def is_ready(self):
        """
        Returns whether the hook is ready to invoke its callback or not
        """
        return datetime.now() >= self.ready_time

    def invoke(self):
        """
        Run callback, optionally passing a variable number
        of arguments `callback_args`
        """
        if self.timeout_milliseconds > 0:
            self.ready_time = datetime.now() + timedelta(milliseconds=(self.timeout_milliseconds))
        self.callback(self.callback_args)