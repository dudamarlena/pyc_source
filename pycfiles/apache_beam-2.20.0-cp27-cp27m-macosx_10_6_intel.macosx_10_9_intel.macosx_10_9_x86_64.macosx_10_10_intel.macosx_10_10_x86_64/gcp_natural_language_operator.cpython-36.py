# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_natural_language_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 10313 bytes
from google.protobuf.json_format import MessageToDict
from airflow.contrib.hooks.gcp_natural_language_hook import CloudNaturalLanguageHook
from airflow.models import BaseOperator

class CloudLanguageAnalyzeEntitiesOperator(BaseOperator):
    """CloudLanguageAnalyzeEntitiesOperator"""
    template_fields = ('document', 'gcp_conn_id')

    def __init__(self, document, encoding_type=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudLanguageAnalyzeEntitiesOperator, self).__init__)(*args, **kwargs)
        self.document = document
        self.encoding_type = encoding_type
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudNaturalLanguageHook(gcp_conn_id=(self.gcp_conn_id))
        self.log.info('Start analyzing entities')
        response = hook.analyze_entities(document=(self.document),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))
        self.log.info('Finished analyzing entities')
        return MessageToDict(response)


class CloudLanguageAnalyzeEntitySentimentOperator(BaseOperator):
    """CloudLanguageAnalyzeEntitySentimentOperator"""
    template_fields = ('document', 'gcp_conn_id')

    def __init__(self, document, encoding_type=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudLanguageAnalyzeEntitySentimentOperator, self).__init__)(*args, **kwargs)
        self.document = document
        self.encoding_type = encoding_type
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudNaturalLanguageHook(gcp_conn_id=(self.gcp_conn_id))
        self.log.info('Start entity sentiment analyze')
        response = hook.analyze_entity_sentiment(document=(self.document),
          encoding_type=(self.encoding_type),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))
        self.log.info('Finished entity sentiment analyze')
        return MessageToDict(response)


class CloudLanguageAnalyzeSentimentOperator(BaseOperator):
    """CloudLanguageAnalyzeSentimentOperator"""
    template_fields = ('document', 'gcp_conn_id')

    def __init__(self, document, encoding_type=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudLanguageAnalyzeSentimentOperator, self).__init__)(*args, **kwargs)
        self.document = document
        self.encoding_type = encoding_type
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudNaturalLanguageHook(gcp_conn_id=(self.gcp_conn_id))
        self.log.info('Start sentiment analyze')
        response = hook.analyze_sentiment(document=(self.document),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))
        self.log.info('Finished sentiment analyze')
        return MessageToDict(response)


class CloudLanguageClassifyTextOperator(BaseOperator):
    """CloudLanguageClassifyTextOperator"""
    template_fields = ('document', 'gcp_conn_id')

    def __init__(self, document, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudLanguageClassifyTextOperator, self).__init__)(*args, **kwargs)
        self.document = document
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudNaturalLanguageHook(gcp_conn_id=(self.gcp_conn_id))
        self.log.info('Start text classify')
        response = hook.classify_text(document=(self.document),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))
        self.log.info('Finished text classify')
        return MessageToDict(response)