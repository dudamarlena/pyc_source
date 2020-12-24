# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/latest_only_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2455 bytes
import pendulum
from airflow.models import BaseOperator, SkipMixin

class LatestOnlyOperator(BaseOperator, SkipMixin):
    __doc__ = '\n    Allows a workflow to skip tasks that are not running during the most\n    recent schedule interval.\n\n    If the task is run outside of the latest schedule interval, all\n    directly downstream tasks will be skipped.\n    '
    ui_color = '#e9ffdb'

    def execute(self, context):
        if context['dag_run']:
            if context['dag_run'].external_trigger:
                self.log.info('Externally triggered DAG_Run: allowing execution to proceed.')
                return
        now = pendulum.utcnow()
        left_window = context['dag'].following_schedule(context['execution_date'])
        right_window = context['dag'].following_schedule(left_window)
        self.log.info('Checking latest only with left_window: %s right_window: %s now: %s', left_window, right_window, now)
        if not left_window < now <= right_window:
            self.log.info('Not latest execution, skipping downstream.')
            downstream_tasks = context['task'].get_flat_relatives(upstream=False)
            self.log.debug('Downstream task_ids %s', downstream_tasks)
            if downstream_tasks:
                self.skip(context['dag_run'], context['ti'].execution_date, downstream_tasks)
            self.log.info('Done.')
        else:
            self.log.info('Latest, allowing execution to proceed.')