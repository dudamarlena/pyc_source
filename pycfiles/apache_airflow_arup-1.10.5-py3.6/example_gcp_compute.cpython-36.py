# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_gcp_compute.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4339 bytes
"""
Example Airflow DAG that starts, stops and sets the machine type of a Google Compute
Engine instance.

This DAG relies on the following OS environment variables

* GCP_PROJECT_ID - Google Cloud Platform project where the Compute Engine instance exists.
* GCE_ZONE - Google Cloud Platform zone where the instance exists.
* GCE_INSTANCE - Name of the Compute Engine instance.
* GCE_SHORT_MACHINE_TYPE_NAME - Machine type resource name to set, e.g. 'n1-standard-1'.
    See https://cloud.google.com/compute/docs/machine-types
"""
import os, airflow
from airflow import models
from airflow.contrib.operators.gcp_compute_operator import GceInstanceStartOperator, GceInstanceStopOperator, GceSetMachineTypeOperator
GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID', 'example-project')
GCE_ZONE = os.environ.get('GCE_ZONE', 'europe-west1-b')
GCE_INSTANCE = os.environ.get('GCE_INSTANCE', 'testinstance')
default_args = {'start_date': airflow.utils.dates.days_ago(1)}
GCE_SHORT_MACHINE_TYPE_NAME = os.environ.get('GCE_SHORT_MACHINE_TYPE_NAME', 'n1-standard-1')
SET_MACHINE_TYPE_BODY = {'machineType': 'zones/{}/machineTypes/{}'.format(GCE_ZONE, GCE_SHORT_MACHINE_TYPE_NAME)}
with models.DAG('example_gcp_compute',
  default_args=default_args,
  schedule_interval=None) as (dag):
    gce_instance_start = GceInstanceStartOperator(project_id=GCP_PROJECT_ID,
      zone=GCE_ZONE,
      resource_id=GCE_INSTANCE,
      task_id='gcp_compute_start_task')
    gce_instance_start2 = GceInstanceStartOperator(zone=GCE_ZONE,
      resource_id=GCE_INSTANCE,
      task_id='gcp_compute_start_task2')
    gce_instance_stop = GceInstanceStopOperator(project_id=GCP_PROJECT_ID,
      zone=GCE_ZONE,
      resource_id=GCE_INSTANCE,
      task_id='gcp_compute_stop_task')
    gce_instance_stop2 = GceInstanceStopOperator(zone=GCE_ZONE,
      resource_id=GCE_INSTANCE,
      task_id='gcp_compute_stop_task2')
    gce_set_machine_type = GceSetMachineTypeOperator(project_id=GCP_PROJECT_ID,
      zone=GCE_ZONE,
      resource_id=GCE_INSTANCE,
      body=SET_MACHINE_TYPE_BODY,
      task_id='gcp_compute_set_machine_type')
    gce_set_machine_type2 = GceSetMachineTypeOperator(zone=GCE_ZONE,
      resource_id=GCE_INSTANCE,
      body=SET_MACHINE_TYPE_BODY,
      task_id='gcp_compute_set_machine_type2')
    gce_instance_start >> gce_instance_start2 >> gce_instance_stop >> gce_instance_stop2 >> gce_set_machine_type >> gce_set_machine_type2