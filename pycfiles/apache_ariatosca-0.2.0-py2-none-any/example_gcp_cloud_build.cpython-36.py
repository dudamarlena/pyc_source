# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_gcp_cloud_build.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4374 bytes
__doc__ = '\nExample Airflow DAG that displays interactions with Google Cloud Build.\n\nThis DAG relies on the following OS environment variables:\n\n* GCP_PROJECT_ID - Google Cloud Project to use for the Cloud Function.\n* GCP_CLOUD_BUILD_ARCHIVE_URL - Path to the zipped source in Google Cloud Storage.\n    This object must be a gzipped archive file (.tar.gz) containing source to build.\n* GCP_CLOUD_BUILD_REPOSITORY_NAME - Name of the Cloud Source Repository.\n\n'
import os
from future.backports.urllib.parse import urlparse
from airflow import models
from airflow.contrib.operators.gcp_cloud_build_operator import CloudBuildCreateBuildOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils import dates
GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID', 'example-project')
GCP_SOURCE_ARCHIVE_URL = os.environ.get('GCP_CLOUD_BUILD_ARCHIVE_URL', 'gs://example-bucket/file')
GCP_SOURCE_REPOSITORY_NAME = os.environ.get('GCP_CLOUD_BUILD_REPOSITORY_NAME', '')
GCP_SOURCE_ARCHIVE_URL_PARTS = urlparse(GCP_SOURCE_ARCHIVE_URL)
GCP_SOURCE_BUCKET_NAME = GCP_SOURCE_ARCHIVE_URL_PARTS.netloc
create_build_from_storage_body = {'source':{'storageSource': GCP_SOURCE_ARCHIVE_URL}, 
 'steps':[
  {'name':'gcr.io/cloud-builders/docker', 
   'args':[
    'build', '-t', 'gcr.io/$PROJECT_ID/{}'.format(GCP_SOURCE_BUCKET_NAME), '.']}], 
 'images':[
  'gcr.io/$PROJECT_ID/{}'.format(GCP_SOURCE_BUCKET_NAME)]}
create_build_from_repo_body = {'source':{'repoSource': {'repoName':GCP_SOURCE_REPOSITORY_NAME,  'branchName':'master'}}, 
 'steps':[
  {'name':'gcr.io/cloud-builders/docker', 
   'args':[
    'build', '-t', 'gcr.io/$PROJECT_ID/$REPO_NAME', '.']}], 
 'images':[
  'gcr.io/$PROJECT_ID/$REPO_NAME']}
with models.DAG('example_gcp_cloud_build',
  default_args=dict(start_date=(dates.days_ago(1))), schedule_interval=None) as (dag):
    create_build_from_storage = CloudBuildCreateBuildOperator(task_id='create_build_from_storage',
      project_id=GCP_PROJECT_ID,
      body=create_build_from_storage_body)
    create_build_from_storage_result = BashOperator(bash_command="echo '{{ task_instance.xcom_pull('create_build_from_storage')['images'][0] }}'",
      task_id='create_build_from_storage_result')
    create_build_from_repo = CloudBuildCreateBuildOperator(task_id='create_build_from_repo',
      project_id=GCP_PROJECT_ID,
      body=create_build_from_repo_body)
    create_build_from_repo_result = BashOperator(bash_command="echo '{{ task_instance.xcom_pull('create_build_from_repo')['images'][0] }}'",
      task_id='create_build_from_repo_result')
    create_build_from_storage >> create_build_from_storage_result
    create_build_from_repo >> create_build_from_repo_result