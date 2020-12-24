# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qoaladep/gcp/datastore/datastore.py
# Compiled at: 2020-03-10 05:49:04
# Size of source mod 2**32: 2964 bytes
from datetime import datetime
from google.cloud import datastore

class DataStore(Object):

    def __init__(self, namespace_project):
        """[Init function]
        
        Arguments:
            namespace_project {[string]} -- [Namespace project in Datastore]
        """
        self.datastore_client = datastore.Client(namespace=namespace_project)

    def create_entity(self, kind, entity_id, entity_data):
        """[Creating new entity data in Datastore]
        
        Arguments:
            kind {[string]} -- [Table name in Datastore]
            entity_id {[string]} -- [Key for entity]
            entity_data {[dict]} -- [Dictionary of entity]
        """
        try:
            with self.datastore_client.transaction():
                entity = datastore.Entity(key=(self.datastore_client.key(kind, entity_id)))
                entity_data['created_at'] = str(datetime.utcnow())
                entity_data['updated_at'] = str(datetime.utcnow())
                entity.update(entity_data)
                self.datastore_client.put(entity)
        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e

    def get_entity_by_id(self, kind, entity_id):
        """[Get entity from table by id]
        
        Arguments:
            kind {[string]} -- [Table name in Datastore]
            entity_id {[string]} -- [Key for entity]
        
        Returns:
            entity[dict] -- [Dictionary of entity data]
        """
        try:
            key_entity = self.datastore_client.key(kind, entity_id)
            entity = self.datastore_client.get(key_entity)
            entity = dict(entity)
            return entity
        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e

    def update_properties_by_id(self, kind, entity_id, properties_name, properties_value):
        """[Update entity properties in Datastore]
        
        Arguments:
            kind {[string]} -- [Table name in Datastore]
            entity_id {[string]} -- [Key for entity]
            properties_name {[string]} -- [Name of entity column in Datastore]
            properties_value {[string]} -- [Value of entity column in Datastore]
        """
        try:
            key_entity = self.datastore_client.key(kind, entity_id)
            entity = self.datastore_client.get(key_entity)
            entity[properties_name] = properties_value
            entity['updated_at'] = str(datetime.utcnow())
            self.datastore_client.put(entity)
        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e

    def delete_entity(self, kind, entity_id):
        """[Delete entity in Datastore]
        
        Arguments:
            kind {[string]} -- [Table name in Datastore]
            entity_id {[string]} -- [Key for entity]
        """
        try:
            key_entity = self.datastore_client.key(kind, entity_id)
            entity = self.datastore_client.delete(key_entity)
        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e