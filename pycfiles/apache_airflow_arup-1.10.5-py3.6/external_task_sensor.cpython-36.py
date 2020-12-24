# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/external_task_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6708 bytes
import os
from airflow.exceptions import AirflowException
from airflow.models import TaskInstance, DagBag, DagModel, DagRun
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.db import provide_session
from airflow.utils.decorators import apply_defaults
from airflow.utils.state import State

class ExternalTaskSensor(BaseSensorOperator):
    __doc__ = "\n    Waits for a different DAG or a task in a different DAG to complete for a\n    specific execution_date\n\n    :param external_dag_id: The dag_id that contains the task you want to\n        wait for\n    :type external_dag_id: str\n    :param external_task_id: The task_id that contains the task you want to\n        wait for. If ``None`` the sensor waits for the DAG\n    :type external_task_id: str\n    :param allowed_states: list of allowed states, default is ``['success']``\n    :type allowed_states: list\n    :param execution_delta: time difference with the previous execution to\n        look at, the default is the same execution_date as the current task or DAG.\n        For yesterday, use [positive!] datetime.timedelta(days=1). Either\n        execution_delta or execution_date_fn can be passed to\n        ExternalTaskSensor, but not both.\n    :type execution_delta: datetime.timedelta\n    :param execution_date_fn: function that receives the current execution date\n        and returns the desired execution dates to query. Either execution_delta\n        or execution_date_fn can be passed to ExternalTaskSensor, but not both.\n    :type execution_date_fn: callable\n    :param check_existence: Set to `True` to check if the external task exists (when\n        external_task_id is not None) or check if the DAG to wait for exists (when\n        external_task_id is None), and immediately cease waiting if the external task\n        or DAG does not exist (default value: False).\n    :type check_existence: bool\n    "
    template_fields = ['external_dag_id', 'external_task_id']
    ui_color = '#19647e'

    @apply_defaults
    def __init__(self, external_dag_id, external_task_id, allowed_states=None, execution_delta=None, execution_date_fn=None, check_existence=False, *args, **kwargs):
        (super(ExternalTaskSensor, self).__init__)(*args, **kwargs)
        self.allowed_states = allowed_states or [State.SUCCESS]
        if external_task_id:
            if not set(self.allowed_states) <= set(State.task_states):
                raise ValueError('Valid values for `allowed_states` when `external_task_id` is not `None`: {}'.format(State.task_states))
        else:
            if not set(self.allowed_states) <= set(State.dag_states):
                raise ValueError('Valid values for `allowed_states` when `external_task_id` is `None`: {}'.format(State.dag_states))
        if execution_delta is not None:
            if execution_date_fn is not None:
                raise ValueError('Only one of `execution_delta` or `execution_date_fn` may be provided to ExternalTaskSensor; not both.')
        self.execution_delta = execution_delta
        self.execution_date_fn = execution_date_fn
        self.external_dag_id = external_dag_id
        self.external_task_id = external_task_id
        self.check_existence = check_existence

    @provide_session
    def poke(self, context, session=None):
        if self.execution_delta:
            dttm = context['execution_date'] - self.execution_delta
        else:
            if self.execution_date_fn:
                dttm = self.execution_date_fn(context['execution_date'])
            else:
                dttm = context['execution_date']
            dttm_filter = dttm if isinstance(dttm, list) else [dttm]
            serialized_dttm_filter = ','.join([datetime.isoformat() for datetime in dttm_filter])
            self.log.info('Poking for %s.%s on %s ... ', self.external_dag_id, self.external_task_id, serialized_dttm_filter)
            DM = DagModel
            TI = TaskInstance
            DR = DagRun
            if self.check_existence:
                dag_to_wait = session.query(DM).filter(DM.dag_id == self.external_dag_id).first()
                if not dag_to_wait:
                    raise AirflowException('The external DAG {} does not exist.'.format(self.external_dag_id))
                else:
                    if not os.path.exists(dag_to_wait.fileloc):
                        raise AirflowException('The external DAG {} was deleted.'.format(self.external_dag_id))
                    if self.external_task_id:
                        refreshed_dag_info = DagBag(dag_to_wait.fileloc).get_dag(self.external_dag_id)
                        if not refreshed_dag_info.has_task(self.external_task_id):
                            raise AirflowException('The external task{} in DAG {} does not exist.'.format(self.external_task_id, self.external_dag_id))
            if self.external_task_id:
                count = session.query(TI).filter(TI.dag_id == self.external_dag_id, TI.task_id == self.external_task_id, TI.state.in_(self.allowed_states), TI.execution_date.in_(dttm_filter)).count()
            else:
                count = session.query(DR).filter(DR.dag_id == self.external_dag_id, DR.state.in_(self.allowed_states), DR.execution_date.in_(dttm_filter)).count()
        session.commit()
        return count == len(dttm_filter)