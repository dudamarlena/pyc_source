# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/example_pig_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1230 bytes
import airflow
from airflow.models import DAG
from airflow.operators.pig_operator import PigOperator
args = {'owner':'airflow', 
 'start_date':airflow.utils.dates.days_ago(2)}
dag = DAG(dag_id='example_pig_operator',
  default_args=args,
  schedule_interval=None)
run_this = PigOperator(task_id='run_example_pig_script',
  pig='ls /;',
  pig_opts='-x local',
  dag=dag)
run_this