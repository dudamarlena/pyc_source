# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/tutorial.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3022 bytes
"""
### Tutorial Documentation
Documentation that goes along with the Airflow tutorial located
[here](https://airflow.apache.org/tutorial.html)
"""
from datetime import timedelta
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
default_args = {'owner':'airflow', 
 'depends_on_past':False, 
 'start_date':airflow.utils.dates.days_ago(2), 
 'email':[
  'airflow@example.com'], 
 'email_on_failure':False, 
 'email_on_retry':False, 
 'retries':1, 
 'retry_delay':timedelta(minutes=5)}
dag = DAG('tutorial',
  default_args=default_args,
  description='A simple tutorial DAG',
  schedule_interval=timedelta(days=1))
t1 = BashOperator(task_id='print_date',
  bash_command='date',
  dag=dag)
t1.doc_md = "#### Task Documentation\nYou can document your task using the attributes `doc_md` (markdown),\n`doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets\nrendered in the UI's Task Instance Details page.\n![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)\n"
dag.doc_md = __doc__
t2 = BashOperator(task_id='sleep',
  depends_on_past=False,
  bash_command='sleep 5',
  dag=dag)
templated_command = '\n{% for i in range(5) %}\n    echo "{{ ds }}"\n    echo "{{ macros.ds_add(ds, 7)}}"\n    echo "{{ params.my_param }}"\n{% endfor %}\n'
t3 = BashOperator(task_id='templated',
  depends_on_past=False,
  bash_command=templated_command,
  params={'my_param': 'Parameter I passed in'},
  dag=dag)
t1 >> [t2, t3]