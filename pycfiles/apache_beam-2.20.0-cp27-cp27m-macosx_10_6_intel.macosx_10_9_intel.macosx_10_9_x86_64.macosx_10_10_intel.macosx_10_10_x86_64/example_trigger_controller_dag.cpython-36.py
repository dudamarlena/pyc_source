# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/example_trigger_controller_dag.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2758 bytes
__doc__ = 'This example illustrates the use of the TriggerDagRunOperator. There are 2\nentities at work in this scenario:\n1. The Controller DAG - the DAG that conditionally executes the trigger\n2. The Target DAG - DAG being triggered (in example_trigger_target_dag.py)\n\nThis example illustrates the following features :\n1. A TriggerDagRunOperator that takes:\n  a. A python callable that decides whether or not to trigger the Target DAG\n  b. An optional params dict passed to the python callable to help in\n     evaluating whether or not to trigger the Target DAG\n  c. The id (name) of the Target DAG\n  d. The python callable can add contextual info to the DagRun created by\n     way of adding a Pickleable payload (e.g. dictionary of primitives). This\n     state is then made available to the TargetDag\n2. A Target DAG : c.f. example_trigger_target_dag.py\n'
import pprint, airflow
from airflow import DAG
from airflow.operators.dagrun_operator import TriggerDagRunOperator
pp = pprint.PrettyPrinter(indent=4)

def conditionally_trigger(context, dag_run_obj):
    """This function decides whether or not to Trigger the remote DAG"""
    c_p = context['params']['condition_param']
    print('Controller DAG : conditionally_trigger = {}'.format(c_p))
    if context['params']['condition_param']:
        dag_run_obj.payload = {'message': context['params']['message']}
        pp.pprint(dag_run_obj.payload)
        return dag_run_obj


dag = DAG(dag_id='example_trigger_controller_dag',
  default_args={'owner':'airflow', 
 'start_date':airflow.utils.dates.days_ago(2)},
  schedule_interval='@once')
trigger = TriggerDagRunOperator(task_id='test_trigger_dagrun',
  trigger_dag_id='example_trigger_target_dag',
  python_callable=conditionally_trigger,
  params={'condition_param':True, 
 'message':'Hello World'},
  dag=dag)