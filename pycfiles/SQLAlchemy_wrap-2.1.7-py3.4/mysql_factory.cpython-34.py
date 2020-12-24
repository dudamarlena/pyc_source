# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\SQLAlchemy_wrap\sql_factory\mysql_factory.py
# Compiled at: 2019-08-20 12:44:50
# Size of source mod 2**32: 669 bytes
from SQLAlchemy_wrap.sql_factory import SqlalchemyFactory

class MysqlFactory(SqlalchemyFactory):

    def db(self, db_name, username='', password='', host='127.0.0.1', *args, **kw):
        if username != '':
            sql_url = 'mysql+pymysql://' + username + ':' + password + '@' + host + ':3306' + '/' + db_name
            super().connect(db_name, sql_url, *args, **kw)
        return super().db(db_name)