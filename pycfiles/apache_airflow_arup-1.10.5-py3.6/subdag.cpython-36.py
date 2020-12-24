# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/subdags/subdag.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1305 bytes
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator

def subdag(parent_dag_name, child_dag_name, args):
    dag_subdag = DAG(dag_id=('%s.%s' % (parent_dag_name, child_dag_name)),
      default_args=args,
      schedule_interval='@daily')
    for i in range(5):
        DummyOperator(task_id=('%s-task-%s' % (child_dag_name, i + 1)),
          default_args=args,
          dag=dag_subdag)

    return dag_subdag