# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/utils/sql/pg.py
# Compiled at: 2020-02-03 23:11:43
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: pg.py
@create at: 2017-12-15 14:28

这一行开始写关于本文件的说明与解释
"""
from crwy.exceptions import CrwyImportException, CrwyDbException
from crwy.decorates import cls2singleton
try:
    import pgdb
except ImportError:
    raise CrwyImportException('You should install PyGreSQL first! try: pip install PyGreSQL')

try:
    from DBUtils.PersistentDB import PersistentDB
except ImportError:
    raise CrwyImportException('You should install DBUtils first! try: pip install dbutils')

@cls2singleton
class PgHandle(object):

    def __init__(self, **kwargs):
        self._pg_pool = PersistentDB(pgdb, **kwargs)

    def query_by_sql(self, sql):
        conn = self._pg_pool.connection()
        cur = conn.cursor()
        try:
            try:
                cur.execute(sql)
                result = cur.fetchall()
                return result
            except Exception as e:
                raise CrwyDbException(e)

        finally:
            cur.close()
            conn.close()

    def save(self, sql, data, many=False, get_last_insert_id=False):
        conn = self._pg_pool.connection()
        cur = conn.cursor()
        try:
            try:
                if get_last_insert_id is True:
                    sql = sql.strip(';')
                    sql = sql + ' returning id'
                if many is False:
                    cur.execute(sql, data)
                else:
                    cur.executemany(sql, data)
                conn.commit()
                if get_last_insert_id is True:
                    res = cur.fetchone()
                    return res.id
            except Exception as e:
                raise CrwyDbException(e)

        finally:
            cur.close()
            conn.close()