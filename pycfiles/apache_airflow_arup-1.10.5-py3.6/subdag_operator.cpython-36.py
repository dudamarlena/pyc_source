# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/subdag_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4148 bytes
from airflow import settings
from airflow.exceptions import AirflowException
from airflow.executors.sequential_executor import SequentialExecutor
from airflow.models import BaseOperator, Pool
from airflow.utils.decorators import apply_defaults
from airflow.utils.db import provide_session

class SubDagOperator(BaseOperator):
    __doc__ = "\n    This runs a sub dag. By convention, a sub dag's dag_id\n    should be prefixed by its parent and a dot. As in `parent.child`.\n\n    :param subdag: the DAG object to run as a subdag of the current DAG.\n    :type subdag: airflow.models.DAG\n    :param dag: the parent DAG for the subdag.\n    :type dag: airflow.models.DAG\n    :param executor: the executor for this subdag. Default to use SequentialExecutor.\n        Please find AIRFLOW-74 for more details.\n    :type executor: airflow.executors.base_executor.BaseExecutor\n    "
    ui_color = '#555'
    ui_fgcolor = '#fff'

    @provide_session
    @apply_defaults
    def __init__(self, subdag, executor=SequentialExecutor(), *args, **kwargs):
        dag = kwargs.get('dag') or settings.CONTEXT_MANAGER_DAG
        if not dag:
            raise AirflowException('Please pass in the `dag` param or call within a DAG context manager')
        session = kwargs.pop('session')
        (super(SubDagOperator, self).__init__)(*args, **kwargs)
        if dag.dag_id + '.' + kwargs['task_id'] != subdag.dag_id:
            raise AirflowException("The subdag's dag_id should have the form '{{parent_dag_id}}.{{this_task_id}}'. Expected '{d}.{t}'; received '{rcvd}'.".format(d=(dag.dag_id),
              t=(kwargs['task_id']),
              rcvd=(subdag.dag_id)))
        if self.pool:
            conflicts = [t for t in subdag.tasks if t.pool == self.pool]
            if conflicts:
                pool = session.query(Pool).filter(Pool.slots == 1).filter(Pool.pool == self.pool).first()
                if pool and any(t.pool == self.pool for t in subdag.tasks):
                    raise AirflowException('SubDagOperator {sd} and subdag task{plural} {t} both use pool {p}, but the pool only has 1 slot. The subdag tasks will never run.'.format(sd=(self.task_id),
                      plural=(len(conflicts) > 1),
                      t=(', '.join(t.task_id for t in conflicts)),
                      p=(self.pool)))
        self.subdag = subdag
        self.executor = executor

    def execute(self, context):
        ed = context['execution_date']
        self.subdag.run(start_date=ed,
          end_date=ed,
          donot_pickle=True,
          executor=(self.executor))