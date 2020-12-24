# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_natural_language_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 10313 bytes
from google.protobuf.json_format import MessageToDict
from airflow.contrib.hooks.gcp_natural_language_hook import CloudNaturalLanguageHook
from airflow.models import BaseOperator

class CloudLanguageAnalyzeEntitiesOperator(BaseOperator):
    __doc__ = '\n    Finds named entities in the text along with entity types,\n    salience, mentions for each entity, and other properties.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudLanguageAnalyzeEntitiesOperator`\n\n    :param document: Input document.\n        If a dict is provided, it must be of the same form as the protobuf message Document\n    :type document: dict or google.cloud.language_v1.types.Document\n    :param encoding_type: The encoding type used by the API to calculate offsets.\n    :type encoding_type: google.cloud.language_v1.types.EncodingType\n    :param retry: A retry object used to retry requests. If None is specified, requests will not be\n        retried.\n    :param timeout: The amount of time, in seconds, to wait for the request to complete. Note that if\n        retry is specified, the timeout applies to each individual attempt.\n    :type timeout: float\n    :param metadata: Additional metadata that is provided to the method.\n    :type metadata: seq[tuple[str, str]]]\n    :param gcp_conn_id: The connection ID to use connecting to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
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
    __doc__ = '\n    Finds entities, similar to AnalyzeEntities in the text and analyzes sentiment associated with each\n    entity and its mentions.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudLanguageAnalyzeEntitySentimentOperator`\n\n    :param document: Input document.\n        If a dict is provided, it must be of the same form as the protobuf message Document\n    :type document: dict or google.cloud.language_v1.types.Document\n    :param encoding_type: The encoding type used by the API to calculate offsets.\n    :type encoding_type: google.cloud.language_v1.types.EncodingType\n    :param retry: A retry object used to retry requests. If None is specified, requests will not be\n        retried.\n    :param timeout: The amount of time, in seconds, to wait for the request to complete. Note that if\n        retry is specified, the timeout applies to each individual attempt.\n    :type timeout: float\n    :param metadata: Additional metadata that is provided to the method.\n    :type metadata: seq[tuple[str, str]]]\n    :rtype: google.cloud.language_v1.types.AnalyzeEntitiesResponse\n    :param gcp_conn_id: The connection ID to use connecting to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
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
    __doc__ = '\n    Analyzes the sentiment of the provided text.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudLanguageAnalyzeSentimentOperator`\n\n    :param document: Input document.\n        If a dict is provided, it must be of the same form as the protobuf message Document\n    :type document: dict or google.cloud.language_v1.types.Document\n    :param encoding_type: The encoding type used by the API to calculate offsets.\n    :type encoding_type: google.cloud.language_v1.types.EncodingType\n    :param retry: A retry object used to retry requests. If None is specified, requests will not be\n        retried.\n    :param timeout: The amount of time, in seconds, to wait for the request to complete. Note that if\n        retry is specified, the timeout applies to each individual attempt.\n    :type timeout: float\n    :param metadata: Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :rtype: google.cloud.language_v1.types.AnalyzeEntitiesResponse\n    :param gcp_conn_id: The connection ID to use connecting to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
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
    __doc__ = '\n    Classifies a document into categories.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudLanguageClassifyTextOperator`\n\n    :param document: Input document.\n        If a dict is provided, it must be of the same form as the protobuf message Document\n    :type document: dict or google.cloud.language_v1.types.Document\n    :param retry: A retry object used to retry requests. If None is specified, requests will not be\n        retried.\n    :param timeout: The amount of time, in seconds, to wait for the request to complete. Note that if\n        retry is specified, the timeout applies to each individual attempt.\n    :type timeout: float\n    :param metadata: Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: The connection ID to use connecting to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
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