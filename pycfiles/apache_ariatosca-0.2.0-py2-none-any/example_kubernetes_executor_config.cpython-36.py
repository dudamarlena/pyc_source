# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_kubernetes_executor_config.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2623 bytes
from __future__ import print_function
import airflow
from airflow.operators.python_operator import PythonOperator
from libs.helper import print_stuff
from airflow.models import DAG
import os
args = {'owner':'airflow', 
 'start_date':airflow.utils.dates.days_ago(2)}
dag = DAG(dag_id='example_kubernetes_executor_config',
  default_args=args,
  schedule_interval=None)

def test_volume_mount():
    with open('/foo/volume_mount_test.txt', 'w') as (foo):
        foo.write('Hello')
    rc = os.system('cat /foo/volume_mount_test.txt')
    assert rc == 0


start_task = PythonOperator(task_id='start_task',
  python_callable=print_stuff,
  dag=dag,
  executor_config={'KubernetesExecutor': {'annotations': {'test': 'annotation'}}})
second_task = PythonOperator(task_id='four_task',
  python_callable=test_volume_mount,
  dag=dag,
  executor_config={'KubernetesExecutor': {'volumes':[
                         {'name':'example-kubernetes-test-volume', 
                          'hostPath':{'path': '/tmp/'}}], 
                        'volume_mounts':[
                         {'mountPath':'/foo/', 
                          'name':'example-kubernetes-test-volume'}]}})
third_task = PythonOperator(task_id='non_root_task',
  python_callable=print_stuff,
  dag=dag,
  executor_config={'KubernetesExecutor': {'securityContext': {'runAsUser': 1000}}})
start_task.set_downstream(second_task)
second_task.set_downstream(third_task)