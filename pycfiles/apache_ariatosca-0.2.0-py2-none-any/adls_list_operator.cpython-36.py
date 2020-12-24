# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/adls_list_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2598 bytes
from typing import Iterable
from airflow.contrib.hooks.azure_data_lake_hook import AzureDataLakeHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class AzureDataLakeStorageListOperator(BaseOperator):
    """AzureDataLakeStorageListOperator"""
    template_fields = ('path', )
    ui_color = '#901dd2'

    @apply_defaults
    def __init__(self, path, azure_data_lake_conn_id='azure_data_lake_default', *args, **kwargs):
        (super(AzureDataLakeStorageListOperator, self).__init__)(*args, **kwargs)
        self.path = path
        self.azure_data_lake_conn_id = azure_data_lake_conn_id

    def execute(self, context):
        hook = AzureDataLakeHook(azure_data_lake_conn_id=(self.azure_data_lake_conn_id))
        self.log.info('Getting list of ADLS files in path: %s', self.path)
        return hook.list(path=(self.path))