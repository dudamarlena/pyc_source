# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/azure_cosmos_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 10421 bytes
import azure.cosmos.cosmos_client as cosmos_client
from azure.cosmos.errors import HTTPFailure
import uuid
from airflow.exceptions import AirflowBadRequest
from airflow.hooks.base_hook import BaseHook

class AzureCosmosDBHook(BaseHook):
    """AzureCosmosDBHook"""

    def __init__(self, azure_cosmos_conn_id='azure_cosmos_default'):
        self.conn_id = azure_cosmos_conn_id
        self.connection = self.get_connection(self.conn_id)
        self.extras = self.connection.extra_dejson
        self.endpoint_uri = self.connection.login
        self.master_key = self.connection.password
        self.default_database_name = self.extras.get('database_name')
        self.default_collection_name = self.extras.get('collection_name')
        self.cosmos_client = None

    def get_conn(self):
        """
        Return a cosmos db client.
        """
        if self.cosmos_client is not None:
            return self.cosmos_client
        else:
            self.cosmos_client = cosmos_client.CosmosClient(self.endpoint_uri, {'masterKey': self.master_key})
            return self.cosmos_client

    def __get_database_name(self, database_name=None):
        db_name = database_name
        if db_name is None:
            db_name = self.default_database_name
        if db_name is None:
            raise AirflowBadRequest('Database name must be specified')
        return db_name

    def __get_collection_name(self, collection_name=None):
        coll_name = collection_name
        if coll_name is None:
            coll_name = self.default_collection_name
        if coll_name is None:
            raise AirflowBadRequest('Collection name must be specified')
        return coll_name

    def does_collection_exist(self, collection_name, database_name=None):
        """
        Checks if a collection exists in CosmosDB.
        """
        if collection_name is None:
            raise AirflowBadRequest('Collection name cannot be None.')
        existing_container = list(self.get_conn().QueryContainers(get_database_link(self._AzureCosmosDBHook__get_database_name(database_name)), {'query':'SELECT * FROM r WHERE r.id=@id', 
         'parameters':[
          {'name':'@id', 
           'value':collection_name}]}))
        if len(existing_container) == 0:
            return False
        else:
            return True

    def create_collection(self, collection_name, database_name=None):
        """
        Creates a new collection in the CosmosDB database.
        """
        if collection_name is None:
            raise AirflowBadRequest('Collection name cannot be None.')
        existing_container = list(self.get_conn().QueryContainers(get_database_link(self._AzureCosmosDBHook__get_database_name(database_name)), {'query':'SELECT * FROM r WHERE r.id=@id', 
         'parameters':[
          {'name':'@id', 
           'value':collection_name}]}))
        if len(existing_container) == 0:
            self.get_conn().CreateContainer(get_database_link(self._AzureCosmosDBHook__get_database_name(database_name)), {'id': collection_name})

    def does_database_exist(self, database_name):
        """
        Checks if a database exists in CosmosDB.
        """
        if database_name is None:
            raise AirflowBadRequest('Database name cannot be None.')
        existing_database = list(self.get_conn().QueryDatabases({'query':'SELECT * FROM r WHERE r.id=@id', 
         'parameters':[
          {'name':'@id', 
           'value':database_name}]}))
        if len(existing_database) == 0:
            return False
        else:
            return True

    def create_database(self, database_name):
        """
        Creates a new database in CosmosDB.
        """
        if database_name is None:
            raise AirflowBadRequest('Database name cannot be None.')
        existing_database = list(self.get_conn().QueryDatabases({'query':'SELECT * FROM r WHERE r.id=@id', 
         'parameters':[
          {'name':'@id', 
           'value':database_name}]}))
        if len(existing_database) == 0:
            self.get_conn().CreateDatabase({'id': database_name})

    def delete_database(self, database_name):
        """
        Deletes an existing database in CosmosDB.
        """
        if database_name is None:
            raise AirflowBadRequest('Database name cannot be None.')
        self.get_conn().DeleteDatabase(get_database_link(database_name))

    def delete_collection(self, collection_name, database_name=None):
        """
        Deletes an existing collection in the CosmosDB database.
        """
        if collection_name is None:
            raise AirflowBadRequest('Collection name cannot be None.')
        self.get_conn().DeleteContainer(get_collection_link(self._AzureCosmosDBHook__get_database_name(database_name), collection_name))

    def upsert_document(self, document, database_name=None, collection_name=None, document_id=None):
        """
        Inserts a new document (or updates an existing one) into an existing
        collection in the CosmosDB database.
        """
        if document_id is None:
            document_id = str(uuid.uuid4())
        elif document is None:
            raise AirflowBadRequest('You cannot insert a None document')
        else:
            if 'id' in document:
                if document['id'] is None:
                    document['id'] = document_id
            else:
                document['id'] = document_id
        created_document = self.get_conn().CreateItem(get_collection_link(self._AzureCosmosDBHook__get_database_name(database_name), self._AzureCosmosDBHook__get_collection_name(collection_name)), document)
        return created_document

    def insert_documents(self, documents, database_name=None, collection_name=None):
        """
        Insert a list of new documents into an existing collection in the CosmosDB database.
        """
        if documents is None:
            raise AirflowBadRequest('You cannot insert empty documents')
        created_documents = []
        for single_document in documents:
            created_documents.append(self.get_conn().CreateItem(get_collection_link(self._AzureCosmosDBHook__get_database_name(database_name), self._AzureCosmosDBHook__get_collection_name(collection_name)), single_document))

        return created_documents

    def delete_document(self, document_id, database_name=None, collection_name=None):
        """
        Delete an existing document out of a collection in the CosmosDB database.
        """
        if document_id is None:
            raise AirflowBadRequest('Cannot delete a document without an id')
        self.get_conn().DeleteItem(get_document_link(self._AzureCosmosDBHook__get_database_name(database_name), self._AzureCosmosDBHook__get_collection_name(collection_name), document_id))

    def get_document(self, document_id, database_name=None, collection_name=None):
        """
        Get a document from an existing collection in the CosmosDB database.
        """
        if document_id is None:
            raise AirflowBadRequest('Cannot get a document without an id')
        try:
            return self.get_conn().ReadItem(get_document_link(self._AzureCosmosDBHook__get_database_name(database_name), self._AzureCosmosDBHook__get_collection_name(collection_name), document_id))
        except HTTPFailure:
            return

    def get_documents(self, sql_string, database_name=None, collection_name=None, partition_key=None):
        """
        Get a list of documents from an existing collection in the CosmosDB database via SQL query.
        """
        if sql_string is None:
            raise AirflowBadRequest('SQL query string cannot be None')
        query = {'query': sql_string}
        try:
            result_iterable = self.get_conn().QueryItems(get_collection_link(self._AzureCosmosDBHook__get_database_name(database_name), self._AzureCosmosDBHook__get_collection_name(collection_name)), query, partition_key)
            return list(result_iterable)
        except HTTPFailure:
            return


def get_database_link(database_id):
    return 'dbs/' + database_id


def get_collection_link(database_id, collection_id):
    return get_database_link(database_id) + '/colls/' + collection_id


def get_document_link(database_id, collection_id, document_id):
    return get_collection_link(database_id, collection_id) + '/docs/' + document_id