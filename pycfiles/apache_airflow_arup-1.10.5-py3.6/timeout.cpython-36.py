# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/timeout.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 2055 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import signal, os
from airflow.exceptions import AirflowTaskTimeout
from airflow.utils.log.logging_mixin import LoggingMixin

class timeout(LoggingMixin):
    __doc__ = '\n    To be used in a ``with`` block and timeout its content.\n    '

    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message + ', PID: ' + str(os.getpid())

    def handle_timeout(self, signum, frame):
        self.log.error('Process timed out, PID: %s', str(os.getpid()))
        raise AirflowTaskTimeout(self.error_message)

    def __enter__(self):
        try:
            signal.signal(signal.SIGALRM, self.handle_timeout)
            signal.alarm(self.seconds)
        except ValueError as e:
            self.log.warning("timeout can't be used in the current context")
            self.log.exception(e)

    def __exit__(self, type, value, traceback):
        try:
            signal.alarm(0)
        except ValueError as e:
            self.log.warning("timeout can't be used in the current context")
            self.log.exception(e)