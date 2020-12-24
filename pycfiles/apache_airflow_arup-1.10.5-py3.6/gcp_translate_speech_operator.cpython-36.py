# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = "\n    Recognizes speech in audio input and translates it.\n\n    Note that it uses the first result from the recognition api response - the one with the highest confidence\n    In order to see other possible results please use\n    :ref:`howto/operator:GcpSpeechToTextRecognizeSpeechOperator`\n    and\n    :ref:`howto/operator:CloudTranslateTextOperator`\n    separately\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:GcpTranslateSpeechOperator`\n\n    See https://cloud.google.com/translate/docs/translating-text\n\n    Execute method returns string object with the translation\n\n    This is a list of dictionaries queried value.\n    Dictionary typically contains three keys (though not\n    all will be present in all cases).\n\n    * ``detectedSourceLanguage``: The detected language (as an\n      ISO 639-1 language code) of the text.\n    * ``translatedText``: The translation of the text into the\n      target language.\n    * ``input``: The corresponding input value.\n    * ``model``: The model used to translate the text.\n\n    Dictionary is set as XCom return value.\n\n    :param audio: audio data to be recognized. See more:\n        https://googleapis.github.io/google-cloud-python/latest/speech/gapic/v1/types.html#google.cloud.speech_v1.types.RecognitionAudio\n    :type audio: dict or google.cloud.speech_v1.types.RecognitionAudio\n\n    :param config: information to the recognizer that specifies how to process the request. See more:\n        https://googleapis.github.io/google-cloud-python/latest/speech/gapic/v1/types.html#google.cloud.speech_v1.types.RecognitionConfig\n    :type config: dict or google.cloud.speech_v1.types.RecognitionConfig\n\n    :param target_language: The language to translate results into. This is required by the API and defaults\n        to the target language of the current instance.\n        Check the list of available languages here: https://cloud.google.com/translate/docs/languages\n    :type target_language: str\n\n    :param format_: (Optional) One of ``text`` or ``html``, to specify\n        if the input text is plain text or HTML.\n    :type format_: str or None\n\n    :param source_language: (Optional) The language of the text to\n        be translated.\n    :type source_language: str or None\n\n    :param model: (Optional) The model used to translate the text, such\n        as ``'base'`` or ``'nmt'``.\n    :type model: str or None\n\n    :param project_id: Optional, Google Cloud Platform Project ID where the Compute\n        Engine Instance exists.  If set to None or missing, the default project_id from the GCP connection is\n        used.\n    :type project_id: str\n\n    :param gcp_conn_id: Optional, The connection ID used to connect to Google Cloud\n        Platform. Defaults to 'google_cloud_default'.\n    :type gcp_conn_id: str\n\n    "
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