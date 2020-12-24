# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_kubernetes_annotation.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1459 bytes
from __future__ import print_function
import airflow
from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG
args = {'owner':'airflow', 
 'start_date':airflow.utils.dates.days_ago(2)}
dag = DAG(dag_id='example_kubernetes_annotation',
  default_args=args,
  schedule_interval=None)

def print_stuff():
    print('annotated!')


start_task = PythonOperator(task_id='start_task',
  python_callable=print_stuff,
  dag=dag,
  executor_config={'KubernetesExecutor': {'annotations': {'test': 'annotation'}}})