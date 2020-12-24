# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/file_to_wasb.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2513 bytes
from airflow.contrib.hooks.wasb_hook import WasbHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class FileToWasbOperator(BaseOperator):
    """FileToWasbOperator"""
    template_fields = ('file_path', 'container_name', 'blob_name')

    @apply_defaults
    def __init__(self, file_path, container_name, blob_name, wasb_conn_id='wasb_default', load_options=None, *args, **kwargs):
        (super(FileToWasbOperator, self).__init__)(*args, **kwargs)
        if load_options is None:
            load_options = {}
        self.file_path = file_path
        self.container_name = container_name
        self.blob_name = blob_name
        self.wasb_conn_id = wasb_conn_id
        self.load_options = load_options

    def execute(self, context):
        """Upload a file to Azure Blob Storage."""
        hook = WasbHook(wasb_conn_id=(self.wasb_conn_id))
        self.log.info('Uploading %s to wasb://%s as %s'.format(self.file_path, self.container_name, self.blob_name))
        (hook.load_file)((self.file_path), (self.container_name), 
         (self.blob_name), **self.load_options)