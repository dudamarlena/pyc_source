# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/ti_deps/deps/task_concurrency_dep.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1766 bytes
from airflow.ti_deps.deps.base_ti_dep import BaseTIDep
from airflow.utils.db import provide_session

class TaskConcurrencyDep(BaseTIDep):
    """TaskConcurrencyDep"""
    NAME = 'Task Concurrency'
    IGNOREABLE = True
    IS_TASK_DEP = True

    @provide_session
    def _get_dep_statuses(self, ti, session, dep_context):
        if ti.task.task_concurrency is None:
            yield self._passing_status(reason='Task concurrency is not set.')
            return
        else:
            if ti.get_num_running_task_instances(session) >= ti.task.task_concurrency:
                yield self._failing_status(reason='The max task concurrency has been reached.')
                return
            yield self._passing_status(reason='The max task concurrency has not been reached.')
            return