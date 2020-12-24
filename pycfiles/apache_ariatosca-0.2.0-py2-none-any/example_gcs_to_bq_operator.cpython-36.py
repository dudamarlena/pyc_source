# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_gcs_to_bq_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2261 bytes
from typing import Any
import airflow
from airflow import models
from airflow.operators import bash_operator
gcs_to_bq = None
try:
    from airflow.contrib.operators import gcs_to_bq
except ImportError:
    pass

if gcs_to_bq is not None:
    args = {'owner':'airflow',  'start_date':airflow.utils.dates.days_ago(2)}
    dag = models.DAG(dag_id='example_gcs_to_bq_operator',
      default_args=args,
      schedule_interval=None)
    create_test_dataset = bash_operator.BashOperator(task_id='create_airflow_test_dataset',
      bash_command='bq mk airflow_test',
      dag=dag)
    load_csv = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(task_id='gcs_to_bq_example',
      bucket='cloud-samples-data',
      source_objects=[
     'bigquery/us-states/us-states.csv'],
      destination_project_dataset_table='airflow_test.gcs_to_bq_table',
      schema_fields=[
     {'name':'name', 
      'type':'STRING',  'mode':'NULLABLE'},
     {'name':'post_abbr', 
      'type':'STRING',  'mode':'NULLABLE'}],
      write_disposition='WRITE_TRUNCATE',
      dag=dag)
    delete_test_dataset = bash_operator.BashOperator(task_id='delete_airflow_test_dataset',
      bash_command='bq rm -rf airflow_test',
      dag=dag)
    create_test_dataset >> load_csv >> delete_test_dataset