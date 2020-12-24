# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_video_intelligence_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 11742 bytes
"""
This module contains Google Cloud Vision operators.
"""
from google.protobuf.json_format import MessageToDict
from google.cloud.videointelligence_v1 import enums
from airflow.contrib.hooks.gcp_video_intelligence_hook import CloudVideoIntelligenceHook
from airflow.models import BaseOperator

class CloudVideoIntelligenceDetectVideoLabelsOperator(BaseOperator):
    __doc__ = '\n    Performs video annotation, annotating video labels.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVideoIntelligenceDetectVideoLabelsOperator`.\n\n    :param input_uri: Input video location. Currently, only Google Cloud Storage URIs are supported,\n        which must be specified in the following format: ``gs://bucket-id/object-id``.\n    :type input_uri: str\n    :param input_content: The video data bytes.\n        If unset, the input video(s) should be specified via ``input_uri``.\n        If set, ``input_uri`` should be unset.\n    :type input_content: bytes\n    :param output_uri: Optional, location where the output (in JSON format) should be stored. Currently, only\n        Google Cloud Storage URIs are supported, which must be specified in the following format:\n        ``gs://bucket-id/object-id``.\n    :type output_uri: str\n    :param video_context: Optional, Additional video context and/or feature-specific parameters.\n    :type video_context: dict or google.cloud.videointelligence_v1.types.VideoContext\n    :param location: Optional, cloud region where annotation should take place. Supported cloud regions:\n        us-east1, us-west1, europe-west1, asia-east1. If no region is specified, a region will be determined\n        based on video file location.\n    :type location: str\n    :param retry: Retry object used to determine when/if to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: Optional, The amount of time, in seconds, to wait for the request to complete.\n        Note that if retry is specified, the timeout applies to each individual attempt.\n    :type timeout: float\n    :param gcp_conn_id: Optional, The connection ID used to connect to Google Cloud\n        Platform. Defaults to ``google_cloud_default``.\n    :type gcp_conn_id: str\n    '
    template_fields = ('input_uri', 'output_uri', 'gcp_conn_id')

    def __init__(self, input_uri, input_content=None, output_uri=None, video_context=None, location=None, retry=None, timeout=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVideoIntelligenceDetectVideoLabelsOperator, self).__init__)(*args, **kwargs)
        self.input_uri = input_uri
        self.input_content = input_content
        self.output_uri = output_uri
        self.video_context = video_context
        self.location = location
        self.retry = retry
        self.gcp_conn_id = gcp_conn_id
        self.timeout = timeout

    def execute(self, context):
        hook = CloudVideoIntelligenceHook(gcp_conn_id=(self.gcp_conn_id))
        operation = hook.annotate_video(input_uri=(self.input_uri),
          input_content=(self.input_content),
          video_context=(self.video_context),
          location=(self.location),
          retry=(self.retry),
          features=[
         enums.Feature.LABEL_DETECTION],
          timeout=(self.timeout))
        self.log.info('Processing video for label annotations')
        result = MessageToDict(operation.result())
        self.log.info('Finished processing.')
        return result


