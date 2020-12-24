# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/task/task_runner/standard_task_runner.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1535 bytes
import psutil
from airflow.task.task_runner.base_task_runner import BaseTaskRunner
from airflow.utils.helpers import reap_process_group

class StandardTaskRunner(BaseTaskRunner):
    """StandardTaskRunner"""

    def __init__(self, local_task_job):
        super(StandardTaskRunner, self).__init__(local_task_job)

    def start(self):
        self.process = self.run_command()

    def return_code(self):
        return self.process.poll()

    def terminate(self):
        if self.process:
            if psutil.pid_exists(self.process.pid):
                reap_process_group(self.process.pid, self.log)

    def on_finish(self):
        super(StandardTaskRunner, self).on_finish()