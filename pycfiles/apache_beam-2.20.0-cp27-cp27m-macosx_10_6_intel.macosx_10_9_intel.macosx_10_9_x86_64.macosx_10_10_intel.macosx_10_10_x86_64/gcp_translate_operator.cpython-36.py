# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_translate_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4018 bytes
from airflow import AirflowException
from airflow.contrib.hooks.gcp_translate_hook import CloudTranslateHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CloudTranslateTextOperator(BaseOperator):
    """CloudTranslateTextOperator"""
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