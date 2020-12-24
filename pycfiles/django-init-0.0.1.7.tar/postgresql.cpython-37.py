# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/projects/django-init/django_init/db/postgresql.py
# Compiled at: 2020-01-15 01:24:21
# Size of source mod 2**32: 920 bytes
import psycopg2
from django_init.db.base import DatabaseBase

class DatabasePostgreSQL(DatabaseBase):
    client = psycopg2
    sql_show_dbs = 'SELECT * FROM pg_database'
    sql_create_db = 'CREATE DATABASE %s WITH OWNER = %s'

    def connect(self):
        try:
            self.conn = (self.client.connect)(**self.config)
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e

        else:
            print(self.msg_connect)

    def create_db(self, db_name):
        user = self.config.get('user')
        sql = self.sql_create_db % (db_name, user)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e

        else:
            print(self.msg_create_db % db_name)