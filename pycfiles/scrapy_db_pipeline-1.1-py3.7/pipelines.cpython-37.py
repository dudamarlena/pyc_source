# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/scrapy_db_pipeline/pipelines.py
# Compiled at: 2019-11-14 07:19:31
# Size of source mod 2**32: 2154 bytes
"""
# =============================================================================
#      FileName: pipelines.py
#          Desc: scrapy database pipeline
#        Author: chemf
#         Email: eoyohe@gmail.com
#      HomePage: eoyohe.cn
#       Version: 0.0.1
#    LastChange: 2019-11-14 20:18:33
#       History:
# =============================================================================
"""
import logging
from DBUtils.SteadyDB import SteadyDBConnection
import pymysql

class DBStorePipeline(object):

    def __init__(self, host, db, user, password):
        self.conn = SteadyDBConnection(creator=(pymysql.connect),
          host=host,
          db=db,
          user=user,
          password=password,
          autocommit=True)

    @classmethod
    def from_settings(cls, settings):
        host = settings.get('DB_HOST')
        db = settings.get('DB_NAME')
        user = settings.get('DB_USER')
        password = settings.get('DB_PASSWORD')
        return cls(host, db, user, password)

    @property
    def logger(self):
        logger = logging.getLogger('mysql')
        return logging.LoggerAdapter(logger, {'spider': self})

    def process_item(self, item, spider):
        if hasattr(item, '__table_name__'):
            self._process_item(item)
        return item

    def _process_item(self, item):
        sql = '\n        INSERT INTO {table_name}\n        ({fields})\n        VALUES\n        ({values})\n        ON DUPLICATE KEY UPDATE\n        {update}\n        '
        fields = item._values
        sql = sql.format(table_name=(item.__table_name__),
          fields=(','.join(fields)),
          values=(','.join(['%s'] * len(fields))),
          update=(','.join(('{field}=VALUES({field})'.format(field=field) for field in fields))))
        with self.conn.cursor() as (cursor):
            self.logger.debug('[sql] %s %s', sql, item)
            cursor.execute(sql, [item.get(k) for k in fields])
            self.logger.debug('[sql] executed sql %s', cursor._last_executed)