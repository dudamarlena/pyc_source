# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sqlpool\SqlPool.py
# Compiled at: 2020-05-06 22:51:48
# Size of source mod 2**32: 7721 bytes
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
from DBUtils.PooledDB import PooledDB
import pymysql, pymssql, cx_Oracle

class SQLHandler(object):

    def __init__(self, host, user, password, db_type, db_name, port=None):
        self.db_type = db_type
        if db_type == 'mysql':
            self.pool = PooledDB(creator=pymysql,
              maxconnections=3,
              mincached=1,
              maxcached=3,
              maxshared=3,
              blocking=True,
              maxusage=None,
              setsession=[],
              ping=0,
              host=host,
              user=user,
              password=password,
              database=db_name,
              charset='utf8')
        else:
            if db_type == 'sqlserver':
                self.pool = PooledDB(creator=pymssql,
                  maxconnections=10,
                  mincached=5,
                  maxcached=5,
                  maxshared=0,
                  blocking=True,
                  maxusage=0,
                  setsession=[],
                  ping=0,
                  host=host,
                  user=user,
                  password=password,
                  database=db_name,
                  charset='utf8')
            elif db_type == 'oracle':
                dsn = cx_Oracle.makedsn(host, 1521, sid='ORCL')
                self.pool = PooledDB(creator=cx_Oracle,
                  maxconnections=10,
                  mincached=5,
                  maxcached=5,
                  maxshared=0,
                  blocking=True,
                  maxusage=0,
                  setsession=[],
                  ping=0,
                  user=user,
                  password=password,
                  dsn=dsn)

    def create_conn_cursor(self):
        conn = self.pool.connection()
        if self.db_type == 'mysql':
            cursor = conn.cursor(pymysql.cursors.DictCursor)
        else:
            if self.db_type == 'sqlserver':
                cursor = conn.cursor(as_dict=True)
            else:
                if self.db_type == 'oracle':
                    cursor = conn.cursor()
        return (
         conn, cursor)

    def fetch_one(self, sql, args=None):
        conn, cursor = self.create_conn_cursor()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def fetch_many(self, sql, args=None):
        conn, cursor = self.create_conn_cursor()
        cursor.execute(sql)
        result = cursor.fetchmany(args)
        cursor.close()
        conn.close()
        return result

    def fetch_all(self, sql, args=None):
        conn, cursor = self.create_conn_cursor()
        if self.db_type == 'oracle':
            cursor.execute(sql)
        else:
            cursor.execute(sql, args)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def insert_one(self, sql, args=None):
        conn, cursor = self.create_conn_cursor()
        res = cursor.execute(sql, args)
        conn.commit()
        conn.close()
        return res

    def insert_many(self, sql, args=None):
        conn, cursor = self.create_conn_cursor()
        res = cursor.executemany(sql, args)
        conn.commit()
        conn.close()
        return res

    def update(self, sql, args=None):
        conn, cursor = self.create_conn_cursor()
        res = cursor.execute(sql, args)
        conn.commit()
        conn.close()
        return res

    def delete(self, sql, args=None):
        conn, cursor = self.create_conn_cursor()
        res = cursor.execute(sql, args)
        conn.commit()
        print(res)
        conn.close()
        return res