# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/example_subdag_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1736 bytes
import airflow
from airflow.example_dags.subdags.subdag import subdag
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator
DAG_NAME = 'example_subdag_operator'
args = {'owner':'airflow', 
 'start_date':airflow.utils.dates.days_ago(2)}
dag = DAG(dag_id=DAG_NAME,
  default_args=args,
  schedule_interval='@once')
start = DummyOperator(task_id='start',
  dag=dag)
section_1 = SubDagOperator(task_id='section-1',
  subdag=(subdag(DAG_NAME, 'section-1', args)),
  dag=dag)
some_other_task = DummyOperator(task_id='some-other-task',
  dag=dag)
section_2 = SubDagOperator(task_id='section-2',
  subdag=(subdag(DAG_NAME, 'section-2', args)),
  dag=dag)
end = DummyOperator(task_id='end',
  dag=dag)
start >> section_1 >> some_other_task >> section_2 >> end