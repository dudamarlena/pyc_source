# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_gcp_sql.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 14961 bytes
__doc__ = '\nExample Airflow DAG that creates, patches and deletes a Cloud SQL instance, and also\ncreates, patches and deletes a database inside the instance, in Google Cloud Platform.\n\nThis DAG relies on the following OS environment variables\nhttps://airflow.apache.org/concepts.html#variables\n* GCP_PROJECT_ID - Google Cloud Platform project for the Cloud SQL instance.\n* INSTANCE_NAME - Name of the Cloud SQL instance.\n* DB_NAME - Name of the database inside a Cloud SQL instance.\n'
import os, airflow
from airflow import models
from airflow.contrib.operators.gcp_sql_operator import CloudSqlInstanceCreateOperator, CloudSqlInstancePatchOperator, CloudSqlInstanceDeleteOperator, CloudSqlInstanceDatabaseCreateOperator, CloudSqlInstanceDatabasePatchOperator, CloudSqlInstanceDatabaseDeleteOperator, CloudSqlInstanceExportOperator, CloudSqlInstanceImportOperator
from airflow.contrib.operators.gcs_acl_operator import GoogleCloudStorageBucketCreateAclEntryOperator, GoogleCloudStorageObjectCreateAclEntryOperator
from six.moves.urllib.parse import urlsplit
GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID', 'example-project')
INSTANCE_NAME = os.environ.get('GCSQL_MYSQL_INSTANCE_NAME', 'test-mysql')
INSTANCE_NAME2 = os.environ.get('GCSQL_MYSQL_INSTANCE_NAME2', 'test-mysql2')
DB_NAME = os.environ.get('GCSQL_MYSQL_DATABASE_NAME', 'testdb')
EXPORT_URI = os.environ.get('GCSQL_MYSQL_EXPORT_URI', 'gs://bucketName/fileName')
IMPORT_URI = os.environ.get('GCSQL_MYSQL_IMPORT_URI', 'gs://bucketName/fileName')
FAILOVER_REPLICA_NAME = INSTANCE_NAME + '-failover-replica'
READ_REPLICA_NAME = INSTANCE_NAME + '-read-replica'
body = {'name':INSTANCE_NAME, 
 'settings':{'tier':'db-n1-standard-1', 
  'backupConfiguration':{'binaryLogEnabled':True, 
   'enabled':True, 
   'startTime':'05:00'}, 
  'activationPolicy':'ALWAYS', 
  'dataDiskSizeGb':30, 
  'dataDiskType':'PD_SSD', 
  'databaseFlags':[],  'ipConfiguration':{'ipv4Enabled':True, 
   'requireSsl':True}, 
  'locationPreference':{'zone': 'europe-west4-a'}, 
  'maintenanceWindow':{'hour':5, 
   'day':7, 
   'updateTrack':'canary'}, 
  'pricingPlan':'PER_USE', 
  'replicationType':'ASYNCHRONOUS', 
  'storageAutoResize':True, 
  'storageAutoResizeLimit':0, 
  'userLabels':{'my-key': 'my-value'}}, 
 'failoverReplica':{'name': FAILOVER_REPLICA_NAME}, 
 'databaseVersion':'MYSQL_5_7', 
 'region':'europe-west4'}
body2 = {'name':INSTANCE_NAME2, 
 'settings':{'tier': 'db-n1-standard-1'}, 
 'databaseVersion':'MYSQL_5_7', 
 'region':'europe-west4'}
read_replica_body = {'name':READ_REPLICA_NAME, 
 'settings':{'tier': 'db-n1-standard-1'}, 
 'databaseVersion':'MYSQL_5_7', 
 'region':'europe-west4', 
 'masterInstanceName':INSTANCE_NAME}
patch_body = {'name':INSTANCE_NAME, 
 'settings':{'dataDiskSizeGb':35, 
  'maintenanceWindow':{'hour':3, 
   'day':6, 
   'updateTrack':'canary'}, 
  'userLabels':{'my-key-patch': 'my-value-patch'}}}
