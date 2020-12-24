# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_databricks_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2806 bytes
import airflow
from airflow import DAG
from airflow.contrib.operators.databricks_operator import DatabricksSubmitRunOperator
args = {'owner':'airflow', 
 'email':[
  'airflow@example.com'], 
 'depends_on_past':False, 
 'start_date':airflow.utils.dates.days_ago(2)}
dag = DAG(dag_id='example_databricks_operator',
  default_args=args,
  schedule_interval='@daily')
new_cluster = {'spark_version':'2.1.0-db3-scala2.11', 
 'node_type_id':'r3.xlarge', 
 'aws_attributes':{'availability': 'ON_DEMAND'}, 
 'num_workers':8}
notebook_task_params = {'new_cluster':new_cluster, 
 'notebook_task':{'notebook_path': '/Users/airflow@example.com/PrepareData'}}
notebook_task = DatabricksSubmitRunOperator(task_id='notebook_task',
  dag=dag,
  json=notebook_task_params)
spark_jar_task = DatabricksSubmitRunOperator(task_id='spark_jar_task',
  dag=dag,
  new_cluster=new_cluster,
  spark_jar_task={'main_class_name': 'com.example.ProcessData'},
  libraries=[
 {'jar': 'dbfs:/lib/etl-0.1.jar'}])
notebook_task.set_downstream(spark_jar_task)