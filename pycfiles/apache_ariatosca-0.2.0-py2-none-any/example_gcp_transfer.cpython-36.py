# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_gcp_transfer.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 10689 bytes
__doc__ = '\nExample Airflow DAG that demonstrates interactions with Google Cloud Transfer.\n\n\nThis DAG relies on the following OS environment variables\n\n* GCP_PROJECT_ID - Google Cloud Project to use for the Google Cloud Transfer Service.\n* GCP_DESCRIPTION - Description of transfer job\n* GCP_TRANSFER_SOURCE_AWS_BUCKET - Amazon Web Services Storage bucket from which files are copied.\n  .. warning::\n    You need to provide a large enough set of data so that operations do not execute too quickly.\n    Otherwise, DAG will fail.\n* GCP_TRANSFER_FIRST_TARGET_BUCKET - Google Cloud Storage bucket to which files are copied from AWS.\n  It is also a source bucket in next step\n* GCP_TRANSFER_SECOND_TARGET_BUCKET - Google Cloud Storage bucket bucket to which files are copied\n* WAIT_FOR_OPERATION_POKE_INTERVAL - interval of what to check the status of the operation\n  A smaller value than the default value accelerates the system test and ensures its correct execution with\n  smaller quantities of files in the source bucket\n  Look at documentation of :class:`~airflow.operators.sensors.BaseSensorOperator` for more information\n\n'
import os
from datetime import datetime, timedelta
from typing import Any, Dict
from airflow import models
from airflow.contrib.hooks.gcp_transfer_hook import GcpTransferOperationStatus, GcpTransferJobsStatus, TRANSFER_OPTIONS, PROJECT_ID, BUCKET_NAME, GCS_DATA_SINK, STATUS, DESCRIPTION, GCS_DATA_SOURCE, START_TIME_OF_DAY, SCHEDULE_END_DATE, SCHEDULE_START_DATE, SCHEDULE, AWS_S3_DATA_SOURCE, TRANSFER_SPEC, FILTER_PROJECT_ID, FILTER_JOB_NAMES, TRANSFER_JOB, TRANSFER_JOB_FIELD_MASK, ALREADY_EXISTING_IN_SINK
from airflow.contrib.operators.gcp_transfer_operator import GcpTransferServiceJobCreateOperator, GcpTransferServiceJobDeleteOperator, GcpTransferServiceJobUpdateOperator, GcpTransferServiceOperationsListOperator, GcpTransferServiceOperationGetOperator, GcpTransferServiceOperationPauseOperator, GcpTransferServiceOperationResumeOperator, GcpTransferServiceOperationCancelOperator
from airflow.contrib.sensors.gcp_transfer_sensor import GCPTransferServiceWaitForJobStatusSensor
from airflow.utils.dates import days_ago
GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID', 'example-project')
GCP_DESCRIPTION = os.environ.get('GCP_DESCRIPTION', 'description')
GCP_TRANSFER_TARGET_BUCKET = os.environ.get('GCP_TRANSFER_TARGET_BUCKET')
WAIT_FOR_OPERATION_POKE_INTERVAL = int(os.environ.get('WAIT_FOR_OPERATION_POKE_INTERVAL', 5))
GCP_TRANSFER_SOURCE_AWS_BUCKET = os.environ.get('GCP_TRANSFER_SOURCE_AWS_BUCKET')
GCP_TRANSFER_FIRST_TARGET_BUCKET = os.environ.get('GCP_TRANSFER_FIRST_TARGET_BUCKET', 'gcp-transfer-first-target')
GCP_TRANSFER_SECOND_TARGET_BUCKET = os.environ.get('GCP_TRANSFER_SECOND_TARGET_BUCKET', 'gcp-transfer-second-target')
aws_to_gcs_transfer_body = {DESCRIPTION: GCP_DESCRIPTION, 
 STATUS: GcpTransferJobsStatus.ENABLED, 
 PROJECT_ID: GCP_PROJECT_ID, 
 SCHEDULE: {SCHEDULE_START_DATE: datetime(2015, 1, 1).date(), 
            SCHEDULE_END_DATE: datetime(2030, 1, 1).date(), 
            START_TIME_OF_DAY: (datetime.utcnow() + timedelta(minutes=2)).time()}, 
 
 TRANSFER_SPEC: {AWS_S3_DATA_SOURCE: {BUCKET_NAME: GCP_TRANSFER_SOURCE_AWS_BUCKET}, 
                 GCS_DATA_SINK: {BUCKET_NAME: GCP_TRANSFER_FIRST_TARGET_BUCKET}, 
                 TRANSFER_OPTIONS: {ALREADY_EXISTING_IN_SINK: True}}}
gcs_to_gcs_transfer_body = {DESCRIPTION: GCP_DESCRIPTION, 
 STATUS: GcpTransferJobsStatus.ENABLED, 
 PROJECT_ID: GCP_PROJECT_ID, 
 SCHEDULE: {SCHEDULE_START_DATE: datetime(2015, 1, 1).date(), 
            SCHEDULE_END_DATE: datetime(2030, 1, 1).date(), 
            START_TIME_OF_DAY: (datetime.utcnow() + timedelta(minutes=2)).time()}, 
 
 TRANSFER_SPEC: {GCS_DATA_SOURCE: {BUCKET_NAME: GCP_TRANSFER_FIRST_TARGET_BUCKET}, 
                 GCS_DATA_SINK: {BUCKET_NAME: GCP_TRANSFER_SECOND_TARGET_BUCKET}, 
                 TRANSFER_OPTIONS: {ALREADY_EXISTING_IN_SINK: True}}}