export_body = {'exportContext': {'fileType':'sql', 
                   'uri':EXPORT_URI, 
                   'sqlExportOptions':{'schemaOnly': False}}}
import_body = {'importContext': {'fileType':'sql', 
                   'uri':IMPORT_URI}}
db_create_body = {'instance':INSTANCE_NAME, 
 'name':DB_NAME, 
 'project':GCP_PROJECT_ID}
db_patch_body = {'charset':'utf16', 
 'collation':'utf16_general_ci'}
default_args = {'start_date': airflow.utils.dates.days_ago(1)}
with models.DAG('example_gcp_sql',
  default_args=default_args,
  schedule_interval=None) as (dag):

    def next_dep(task, prev):
        prev >> task
        return task


    sql_instance_create_task = CloudSqlInstanceCreateOperator(project_id=GCP_PROJECT_ID,
      body=body,
      instance=INSTANCE_NAME,
      task_id='sql_instance_create_task')
    prev_task = sql_instance_create_task
    sql_instance_create_2_task = CloudSqlInstanceCreateOperator(project_id=GCP_PROJECT_ID,
      body=body2,
      instance=INSTANCE_NAME2,
      task_id='sql_instance_create_task2')
    prev_task = sql_instance_create_task
    prev_task = next_dep(sql_instance_create_2_task, prev_task)
    sql_instance_read_replica_create = CloudSqlInstanceCreateOperator(project_id=GCP_PROJECT_ID,
      body=read_replica_body,
      instance=INSTANCE_NAME2,
      task_id='sql_instance_read_replica_create')
    prev_task = next_dep(sql_instance_read_replica_create, prev_task)
    sql_instance_patch_task = CloudSqlInstancePatchOperator(project_id=GCP_PROJECT_ID,
      body=patch_body,
      instance=INSTANCE_NAME,
      task_id='sql_instance_patch_task')
    sql_instance_patch_task2 = CloudSqlInstancePatchOperator(body=patch_body,
      instance=INSTANCE_NAME,
      task_id='sql_instance_patch_task2')
    prev_task = next_dep(sql_instance_patch_task, prev_task)
    prev_task = next_dep(sql_instance_patch_task2, prev_task)
    sql_db_create_task = CloudSqlInstanceDatabaseCreateOperator(project_id=GCP_PROJECT_ID,
      body=db_create_body,
      instance=INSTANCE_NAME,
      task_id='sql_db_create_task')
    sql_db_create_task2 = CloudSqlInstanceDatabaseCreateOperator(body=db_create_body,
      instance=INSTANCE_NAME,
      task_id='sql_db_create_task2')
    prev_task = next_dep(sql_db_create_task, prev_task)
    prev_task = next_dep(sql_db_create_task2, prev_task)
    sql_db_patch_task = CloudSqlInstanceDatabasePatchOperator(project_id=GCP_PROJECT_ID,
      body=db_patch_body,
      instance=INSTANCE_NAME,
      database=DB_NAME,
      task_id='sql_db_patch_task')
    sql_db_patch_task2 = CloudSqlInstanceDatabasePatchOperator(body=db_patch_body,
      instance=INSTANCE_NAME,
      database=DB_NAME,
      task_id='sql_db_patch_task2')
    prev_task = next_dep(sql_db_patch_task, prev_task)
    prev_task = next_dep(sql_db_patch_task2, prev_task)
    export_url_split = urlsplit(EXPORT_URI)
    sql_gcp_add_bucket_permission_task = GoogleCloudStorageBucketCreateAclEntryOperator(entity="user-{{ task_instance.xcom_pull('sql_instance_create_task', key='service_account_email') }}",
      role='WRITER',
      bucket=(export_url_split[1]),
      task_id='sql_gcp_add_bucket_permission_task')
    prev_task = next_dep(sql_gcp_add_bucket_permission_task, prev_task)
    sql_export_task = CloudSqlInstanceExportOperator(project_id=GCP_PROJECT_ID,
      body=export_body,
      instance=INSTANCE_NAME,
      task_id='sql_export_task')
    sql_export_task2 = CloudSqlInstanceExportOperator(body=export_body,
      instance=INSTANCE_NAME,
      task_id='sql_export_task2')
    prev_task = next_dep(sql_export_task, prev_task)
    prev_task = next_dep(sql_export_task2, prev_task)
    import_url_split = urlsplit(IMPORT_URI)
    sql_gcp_add_object_permission_task = GoogleCloudStorageObjectCreateAclEntryOperator(entity="user-{{ task_instance.xcom_pull('sql_instance_create_task2', key='service_account_email') }}",
      role='READER',
      bucket=(import_url_split[1]),
      object_name=(import_url_split[2][1:]),
      task_id='sql_gcp_add_object_permission_task')
    prev_task = next_dep(sql_gcp_add_object_permission_task, prev_task)
    sql_gcp_add_bucket_permission_2_task = GoogleCloudStorageBucketCreateAclEntryOperator(entity="user-{{ task_instance.xcom_pull('sql_instance_create_task2', key='service_account_email') }}",
      role='WRITER',
      bucket=(import_url_split[1]),
      task_id='sql_gcp_add_bucket_permission_2_task')
    prev_task = next_dep(sql_gcp_add_bucket_permission_2_task, prev_task)
    sql_import_task = CloudSqlInstanceImportOperator(project_id=GCP_PROJECT_ID,
      body=import_body,
      instance=INSTANCE_NAME2,
      task_id='sql_import_task')
    sql_import_task2 = CloudSqlInstanceImportOperator(body=import_body,
      instance=INSTANCE_NAME2,
      task_id='sql_import_task2')
    prev_task = next_dep(sql_import_task, prev_task)
    prev_task = next_dep(sql_import_task2, prev_task)
    sql_db_delete_task = CloudSqlInstanceDatabaseDeleteOperator(project_id=GCP_PROJECT_ID,
      instance=INSTANCE_NAME,
      database=DB_NAME,
      task_id='sql_db_delete_task')
    sql_db_delete_task2 = CloudSqlInstanceDatabaseDeleteOperator(instance=INSTANCE_NAME,
      database=DB_NAME,
      task_id='sql_db_delete_task2')
    prev_task = next_dep(sql_db_delete_task, prev_task)
    prev_task = next_dep(sql_db_delete_task2, prev_task)
    sql_instance_failover_replica_delete_task = CloudSqlInstanceDeleteOperator(project_id=GCP_PROJECT_ID,
      instance=FAILOVER_REPLICA_NAME,
      task_id='sql_instance_failover_replica_delete_task')
    sql_instance_read_replica_delete_task = CloudSqlInstanceDeleteOperator(project_id=GCP_PROJECT_ID,
      instance=READ_REPLICA_NAME,
      task_id='sql_instance_read_replica_delete_task')
    prev_task = next_dep(sql_instance_failover_replica_delete_task, prev_task)
    prev_task = next_dep(sql_instance_read_replica_delete_task, prev_task)
    sql_instance_delete_task = CloudSqlInstanceDeleteOperator(project_id=GCP_PROJECT_ID,
      instance=INSTANCE_NAME,
      task_id='sql_instance_delete_task')
    sql_instance_delete_task2 = CloudSqlInstanceDeleteOperator(instance=INSTANCE_NAME2,
      task_id='sql_instance_delete_task2')
    prev_task = next_dep(sql_instance_delete_task, prev_task)
    sql_instance_delete_2_task = CloudSqlInstanceDeleteOperator(project_id=GCP_PROJECT_ID,
      instance=INSTANCE_NAME2,
      task_id='sql_instance_delete_2_task')
    prev_task = next_dep(sql_instance_delete_2_task, prev_task)