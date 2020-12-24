# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """ExternalTaskSensor"""
    template_fields = [
     'external_dag_id', 'external_task_id']
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