update_body = {PROJECT_ID: GCP_PROJECT_ID, 
 TRANSFER_JOB: {DESCRIPTION: '{}_updated'.format(GCP_DESCRIPTION)}, 
 TRANSFER_JOB_FIELD_MASK: 'description'}
list_filter_dict = {FILTER_PROJECT_ID: GCP_PROJECT_ID, FILTER_JOB_NAMES: []}
default_args = {'start_date': days_ago(1)}
with models.DAG('example_gcp_transfer',
  default_args=default_args, schedule_interval=None) as (dag):
    create_transfer_job_from_aws = GcpTransferServiceJobCreateOperator(task_id='create_transfer_job_from_aws',
      body=aws_to_gcs_transfer_body)
    wait_for_operation_to_start = GCPTransferServiceWaitForJobStatusSensor(task_id='wait_for_operation_to_start',
      job_name="{{task_instance.xcom_pull('create_transfer_job_from_aws')['name']}}",
      project_id=GCP_PROJECT_ID,
      expected_statuses={
     GcpTransferOperationStatus.IN_PROGRESS},
      poke_interval=WAIT_FOR_OPERATION_POKE_INTERVAL)
    pause_operation = GcpTransferServiceOperationPauseOperator(task_id='pause_operation',
      operation_name="{{task_instance.xcom_pull('wait_for_operation_to_start', key='sensed_operations')[0]['name']}}")
    update_job = GcpTransferServiceJobUpdateOperator(task_id='update_job',
      job_name="{{task_instance.xcom_pull('create_transfer_job_from_aws')['name']}}",
      body=update_body)
    list_operations = GcpTransferServiceOperationsListOperator(task_id='list_operations',
      filter={FILTER_PROJECT_ID: GCP_PROJECT_ID, 
     FILTER_JOB_NAMES: ["{{task_instance.xcom_pull('create_transfer_job_from_aws')['name']}}"]})
    get_operation = GcpTransferServiceOperationGetOperator(task_id='get_operation',
      operation_name="{{task_instance.xcom_pull('list_operations')[0]['name']}}")
    resume_operation = GcpTransferServiceOperationResumeOperator(task_id='resume_operation',
      operation_name="{{task_instance.xcom_pull('get_operation')['name']}}")
    wait_for_operation_to_end = GCPTransferServiceWaitForJobStatusSensor(task_id='wait_for_operation_to_end',
      job_name="{{task_instance.xcom_pull('create_transfer_job_from_aws')['name']}}",
      project_id=GCP_PROJECT_ID,
      expected_statuses={
     GcpTransferOperationStatus.SUCCESS},
      poke_interval=WAIT_FOR_OPERATION_POKE_INTERVAL)
    job_time = datetime.utcnow() + timedelta(minutes=2)
    gcs_to_gcs_transfer_body['schedule']['startTimeOfDay'] = (datetime.utcnow() + timedelta(minutes=2)).time()
    create_transfer_job_from_gcp = GcpTransferServiceJobCreateOperator(task_id='create_transfer_job_from_gcp',
      body=gcs_to_gcs_transfer_body)
    wait_for_second_operation_to_start = GCPTransferServiceWaitForJobStatusSensor(task_id='wait_for_second_operation_to_start',
      job_name="{{ task_instance.xcom_pull('create_transfer_job_from_gcp')['name'] }}",
      project_id=GCP_PROJECT_ID,
      expected_statuses={
     GcpTransferOperationStatus.IN_PROGRESS},
      poke_interval=WAIT_FOR_OPERATION_POKE_INTERVAL)
    cancel_operation = GcpTransferServiceOperationCancelOperator(task_id='cancel_operation',
      operation_name="{{task_instance.xcom_pull('wait_for_second_operation_to_start', key='sensed_operations')[0]['name']}}")
    delete_transfer_from_aws_job = GcpTransferServiceJobDeleteOperator(task_id='delete_transfer_from_aws_job',
      job_name="{{task_instance.xcom_pull('create_transfer_job_from_aws')['name']}}",
      project_id=GCP_PROJECT_ID)
    delete_transfer_from_gcp_job = GcpTransferServiceJobDeleteOperator(task_id='delete_transfer_from_gcp_job',
      job_name="{{task_instance.xcom_pull('create_transfer_job_from_gcp')['name']}}",
      project_id=GCP_PROJECT_ID)
    create_transfer_job_from_aws >> wait_for_operation_to_start >> pause_operation >> list_operations >> get_operation >> resume_operation >> wait_for_operation_to_end >> create_transfer_job_from_gcp >> wait_for_second_operation_to_start >> cancel_operation >> delete_transfer_from_aws_job >> delete_transfer_from_gcp_job