# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/azure_cosmos_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2893 bytes
from airflow.contrib.hooks.azure_cosmos_hook import AzureCosmosDBHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class AzureCosmosDocumentSensor(BaseSensorOperator):
    """AzureCosmosDocumentSensor"""
    template_fields = ('database_name', 'collection_name', 'document_id')

    @apply_defaults
    def __init__(self, database_name, collection_name, document_id, azure_cosmos_conn_id='azure_cosmos_default', *args, **kwargs):
        """
        Create a new AzureCosmosDocumentSensor

        :param database_name: Target CosmosDB database_name.
        :type database_name: str
        :param collection_name: Target CosmosDB collection_name.
        :type collection_name: str
        :param document_id: The ID of the target document.
        :type query: str
        :param azure_cosmos_conn_id: Reference to the Azure CosmosDB connection.
        :type azure_cosmos_conn_id: str
        """
        (super(AzureCosmosDocumentSensor, self).__init__)(*args, **kwargs)
        self.azure_cosmos_conn_id = azure_cosmos_conn_id
        self.database_name = database_name
        self.collection_name = collection_name
        self.document_id = document_id

    def poke(self, context):
        self.log.info('*** Intering poke')
        hook = AzureCosmosDBHook(self.azure_cosmos_conn_id)
        return hook.get_document(self.document_id, self.database_name, self.collection_name) is not None