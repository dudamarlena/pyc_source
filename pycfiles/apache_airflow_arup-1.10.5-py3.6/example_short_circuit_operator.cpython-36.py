# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/example_short_circuit_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1651 bytes
import airflow.utils.helpers
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import ShortCircuitOperator
args = {'owner':'airflow', 
 'start_date':airflow.utils.dates.days_ago(2)}
dag = DAG(dag_id='example_short_circuit_operator', default_args=args)
cond_true = ShortCircuitOperator(task_id='condition_is_True',
  python_callable=(lambda : True),
  dag=dag)
cond_false = ShortCircuitOperator(task_id='condition_is_False',
  python_callable=(lambda : False),
  dag=dag)
ds_true = [DummyOperator(task_id=('true_' + str(i)), dag=dag) for i in (1, 2)]
ds_false = [DummyOperator(task_id=('false_' + str(i)), dag=dag) for i in (1, 2)]
(airflow.utils.helpers.chain)(cond_true, *ds_true)
(airflow.utils.helpers.chain)(cond_false, *ds_false)