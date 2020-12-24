# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mongodb_model\myMongodb.py
# Compiled at: 2019-10-21 22:26:07
# Size of source mod 2**32: 2732 bytes
import pymongo as pm
from retrying import retry
import log_model

class myMongodb:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.myclient = None
        self.mongodb_log = None

    @retry(stop_max_attempt_number=3)
    def conn_Mongodb(self, log_name, level, file_path):
        self.mongodb_log = log_model.getLogger(log_name, level=level, file=file_path)
        try:
            self.myclient.ping()
        except:
            self.myclient = pm.MongoClient(host=(self.host), port=(self.port))

        return self.myclient

    def insert_one(self, database, table, data):
        try:
            mongo_db = self.myclient[database]
            ret = mongo_db[table].insert_one(data)
            return ret.inserted_id
        except Exception as err:
            self.mongodb_log.error(err)
            return ''

    def insert_many(self, database, table, data_list):
        try:
            mongo_db = self.myclient[database]
            ret = mongo_db[table].insert_many(data_list)
            return ret.inserted_ids
        except Exception as err:
            self.mongodb_log.error(err)
            return ''

    def update_many(self, database, table, data):
        data_filter = {}
        data_revised = {}
        for key in data.keys():
            data_filter[key] = data[key][0]
            data_revised[key] = data[key][1]

        try:
            mongo_db = self.myclient[database]
            return mongo_db[table].update_many(data_filter, {'$set': data_revised}).modified_count
        except Exception as err:
            self.mongodb_log.error(err)
            return ''

    def update_many_condition(self, database, table, query, update):
        try:
            mongo_db = self.myclient[database]
            return mongo_db[table].update_many(query, update, upsert=True)
        except Exception as err:
            self.mongodb_log.error(err)
            return ''

    def select(self, database, table, condition, column=None):
        try:
            mongo_db = self.myclient[database]
            if column is None:
                return mongo_db[table].find(condition)
            else:
                return mongo_db[table].find(condition, column)
        except Exception as err:
            self.mongodb_log.error(err)
            return ''

    def delete(self, database, table, condition):
        try:
            mongo_db = self.myclient[database]
            return mongo_db[table].delete_many(filter=condition).deleted_count
        except Exception as err:
            self.mongodb_log.error(err)
            return ''