class CloudVideoIntelligenceDetectVideoExplicitContentOperator(BaseOperator):
    __doc__ = '\n    Performs video annotation, annotating explicit content.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVideoIntelligenceDetectVideoExplicitContentOperator`\n\n    :param input_uri: Input video location. Currently, only Google Cloud Storage URIs are supported,\n        which must be specified in the following format: ``gs://bucket-id/object-id``.\n    :type input_uri: str\n    :param input_content: The video data bytes.\n        If unset, the input video(s) should be specified via ``input_uri``.\n        If set, ``input_uri`` should be unset.\n    :type input_content: bytes\n    :param output_uri: Optional, location where the output (in JSON format) should be stored. Currently, only\n        Google Cloud Storage URIs are supported, which must be specified in the following format:\n        ``gs://bucket-id/object-id``.\n    :type output_uri: str\n    :param video_context: Optional, Additional video context and/or feature-specific parameters.\n    :type video_context: dict or google.cloud.videointelligence_v1.types.VideoContext\n    :param location: Optional, cloud region where annotation should take place. Supported cloud regions:\n        us-east1, us-west1, europe-west1, asia-east1. If no region is specified, a region will be determined\n        based on video file location.\n    :type location: str\n    :param retry: Retry object used to determine when/if to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: Optional, The amount of time, in seconds, to wait for the request to complete.\n        Note that if retry is specified, the timeout applies to each individual attempt.\n    :type timeout: float\n    :param gcp_conn_id: Optional, The connection ID used to connect to Google Cloud\n        Platform. Defaults to ``google_cloud_default``.\n    :type gcp_conn_id: str\n    '
    template_fields = ('input_uri', 'output_uri', 'gcp_conn_id')

    def __init__(self, input_uri, output_uri=None, input_content=None, video_context=None, location=None, retry=None, timeout=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVideoIntelligenceDetectVideoExplicitContentOperator, self).__init__)(*args, **kwargs)
        self.input_uri = input_uri
        self.output_uri = output_uri
        self.input_content = input_content
        self.video_context = video_context
        self.location = location
        self.retry = retry
        self.gcp_conn_id = gcp_conn_id
        self.timeout = timeout

    def execute(self, context):
        hook = CloudVideoIntelligenceHook(gcp_conn_id=(self.gcp_conn_id))
        operation = hook.annotate_video(input_uri=(self.input_uri),
          input_content=(self.input_content),
          video_context=(self.video_context),
          location=(self.location),
          retry=(self.retry),
          features=[
         enums.Feature.EXPLICIT_CONTENT_DETECTION],
          timeout=(self.timeout))
        self.log.info('Processing video for explicit content annotations')
        result = MessageToDict(operation.result())
        self.log.info('Finished processing.')
        return result


class CloudVideoIntelligenceDetectVideoShotsOperator(BaseOperator):
    __doc__ = '\n    Performs video annotation, annotating video shots.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVideoIntelligenceDetectVideoShotsOperator`\n\n    :param input_uri: Input video location. Currently, only Google Cloud Storage URIs are supported,\n        which must be specified in the following format: ``gs://bucket-id/object-id``.\n    :type input_uri: str\n    :param input_content: The video data bytes.\n        If unset, the input video(s) should be specified via ``input_uri``.\n        If set, ``input_uri`` should be unset.\n    :type input_content: bytes\n    :param output_uri: Optional, location where the output (in JSON format) should be stored. Currently, only\n        Google Cloud Storage URIs are supported, which must be specified in the following format:\n        ``gs://bucket-id/object-id``.\n    :type output_uri: str\n    :param video_context: Optional, Additional video context and/or feature-specific parameters.\n    :type video_context: dict or google.cloud.videointelligence_v1.types.VideoContext\n    :param location: Optional, cloud region where annotation should take place. Supported cloud regions:\n        us-east1, us-west1, europe-west1, asia-east1. If no region is specified, a region will be determined\n        based on video file location.\n    :type location: str\n    :param retry: Retry object used to determine when/if to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: Optional, The amount of time, in seconds, to wait for the request to complete.\n        Note that if retry is specified, the timeout applies to each individual attempt.\n    :type timeout: float\n    :param gcp_conn_id: Optional, The connection ID used to connect to Google Cloud\n        Platform. Defaults to ``google_cloud_default``.\n    :type gcp_conn_id: str\n    '
    template_fields = ('input_uri', 'output_uri', 'gcp_conn_id')

    def __init__(self, input_uri, output_uri=None, input_content=None, video_context=None, location=None, retry=None, timeout=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVideoIntelligenceDetectVideoShotsOperator, self).__init__)(*args, **kwargs)
        self.input_uri = input_uri
        self.output_uri = output_uri
        self.input_content = input_content
        self.video_context = video_context
        self.location = location
        self.retry = retry
        self.gcp_conn_id = gcp_conn_id
        self.timeout = timeout

    def execute(self, context):
        hook = CloudVideoIntelligenceHook(gcp_conn_id=(self.gcp_conn_id))
        operation = hook.annotate_video(input_uri=(self.input_uri),
          input_content=(self.input_content),
          video_context=(self.video_context),
          location=(self.location),
          retry=(self.retry),
          features=[
         enums.Feature.SHOT_CHANGE_DETECTION],
          timeout=(self.timeout))
        self.log.info('Processing video for video shots annotations')
        result = MessageToDict(operation.result())
        self.log.info('Finished processing.')
        return result