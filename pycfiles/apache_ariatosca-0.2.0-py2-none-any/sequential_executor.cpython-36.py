# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/executors/sequential_executor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2113 bytes
from builtins import str
import subprocess
from airflow.executors.base_executor import BaseExecutor
from airflow.utils.state import State

class SequentialExecutor(BaseExecutor):
    """SequentialExecutor"""

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