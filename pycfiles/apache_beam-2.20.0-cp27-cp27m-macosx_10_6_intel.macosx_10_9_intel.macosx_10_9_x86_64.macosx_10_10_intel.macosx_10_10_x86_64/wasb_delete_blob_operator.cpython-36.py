# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/wasb_delete_blob_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2731 bytes
from airflow.contrib.hooks.wasb_hook import WasbHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class WasbDeleteBlobOperator(BaseOperator):
    """WasbDeleteBlobOperator"""
    template_fields = ('container_name', 'blob_name')

    @apply_defaults
    def __init__(self, container_name, blob_name, wasb_conn_id='wasb_default', check_options=None, is_prefix=False, ignore_if_missing=False, *args, **kwargs):
        (super(WasbDeleteBlobOperator, self).__init__)(*args, **kwargs)
        if check_options is None:
            check_options = {}
        self.wasb_conn_id = wasb_conn_id
        self.container_name = container_name
        self.blob_name = blob_name
        self.check_options = check_options
        self.is_prefix = is_prefix
        self.ignore_if_missing = ignore_if_missing

    def execute(self, context):
        self.log.info('Deleting blob: %s\nin wasb://%s', self.blob_name, self.container_name)
        hook = WasbHook(wasb_conn_id=(self.wasb_conn_id))
        (hook.delete_file)((self.container_name), (self.blob_name), 
         (self.is_prefix), (self.ignore_if_missing), **self.check_options)