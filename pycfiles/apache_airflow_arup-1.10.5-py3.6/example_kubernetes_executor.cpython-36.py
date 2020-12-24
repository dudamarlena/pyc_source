# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_kubernetes_executor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3186 bytes
from __future__ import print_function
import airflow
from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG
import os
args = {'owner':'airflow', 
 'start_date':airflow.utils.dates.days_ago(2)}
dag = DAG(dag_id='example_kubernetes_executor',
  default_args=args,
  schedule_interval=None)
affinity = {'podAntiAffinity': {'requiredDuringSchedulingIgnoredDuringExecution': [
                                                                        {'topologyKey':'kubernetes.io/hostname', 
                                                                         'labelSelector':{'matchExpressions': [
                                                                                               {'key':'app', 
                                                                                                'operator':'In', 
                                                                                                'values':[
                                                                                                 'airflow']}]}}]}}
tolerations = [
 {'key':'dedicated', 
  'operator':'Equal', 
  'value':'airflow'}]

def print_stuff():
    print('stuff!')


def use_zip_binary():
    rc = os.system('zip')
    assert rc == 0


start_task = PythonOperator(task_id='start_task',
  python_callable=print_stuff,
  dag=dag)
one_task = PythonOperator(task_id='one_task',
  python_callable=print_stuff,
  dag=dag,
  executor_config={'KubernetesExecutor': {'image': 'airflow/ci:latest'}})
two_task = PythonOperator(task_id='two_task',
  python_callable=use_zip_binary,
  dag=dag,
  executor_config={'KubernetesExecutor': {'image': 'airflow/ci_zip:latest'}})
three_task = PythonOperator(task_id='three_task',
  python_callable=print_stuff,
  dag=dag,
  executor_config={'KubernetesExecutor': {'request_memory':'128Mi',  'limit_memory':'128Mi', 
                        'tolerations':tolerations, 
                        'affinity':affinity}})
four_task = PythonOperator(task_id='four_task',
  python_callable=print_stuff,
  dag=dag,
  executor_config={'KubernetesExecutor': {'labels': {'foo': 'bar'}}})
start_task.set_downstream([one_task, two_task, three_task, four_task])