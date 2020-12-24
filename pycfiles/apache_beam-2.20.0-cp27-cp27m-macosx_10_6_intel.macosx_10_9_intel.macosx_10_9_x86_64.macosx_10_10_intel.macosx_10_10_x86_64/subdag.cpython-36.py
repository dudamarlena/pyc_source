# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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