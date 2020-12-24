# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/ti_deps/deps/valid_state_dep.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2464 bytes
from airflow.exceptions import AirflowException
from airflow.ti_deps.deps.base_ti_dep import BaseTIDep
from airflow.utils.db import provide_session

class ValidStateDep(BaseTIDep):
    NAME = 'Task Instance State'
    IGNOREABLE = True

    def __init__(self, valid_states):
        super(ValidStateDep, self).__init__()
        if not valid_states:
            raise AirflowException('ValidStatesDep received an empty set of valid states.')
        self._valid_states = valid_states

    def __eq__(self, other):
        return type(self) == type(other) and self._valid_states == other._valid_states

    def __hash__(self):
        return hash((type(self), tuple(self._valid_states)))

    @provide_session
    def _get_dep_statuses(self, ti, session, dep_context):
        if dep_context.ignore_ti_state:
            yield self._passing_status(reason='Context specified that state should be ignored.')
            return
        if ti.state in self._valid_states:
            yield self._passing_status(reason=('Task state {} was valid.'.format(ti.state)))
            return
        yield self._failing_status(reason=("Task is in the '{0}' state which is not a valid state for execution. The task must be cleared in order to be run.".format(ti.state)))