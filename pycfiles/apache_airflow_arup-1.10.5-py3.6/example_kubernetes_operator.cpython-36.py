# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_kubernetes_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2113 bytes
from airflow.utils.dates import days_ago
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.models import DAG
log = LoggingMixin().log
try:
    from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
    args = {'owner':'airflow', 
     'start_date':days_ago(2)}
    dag = DAG(dag_id='example_kubernetes_operator',
      default_args=args,
      schedule_interval=None)
    tolerations = [
     {'key':'key', 
      'operator':'Equal', 
      'value':'value'}]
    k = KubernetesPodOperator(namespace='default',
      image='ubuntu:16.04',
      cmds=[
     'bash', '-cx'],
      arguments=[
     'echo', '10'],
      labels={'foo': 'bar'},
      name='airflow-test-pod',
      in_cluster=False,
      task_id='task',
      get_logs=True,
      dag=dag,
      is_delete_operator_pod=False,
      tolerations=tolerations)
except ImportError as e:
    log.warning('Could not import KubernetesPodOperator: ' + str(e))
    log.warning("Install kubernetes dependencies with:     pip install 'apache-airflow[kubernetes]'")