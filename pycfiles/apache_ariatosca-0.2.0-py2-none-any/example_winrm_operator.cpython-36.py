# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_winrm_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2408 bytes
import airflow
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DAG
from datetime import timedelta
from airflow.contrib.hooks.winrm_hook import WinRMHook
from airflow.contrib.operators.winrm_operator import WinRMOperator
args = {'owner':'airflow', 
 'start_date':airflow.utils.dates.days_ago(2)}
dag = DAG(dag_id='POC_winrm_parallel',
  default_args=args,
  schedule_interval='0 0 * * *',
  dagrun_timeout=timedelta(minutes=60))
cmd = 'ls -l'
run_this_last = DummyOperator(task_id='run_this_last', dag=dag)
winRMHook = WinRMHook(ssh_conn_id='ssh_POC1')
t1 = WinRMOperator(task_id='wintask1',
  command='ls -altr',
  winrm_hook=winRMHook,
  dag=dag)
t2 = WinRMOperator(task_id='wintask2',
  command='sleep 60',
  winrm_hook=winRMHook,
  dag=dag)
t3 = WinRMOperator(task_id='wintask3',
  command="echo 'luke test' ",
  winrm_hook=winRMHook,
  dag=dag)
t1.set_downstream(run_this_last)
t2.set_downstream(run_this_last)
t3.set_downstream(run_this_last)