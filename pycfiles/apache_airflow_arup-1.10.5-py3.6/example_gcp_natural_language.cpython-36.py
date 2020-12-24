# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_gcp_natural_language.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5079 bytes
"""
Example Airflow DAG for Google Cloud Natural Language service
"""
from google.cloud.language_v1.proto.language_service_pb2 import Document
import airflow
from airflow import models
from airflow.contrib.operators.gcp_natural_language_operator import CloudLanguageAnalyzeEntitiesOperator, CloudLanguageAnalyzeEntitySentimentOperator, CloudLanguageAnalyzeSentimentOperator, CloudLanguageClassifyTextOperator
from airflow.operators.bash_operator import BashOperator
TEXT = '\nAirflow is a platform to programmatically author, schedule and monitor workflows.\n\nUse Airflow to author workflows as Directed Acyclic Graphs (DAGs) of tasks. The Airflow scheduler executes\n your tasks on an array of workers while following the specified dependencies. Rich command line utilities\n make performing complex surgeries on DAGs a snap. The rich user interface makes it easy to visualize\n pipelines running in production, monitor progress, and troubleshoot issues when needed.\n'
document = Document(content=TEXT, type='PLAIN_TEXT')
GCS_CONTENT_URI = 'gs://my-text-bucket/sentiment-me.txt'
document_gcs = Document(gcs_content_uri=GCS_CONTENT_URI, type='PLAIN_TEXT')
default_args = {'start_date': airflow.utils.dates.days_ago(1)}
with models.DAG('example_gcp_natural_language',
  default_args=default_args,
  schedule_interval=None) as (dag):
    analyze_entities = CloudLanguageAnalyzeEntitiesOperator(document=document, task_id='analyze_entities')
    analyze_entities_result = BashOperator(bash_command='echo "{{ task_instance.xcom_pull(\'analyze_entities\') }}"',
      task_id='analyze_entities_result')
    analyze_entity_sentiment = CloudLanguageAnalyzeEntitySentimentOperator(document=document,
      task_id='analyze_entity_sentiment')
    analyze_entity_sentiment_result = BashOperator(bash_command='echo "{{ task_instance.xcom_pull(\'analyze_entity_sentiment\') }}"',
      task_id='analyze_entity_sentiment_result')
    analyze_sentiment = CloudLanguageAnalyzeSentimentOperator(document=document, task_id='analyze_sentiment')
    analyze_sentiment_result = BashOperator(bash_command='echo "{{ task_instance.xcom_pull(\'analyze_sentiment\') }}"',
      task_id='analyze_sentiment_result')
    analyze_classify_text = CloudLanguageClassifyTextOperator(document=document,
      task_id='analyze_classify_text')
    analyze_classify_text_result = BashOperator(bash_command='echo "{{ task_instance.xcom_pull(\'analyze_classify_text\') }}"',
      task_id='analyze_classify_text_result')
    analyze_entities >> analyze_entities_result
    analyze_entity_sentiment >> analyze_entity_sentiment_result
    analyze_sentiment >> analyze_sentiment_result
    analyze_classify_text >> analyze_classify_text_result