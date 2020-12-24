# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_gcs_acl.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3109 bytes
__doc__ = '\nExample Airflow DAG that creates a new ACL entry on the specified bucket and object.\n\nThis DAG relies on the following OS environment variables\n\n* GCS_ACL_BUCKET - Name of a bucket.\n* GCS_ACL_OBJECT - Name of the object. For information about how to URL encode object\n    names to be path safe, see:\n    https://cloud.google.com/storage/docs/json_api/#encoding\n* GCS_ACL_ENTITY - The entity holding the permission.\n* GCS_ACL_BUCKET_ROLE - The access permission for the entity for the bucket.\n* GCS_ACL_OBJECT_ROLE - The access permission for the entity for the object.\n'
import os, airflow
from airflow import models
from airflow.contrib.operators.gcs_acl_operator import GoogleCloudStorageBucketCreateAclEntryOperator, GoogleCloudStorageObjectCreateAclEntryOperator
GCS_ACL_BUCKET = os.environ.get('GCS_ACL_BUCKET', 'example-bucket')
GCS_ACL_OBJECT = os.environ.get('GCS_ACL_OBJECT', 'example-object')
GCS_ACL_ENTITY = os.environ.get('GCS_ACL_ENTITY', 'example-entity')
GCS_ACL_BUCKET_ROLE = os.environ.get('GCS_ACL_BUCKET_ROLE', 'example-bucket-role')
GCS_ACL_OBJECT_ROLE = os.environ.get('GCS_ACL_OBJECT_ROLE', 'example-object-role')
default_args = {'start_date': airflow.utils.dates.days_ago(1)}
with models.DAG('example_gcs_acl',
  default_args=default_args,
  schedule_interval=None) as (dag):
    gcs_bucket_create_acl_entry_task = GoogleCloudStorageBucketCreateAclEntryOperator(bucket=GCS_ACL_BUCKET,
      entity=GCS_ACL_ENTITY,
      role=GCS_ACL_BUCKET_ROLE,
      task_id='gcs_bucket_create_acl_entry_task')
    gcs_object_create_acl_entry_task = GoogleCloudStorageObjectCreateAclEntryOperator(bucket=GCS_ACL_BUCKET,
      object_name=GCS_ACL_OBJECT,
      entity=GCS_ACL_ENTITY,
      role=GCS_ACL_OBJECT_ROLE,
      task_id='gcs_object_create_acl_entry_task')
    gcs_bucket_create_acl_entry_task >> gcs_object_create_acl_entry_task