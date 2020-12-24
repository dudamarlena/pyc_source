# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_translate_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4018 bytes
from airflow import AirflowException
from airflow.contrib.hooks.gcp_translate_hook import CloudTranslateHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CloudTranslateTextOperator(BaseOperator):
    __doc__ = "\n    Translate a string or list of strings.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudTranslateTextOperator`\n\n    See https://cloud.google.com/translate/docs/translating-text\n\n    Execute method returns str or list.\n\n    This is a list of dictionaries for each queried value. Each\n    dictionary typically contains three keys (though not\n    all will be present in all cases).\n\n    * ``detectedSourceLanguage``: The detected language (as an\n      ISO 639-1 language code) of the text.\n    * ``translatedText``: The translation of the text into the\n      target language.\n    * ``input``: The corresponding input value.\n    * ``model``: The model used to translate the text.\n\n    If only a single value is passed, then only a single\n    dictionary is set as XCom return value.\n\n    :type values: str or list\n    :param values: String or list of strings to translate.\n\n    :type target_language: str\n    :param target_language: The language to translate results into. This\n      is required by the API and defaults to\n      the target language of the current instance.\n\n    :type format_: str or None\n    :param format_: (Optional) One of ``text`` or ``html``, to specify\n      if the input text is plain text or HTML.\n\n    :type source_language: str or None\n    :param source_language: (Optional) The language of the text to\n      be translated.\n\n    :type model: str or None\n    :param model: (Optional) The model used to translate the text, such\n      as ``'base'`` or ``'nmt'``.\n\n    "
    template_fields = ('values', 'target_language', 'format_', 'source_language', 'model',
                       'gcp_conn_id')

    @apply_defaults
    def __init__(self, values, target_language, format_, source_language, model, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudTranslateTextOperator, self).__init__)(*args, **kwargs)
        self.values = values
        self.target_language = target_language
        self.format_ = format_
        self.source_language = source_language
        self.model = model
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        _hook = CloudTranslateHook(gcp_conn_id=(self.gcp_conn_id))
        try:
            translation = _hook.translate(values=(self.values),
              target_language=(self.target_language),
              format_=(self.format_),
              source_language=(self.source_language),
              model=(self.model))
            self.log.debug('Translation %s', translation)
            return translation
        except ValueError as e:
            self.log.error('An error has been thrown from translate method:')
            self.log.error(e)
            raise AirflowException(e)