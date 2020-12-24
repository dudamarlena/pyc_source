# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/example_bash_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2018 bytes
from builtins import range
from datetime import timedelta
import airflow
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
args = {'owner':'airflow', 
 'start_date':airflow.utils.dates.days_ago(2)}
dag = DAG(dag_id='example_bash_operator',
  default_args=args,
  schedule_interval='0 0 * * *',
  dagrun_timeout=timedelta(minutes=60))
run_this_last = DummyOperator(task_id='run_this_last',
  dag=dag)
run_this = BashOperator(task_id='run_after_loop',
  bash_command='echo 1',
  dag=dag)
run_this >> run_this_last
for i in range(3):
    task = BashOperator(task_id=('runme_' + str(i)),
      bash_command='echo "{{ task_instance_key_str }}" && sleep 1',
      dag=dag)
    task >> run_this

also_run_this = BashOperator(task_id='also_run_this',
  bash_command='echo "run_id={{ run_id }} | dag_run={{ dag_run }}"',
  dag=dag)
also_run_this >> run_this_last
if __name__ == '__main__':
    dag.cli()