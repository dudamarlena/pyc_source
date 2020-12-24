# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/gcp_natural_language_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 10686 bytes
from google.cloud.language_v1 import LanguageServiceClient
from airflow.contrib.hooks.gcp_api_base_hook import GoogleCloudBaseHook

class CloudNaturalLanguageHook(GoogleCloudBaseHook):
    """CloudNaturalLanguageHook"""
    _conn = None

    def __init__(self, gcp_conn_id='google_cloud_default', delegate_to=None):
        super(CloudNaturalLanguageHook, self).__init__(gcp_conn_id, delegate_to)

    def get_conn(self):
        """
        Retrieves connection to Cloud Natural Language service.

        :return: Cloud Natural Language service object
        :rtype: google.cloud.language_v1.LanguageServiceClient
        """
        if not self._conn:
            self._conn = LanguageServiceClient(credentials=(self._get_credentials()))
        return self._conn

    @GoogleCloudBaseHook.catch_http_exception
    def analyze_entities(self, document, encoding_type=None, retry=None, timeout=None, metadata=None):
        """
        Finds named entities in the text along with entity types,
        salience, mentions for each entity, and other properties.

        :param document: Input document.
            If a dict is provided, it must be of the same form as the protobuf message Document
        :type document: dict or class google.cloud.language_v1.types.Document
        :param encoding_type: The encoding type used by the API to calculate offsets.
        :type encoding_type: google.cloud.language_v1.types.EncodingType
        :param retry: A retry object used to retry requests. If None is specified, requests will not be
            retried.
        :type retry: google.api_core.retry.Retry
        :param timeout: The amount of time, in seconds, to wait for the request to complete. Note that if
            retry is specified, the timeout applies to each individual attempt.
        :type timeout: float
        :param metadata: Additional metadata that is provided to the method.
        :type metadata: sequence[tuple[str, str]]]
        :rtype: google.cloud.language_v1.types.AnalyzeEntitiesResponse
        """
        client = self.get_conn()
        return client.analyze_entities(document=document,
          encoding_type=encoding_type,
          retry=retry,
          timeout=timeout,
          metadata=metadata)

    @GoogleCloudBaseHook.catch_http_exception
    def analyze_entity_sentiment(self, document, encoding_type=None, retry=None, timeout=None, metadata=None):
        """
        Finds entities, similar to AnalyzeEntities in the text and analyzes sentiment associated with each
        entity and its mentions.

        :param document: Input document.
            If a dict is provided, it must be of the same form as the protobuf message Document
        :type document: dict or class google.cloud.language_v1.types.Document
        :param encoding_type: The encoding type used by the API to calculate offsets.
        :type encoding_type: google.cloud.language_v1.types.EncodingType
        :param retry: A retry object used to retry requests. If None is specified, requests will not be
            retried.
        :type retry: google.api_core.retry.Retry
        :param timeout: The amount of time, in seconds, to wait for the request to complete. Note that if
            retry is specified, the timeout applies to each individual attempt.
        :type timeout: float
        :param metadata: Additional metadata that is provided to the method.
        :type metadata: sequence[tuple[str, str]]]
        :rtype: google.cloud.language_v1.types.AnalyzeEntitiesResponse
        """
        client = self.get_conn()
        return client.analyze_entity_sentiment(document=document,
          encoding_type=encoding_type,
          retry=retry,
          timeout=timeout,
          metadata=metadata)

    @GoogleCloudBaseHook.catch_http_exception
    def analyze_sentiment(self, document, encoding_type=None, retry=None, timeout=None, metadata=None):
        """
        Analyzes the sentiment of the provided text.

        :param document: Input document.
            If a dict is provided, it must be of the same form as the protobuf message Document
        :type document: dict or class google.cloud.language_v1.types.Document
        :param encoding_type: The encoding type used by the API to calculate offsets.
        :type encoding_type: google.cloud.language_v1.types.EncodingType
        :param retry: A retry object used to retry requests. If None is specified, requests will not be
            retried.
        :type retry: google.api_core.retry.Retry
        :param timeout: The amount of time, in seconds, to wait for the request to complete. Note that if
            retry is specified, the timeout applies to each individual attempt.
        :type timeout: float
        :param metadata: Additional metadata that is provided to the method.
        :type metadata: sequence[tuple[str, str]]]
        :rtype: google.cloud.language_v1.types.AnalyzeEntitiesResponse
        """
        client = self.get_conn()
        return client.analyze_sentiment(document=document,
          encoding_type=encoding_type,
          retry=retry,
          timeout=timeout,
          metadata=metadata)

    @GoogleCloudBaseHook.catch_http_exception
    def analyze_syntax(self, document, encoding_type=None, retry=None, timeout=None, metadata=None):
        """
        Analyzes the syntax of the text and provides sentence boundaries and tokenization along with part
        of speech tags, dependency trees, and other properties.

        :param document: Input document.
            If a dict is provided, it must be of the same form as the protobuf message Document
        :type document: dict or class google.cloud.language_v1.types.Document#
        :param encoding_type: The encoding type used by the API to calculate offsets.
        :type encoding_type: google.cloud.language_v1.types.EncodingType
        :param retry: A retry object used to retry requests. If None is specified, requests will not be
            retried.
        :type retry: google.api_core.retry.Retry
        :param timeout: The amount of time, in seconds, to wait for the request to complete. Note that if
            retry is specified, the timeout applies to each individual attempt.
        :type timeout: float
        :param metadata: Additional metadata that is provided to the method.
        :type metadata: sequence[tuple[str, str]]]
        :rtype: google.cloud.language_v1.types.AnalyzeSyntaxResponse
        """
        client = self.get_conn()
        return client.analyze_syntax(document=document,
          encoding_type=encoding_type,
          retry=retry,
          timeout=timeout,
          metadata=metadata)

    @GoogleCloudBaseHook.catch_http_exception
    def annotate_text(self, document, features, encoding_type=None, retry=None, timeout=None, metadata=None):
        """
        A convenience method that provides all the features that analyzeSentiment,
        analyzeEntities, and analyzeSyntax provide in one call.

        :param document: Input document.
            If a dict is provided, it must be of the same form as the protobuf message Document
        :type document: dict or google.cloud.language_v1.types.Document
        :param features: The enabled features.
            If a dict is provided, it must be of the same form as the protobuf message Features
        :type features: dict or google.cloud.language_v1.enums.Features
        :param encoding_type: The encoding type used by the API to calculate offsets.
        :type encoding_type: google.cloud.language_v1.types.EncodingType
        :param retry: A retry object used to retry requests. If None is specified, requests will not be
            retried.
        :type retry: google.api_core.retry.Retry
        :param timeout: The amount of time, in seconds, to wait for the request to complete. Note that if
            retry is specified, the timeout applies to each individual attempt.
        :type timeout: float
        :param metadata: Additional metadata that is provided to the method.
        :type metadata: sequence[tuple[str, str]]]
        :rtype: google.cloud.language_v1.types.AnnotateTextResponse
        """
        client = self.get_conn()
        return client.annotate_text(document=document,
          features=features,
          encoding_type=encoding_type,
          retry=retry,
          timeout=timeout,
          metadata=metadata)

    @GoogleCloudBaseHook.catch_http_exception
    def classify_text(self, document, retry=None, timeout=None, metadata=None):
        """
        Classifies a document into categories.

        :param document: Input document.
            If a dict is provided, it must be of the same form as the protobuf message Document
        :type document: dict or class google.cloud.language_v1.types.Document
        :param retry: A retry object used to retry requests. If None is specified, requests will not be
            retried.
        :type retry: google.api_core.retry.Retry
        :param timeout: The amount of time, in seconds, to wait for the request to complete. Note that if
            retry is specified, the timeout applies to each individual attempt.
        :type timeout: float
        :param metadata: Additional metadata that is provided to the method.
        :type metadata: sequence[tuple[str, str]]]
        :rtype: google.cloud.language_v1.types.AnalyzeEntitiesResponse
        """
        client = self.get_conn()
        return client.classify_text(document=document, retry=retry, timeout=timeout, metadata=metadata)