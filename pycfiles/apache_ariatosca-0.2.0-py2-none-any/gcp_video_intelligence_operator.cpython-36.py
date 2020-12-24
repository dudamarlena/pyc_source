# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_video_intelligence_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 11742 bytes
__doc__ = '\nThis module contains Google Cloud Vision operators.\n'
from google.protobuf.json_format import MessageToDict
from google.cloud.videointelligence_v1 import enums
from airflow.contrib.hooks.gcp_video_intelligence_hook import CloudVideoIntelligenceHook
from airflow.models import BaseOperator

class CloudVideoIntelligenceDetectVideoLabelsOperator(BaseOperator):
    """CloudVideoIntelligenceDetectVideoLabelsOperator"""
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
    """CloudVideoIntelligenceDetectVideoExplicitContentOperator"""
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
    """CloudVideoIntelligenceDetectVideoShotsOperator"""
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