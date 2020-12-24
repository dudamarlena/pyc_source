# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kalimaha/Development/git-repositories/Geobricks/pgeo/pgeo/metadata/db_metadata.py
# Compiled at: 2014-08-18 07:07:40
import pymongo
from pgeo.db.mongo import common
from pgeo.utils import log
log = log.logger(__name__)

class DBMetadata:

    def __init__(self, config):
        """
        @param config: config parameters to configure the metadata db
        @return:
        """
        self.config = config
        self.client = pymongo.MongoClient(config['connection'])
        self.database = config['database']
        self.document_layer = config['document']['layer']

    def insert_metadata(self, json):
        """
        Insert Layer Metadata in mongodb
        @param json: json data
        @return: id
        """
        return common.insert(self.client, self.database, self.document_layer, json)

    def remove_metadata(self, json):
        """
        Delete Layer Metadata in mongodb
        @param json: json data
        @return: id
        """
        return common.remove(self.client, self.database, self.document_layer, json)

    def remove_metadata_by_id(self, id):
        """
        Delete Layer Metadata in mongodb
        @param id: Metadata's id
        @return: id
        """
        return common.remove_by_id(self.client, self.database, self.document_layer, id)