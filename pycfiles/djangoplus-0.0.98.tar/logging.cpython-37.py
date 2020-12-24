# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/utils/logging.py
# Compiled at: 2019-03-30 22:36:03
# Size of source mod 2**32: 601 bytes
from logging import StreamHandler

class CustomStreamHandler(StreamHandler):

    def emit(self, record):
        sql = record.getMessage()
        sql = sql.replace('\n            ', '')
        time = sql[0:8]
        if 'SELECT' in sql:
            sql = sql[8:]
            if 'COUNT' not in sql and 'FROM' in sql:
                sql = 'SELECT * {}'.format(sql[sql.index('FROM'):])
        elif 'BEGIN' in sql:
            sql = None
        else:
            if 'UPDATE "django_session"' in sql:
                sql = None
        if sql:
            print(time, sql)