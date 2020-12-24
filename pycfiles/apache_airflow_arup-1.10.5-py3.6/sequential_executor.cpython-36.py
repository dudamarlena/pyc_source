# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/executors/sequential_executor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2113 bytes
from builtins import str
import subprocess
from airflow.executors.base_executor import BaseExecutor
from airflow.utils.state import State

class SequentialExecutor(BaseExecutor):
    __doc__ = "\n    This executor will only run one task instance at a time, can be used\n    for debugging. It is also the only executor that can be used with sqlite\n    since sqlite doesn't support multiple connections.\n\n    Since we want airflow to work out of the box, it defaults to this\n    SequentialExecutor alongside sqlite as you first install it.\n    "

    def __init__(self):
        super(SequentialExecutor, self).__init__()
        self.commands_to_run = []

    def execute_async(self, key, command, queue=None, executor_config=None):
        self.commands_to_run.append((key, command))

    def sync(self):
        for key, command in self.commands_to_run:
            self.log.info('Executing command: %s', command)
            try:
                subprocess.check_call(command, close_fds=True)
                self.change_state(key, State.SUCCESS)
            except subprocess.CalledProcessError as e:
                self.change_state(key, State.FAILED)
                self.log.error('Failed to execute task %s.', str(e))

        self.commands_to_run = []

    def end(self):
        self.heartbeat()