# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_gcp_dataproc_create_cluster.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1924 bytes
__doc__ = '\nExample Airflow DAG that creates DataProc cluster.\n'
import os, airflow
from airflow import models
from airflow.contrib.operators.dataproc_operator import DataprocClusterCreateOperator, DataprocClusterDeleteOperator
PROJECT_ID = os.environ.get('GCP_PROJECT_ID', 'an-id')
CLUSTER_NAME = os.environ.get('GCP_DATAPROC_CLUSTER_NAME', 'example-project')
REGION = os.environ.get('GCP_LOCATION', 'europe-west1')
ZONE = os.environ.get('GCP_REGION', 'europe-west-1b')
with models.DAG('example_gcp_dataproc_create_cluster',
  default_args={'start_date': airflow.utils.dates.days_ago(1)},
  schedule_interval=None) as (dag):
    create_cluster = DataprocClusterCreateOperator(task_id='create_cluster',
      cluster_name=CLUSTER_NAME,
      project_id=PROJECT_ID,
      num_workers=2,
      region=REGION)
    delete_cluster = DataprocClusterDeleteOperator(task_id='delete_cluster',
      project_id=PROJECT_ID,
      cluster_name=CLUSTER_NAME,
      region=REGION)
    create_cluster >> delete_cluster