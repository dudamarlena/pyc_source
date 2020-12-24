# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/example_skip_dag.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1826 bytes
import airflow
from airflow.exceptions import AirflowSkipException
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
args = {'owner':'airflow', 
 'start_date':airflow.utils.dates.days_ago(2)}

class DummySkipOperator(DummyOperator):
    ui_color = '#e8b7e4'

    def execute(self, context):
        raise AirflowSkipException


def create_test_pipeline(suffix, trigger_rule, dag):
    skip_operator = DummySkipOperator(task_id=('skip_operator_{}'.format(suffix)), dag=dag)
    always_true = DummyOperator(task_id=('always_true_{}'.format(suffix)), dag=dag)
    join = DummyOperator(task_id=trigger_rule, dag=dag, trigger_rule=trigger_rule)
    final = DummyOperator(task_id=('final_{}'.format(suffix)), dag=dag)
    skip_operator >> join
    always_true >> join
    join >> final


dag = DAG(dag_id='example_skip_dag', default_args=args)
create_test_pipeline('1', 'all_success', dag)
create_test_pipeline('2', 'one_success', dag)