# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/youdao/sqlsaver.py
# Compiled at: 2019-02-16 23:51:48
import os, json, sqlite3
from contextlib import contextmanager
from urllib import quote, unquote
from youdao.config import DB_PATH

class SQLSaver(object):

    def __init__(self, db_path=''):
        if db_path:
            self.db_path = db_path
        else:
            self.db_path = os.path.expanduser(DB_PATH)
        self.TABLE = 'query'

    @contextmanager
    def connection(self):
        """connection instance to sqlite"""
        db = sqlite3.connect(self.db_path)
        db.text_factory = str
        cursor = db.cursor()
        cursor.execute(("CREATE TABLE IF NOT EXISTS `{}` (id INTEGER PRIMARY KEY AUTOINCREMENT, query varchar(50) NOT NULL UNIQUE,raw_json TEXT NOT NULL DEFAULT '')").format(self.TABLE))
        yield cursor
        db.commit()
        db.close()

    def query(self, query):
        with self.connection() as (cursor):
            cursor.execute(('select raw_json from {} WHERE query = ? ').format(self.TABLE), (
             query,))
            result = cursor.fetchone()
            if result:
                return json.loads(unquote(result[0]))
            return
        return

    def remove_query(self, query):
        """remove one saved query"""
        with self.connection() as (cursor):
            cursor.execute(('delete from {} where query = ?').format(self.TABLE), (
             query,))

    def shred_query(self, shred):
        """query for auto complete"""
        with self.connection() as (cursor):
            if shred:
                cursor.execute(('select query from {} WHERE query like ? limit 10').format(self.TABLE), (
                 shred + '%',))
            else:
                cursor.execute(('select query from {} order by id desc limit 10').format(self.TABLE))
            return cursor.fetchall()

    def upset(self, query, raw_dict):
        """update or insert one query result"""
        with self.connection() as (cursor):
            cursor.execute(('select id from {} WHERE query = ? ').format(self.TABLE), (
             query,))
            result = cursor.fetchone()
            raw_json = quote(json.dumps(raw_dict))
            if result:
                cursor.execute(('update {} set raw_json = ? WHERE id = ?').format(self.TABLE), (
                 raw_json, result[0]))
            else:
                cursor.execute(('insert into {} (query ,raw_json) VALUES (?, ?)').format(self.TABLE), (
                 query, raw_json))