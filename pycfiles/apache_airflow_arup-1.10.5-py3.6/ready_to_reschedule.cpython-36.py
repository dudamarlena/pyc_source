# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/ti_deps/deps/ready_to_reschedule.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 2923 bytes
from airflow.models import TaskReschedule
from airflow.ti_deps.deps.base_ti_dep import BaseTIDep
from airflow.utils import timezone
from airflow.utils.db import provide_session
from airflow.utils.state import State

class ReadyToRescheduleDep(BaseTIDep):
    NAME = 'Ready To Reschedule'
    IGNOREABLE = True
    IS_TASK_DEP = True
    RESCHEDULEABLE_STATES = {State.UP_FOR_RESCHEDULE, State.NONE}

    @provide_session
    def _get_dep_statuses(self, ti, session, dep_context):
        """
        Determines whether a task is ready to be rescheduled. Only tasks in
        NONE state with at least one row in task_reschedule table are
        handled by this dependency class, otherwise this dependency is
        considered as passed. This dependency fails if the latest reschedule
        request's reschedule date is still in future.
        """
        if dep_context.ignore_in_reschedule_period:
            yield self._passing_status(reason='The context specified that being in a reschedule period was permitted.')
            return
        else:
            if ti.state not in self.RESCHEDULEABLE_STATES:
                yield self._passing_status(reason='The task instance is not in State_UP_FOR_RESCHEDULE or NONE state.')
                return
            task_reschedules = TaskReschedule.find_for_task_instance(task_instance=ti)
            if not task_reschedules:
                yield self._passing_status(reason='There is no reschedule request for this task instance.')
                return
            now = timezone.utcnow()
            next_reschedule_date = task_reschedules[(-1)].reschedule_date
            if now >= next_reschedule_date:
                yield self._passing_status(reason='Task instance id ready for reschedule.')
                return
        yield self._failing_status(reason=('Task is not ready for reschedule yet but will be rescheduled automatically. Current date is {0} and task will be rescheduled at {1}.'.format(now.isoformat(), next_reschedule_date.isoformat())))