# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_translate_speech_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6388 bytes
from google.protobuf.json_format import MessageToDict
from airflow import AirflowException
from airflow.contrib.hooks.gcp_speech_to_text_hook import GCPSpeechToTextHook
from airflow.contrib.hooks.gcp_translate_hook import CloudTranslateHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class GcpTranslateSpeechOperator(BaseOperator):
    """GcpTranslateSpeechOperator"""
    template_fields = ('target_language', 'format_', 'source_language', 'model', 'project_id',
                       'gcp_conn_id')

    @apply_defaults
    def __init__(self, audio, config, target_language, format_, source_language, model, project_id=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(GcpTranslateSpeechOperator, self).__init__)(*args, **kwargs)
        self.audio = audio
        self.config = config
        self.target_language = target_language
        self.format_ = format_
        self.source_language = source_language
        self.model = model
        self.project_id = project_id
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        _speech_to_text_hook = GCPSpeechToTextHook(gcp_conn_id=(self.gcp_conn_id))
        _translate_hook = CloudTranslateHook(gcp_conn_id=(self.gcp_conn_id))
        recognize_result = _speech_to_text_hook.recognize_speech(config=(self.config),
          audio=(self.audio))
        recognize_dict = MessageToDict(recognize_result)
        self.log.info('recognition operation finished', recognize_dict)
        if len(recognize_dict['results']) == 0:
            self.log.info('No recognition results')
            return {}
        self.log.debug('recognition result: %s', recognize_dict)
        try:
            transcript = recognize_dict['results'][0]['alternatives'][0]['transcript']
        except KeyError as key:
            raise AirflowException("Wrong response '{}' returned - it should contain {} field".format(recognize_dict, key))

        try:
            translation = _translate_hook.translate(values=transcript,
              target_language=(self.target_language),
              format_=(self.format_),
              source_language=(self.source_language),
              model=(self.model))
            self.log.info('translated output: %s', translation)
            return translation
        except ValueError as e:
            self.log.error('An error has been thrown from translate speech method:')
            self.log.error(e)
            raise AirflowException(e)