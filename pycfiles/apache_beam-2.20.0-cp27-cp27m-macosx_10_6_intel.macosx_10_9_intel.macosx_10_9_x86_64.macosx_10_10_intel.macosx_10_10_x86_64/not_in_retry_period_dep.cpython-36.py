# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/ti_deps/deps/not_in_retry_period_dep.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 2164 bytes
from airflow.ti_deps.deps.base_ti_dep import BaseTIDep
from airflow.utils import timezone
from airflow.utils.db import provide_session
from airflow.utils.state import State

class NotInRetryPeriodDep(BaseTIDep):
    NAME = 'Not In Retry Period'
    IGNOREABLE = True
    IS_TASK_DEP = True

    @provide_session
    def _get_dep_statuses(self, ti, session, dep_context):
        if dep_context.ignore_in_retry_period:
            yield self._passing_status(reason='The context specified that being in a retry period was permitted.')
            return
        else:
            if ti.state != State.UP_FOR_RETRY:
                yield self._passing_status(reason='The task instance was not marked for retrying.')
                return
            cur_date = timezone.utcnow()
            next_task_retry_date = ti.next_retry_datetime()
            if ti.is_premature:
                yield self._failing_status(reason=('Task is not ready for retry yet but will be retried automatically. Current date is {0} and task will be retried at {1}.'.format(cur_date.isoformat(), next_task_retry_date.isoformat())))