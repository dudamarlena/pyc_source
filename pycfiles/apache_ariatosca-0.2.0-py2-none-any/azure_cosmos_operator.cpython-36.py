# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/azure_cosmos_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2803 bytes
from airflow.contrib.hooks.azure_cosmos_hook import AzureCosmosDBHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class AzureCosmosInsertDocumentOperator(BaseOperator):
    """AzureCosmosInsertDocumentOperator"""
    template_fields = ('database_name', 'collection_name')
    ui_color = '#e4f0e8'

    @apply_defaults
    def __init__(self, database_name, collection_name, document, azure_cosmos_conn_id='azure_cosmos_default', *args, **kwargs):
        (super(AzureCosmosInsertDocumentOperator, self).__init__)(*args, **kwargs)
        self.database_name = database_name
        self.collection_name = collection_name
        self.document = document
        self.azure_cosmos_conn_id = azure_cosmos_conn_id

    def execute(self, context):
        hook = AzureCosmosDBHook(azure_cosmos_conn_id=(self.azure_cosmos_conn_id))
        if not hook.does_database_exist(self.database_name):
            hook.create_database(self.database_name)
        if not hook.does_collection_exist(self.collection_name, self.database_name):
            hook.create_collection(self.collection_name, self.database_name)
        hook.upsert_document(self.document, self.database_name, self.collection_name)