# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/gorgou/sql/mssql.py
# Compiled at: 2018-02-02 23:22:40
# Size of source mod 2**32: 2932 bytes
import pymssql
from gorgou.x import jsonx

class Connection(object):

    def __init__(self, mssql_conf_file=None):
        if not mssql_conf_file:
            mssql_conf_file = 'mssql.conf'
        mssql_conf = jsonx.load_json(mssql_conf_file)
        self.connection = pymssql.Connection(mssql_conf['host'], mssql_conf['user'], mssql_conf['passwd'], mssql_conf['db'])
        self.cursor = self.connection.cursor()

    @property
    def cur(self):
        return self.cursor

    @cur.setter
    def cur(self, value):
        self.cursor = value

    @property
    def conn(self):
        return self.connection

    @conn.setter
    def conn(self, value):
        self.connection = value

    def commit(self):
        return self.conn.commit()

    def rollback(self):
        return self.conn.rollback()

    def execute(self, *args, **kwargs):
        return (self.cur.execute)(*args, **kwargs)

    def close(self):
        self.cur.close()
        self.conn.close()

    def get(self, *args, **kwargs):
        (self.cur.execute)(*args, **kwargs)
        return self.cur.fetchall()

    def get_one(self, *args, **kwargs):
        (self.cur.execute)(*args, **kwargs)
        return self.cur.fetchone()

    def get_page(self, table, orderBy, where, pageSize, pageNum):
        pager = {}
        pager['pageSize'] = pageSize
        pager['pageNum'] = pageNum
        l = pager['pageSize']
        o = (pager['pageNum'] - 1) * pager['pageSize']
        tmpsql = 'select count(*) as count from ' + table
        if where:
            tmpsql = tmpsql + ' where ' + where
        count = self.get_one(tmpsql)['count']
        pager['pageCount'] = int((count + pager['pageSize'] - 1) / pager['pageSize'])
        if not pager['pageCount']:
            pager['pageCount'] = 1
        tmpsql = 'select * from ' + table
        if where:
            tmpsql = tmpsql + ' where ' + where
        if not orderBy:
            pass
        tmpsql = tmpsql + ' order by ' + orderBy + ' limit %s offset %s'
        result = self.get(tmpsql, (l, o))
        return (result, pager)

    def safe_execute(self, *args, **kwargs):
        try:
            (self.cur.execute)(*args, **kwargs)
            self.conn.commit()
        except:
            self.conn.rollback()

    def safe_execute_ret_rowcount(self, *args, **kwargs):
        try:
            (self.cur.execute)(*args, **kwargs)
            self.conn.commit()
            return self.cur.rowcount
        except:
            self.conn.rollback()
            return 0

    def safe_execute_ret_lastrowid(self, *args, **kwargs):
        try:
            (self.cur.execute)(*args, **kwargs)
            self.conn.commit()
            return self.cur.lastrowid
        except:
            self.conn.rollback()
            return 0