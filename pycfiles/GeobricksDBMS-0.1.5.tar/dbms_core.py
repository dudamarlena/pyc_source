# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_dbms/geobricks_dbms/core/dbms_core.py
# Compiled at: 2014-12-01 03:18:15
from geobricks_dbms.core.dbms_mongodb import DBMSMongoDB
from geobricks_dbms.core.dbms_postgresql import DBMSPostgreSQL
from geobricks_dbms.config.dbms_config import config

class DBMS:
    vendor = None
    db_name = None
    username = None
    password = None
    collection_name = None
    datasource = None
    mongodb = None
    postgresql = None

    def __init__(self, vendor=None, db_name=None, datasource=None, username=None, password=None, collection_name=None):
        self.vendor = vendor
        self.db_name = db_name
        self.username = username
        self.password = password
        self.collection_name = collection_name
        self.datasource = datasource
        self.connect()

    def connect(self):
        if self.datasource is not None:
            default = config['default_datasource']
            self.vendor = default['vendor']
            if 'postgresql' in self.vendor:
                tmp = DBMSPostgreSQL(default['db_name'], default['username'], default['password'])
                sql = 'SELECT * FROM ' + default['table_name'] + " WHERE datasource = '" + self.datasource + "' "
                ds = tmp.query(sql)
                self.vendor = ds[0][2]
                if 'postgresql' in ds[0][2]:
                    self.postgresql = DBMSPostgreSQL(ds[0][3], ds[0][4], ds[0][5])
                elif 'mongodb' in ds[0][2]:
                    self.mongodb = DBMSMongoDB(ds[0][3], ds[0][6])
            elif 'mongodb' in self.vendor:
                tmp = DBMSMongoDB(default['db_name'], default['collection'])
                sql = {'datasource': self.datasource}
                ds = tmp.find(sql)
                self.vendor = ds[0]['vendor']
                if 'postgresql' in ds[0]['vendor']:
                    self.postgresql = DBMSPostgreSQL(ds[0]['db_name'], ds[0]['username'], ds[0]['password'])
                elif 'mongodb' in ds[0]['vendor']:
                    self.mongodb = DBMSMongoDB(ds[0]['db_name'], ds[0]['collection'])
        elif 'mongodb' in self.vendor:
            self.mongodb = DBMSMongoDB(self.db_name, self.collection_name)
        elif 'postgresql' in self.vendor:
            self.postgresql = DBMSPostgreSQL(self.db_name, self.username, self.password)
        return

    def find_all(self, table_name=None):
        if 'mongodb' in self.vendor:
            return self.mongodb.find({})
        if 'postgresql' in self.vendor:
            return self.postgresql.select_all(table_name)

    def find_by_id(self, item_id, table_name=None):
        if 'mongodb' in self.vendor:
            return self.mongodb.find_by_id(item_id)
        if 'postgresql' in self.vendor:
            return self.postgresql.select_by_id(table_name, item_id)

    def find_by_field(self, field_name, field_value, table_name=None):
        if 'mongodb' in self.vendor:
            return self.mongodb.find_by_field(field_name, field_value)
        if 'postgresql' in self.vendor:
            return self.postgresql.select_by_field(table_name, field_name, field_value)

    def insert(self, item, table_name=None):
        if 'mongodb' in self.vendor:
            return self.mongodb.insert(item)
        if 'postgresql' in self.vendor:
            return self.postgresql.insert(table_name, item)

    def query(self, query):
        if 'postgresql' in self.vendor:
            return self.postgresql.query(query)
        if 'mongodb' in self.vendor:
            return self.mongodb.find(query)