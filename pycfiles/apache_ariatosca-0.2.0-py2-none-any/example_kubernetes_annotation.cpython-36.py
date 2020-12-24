# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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