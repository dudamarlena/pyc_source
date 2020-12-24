# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\SQLAlchemy_wrap\sql_factory\sqlite_factory.py
# Compiled at: 2019-08-20 12:45:04
# Size of source mod 2**32: 380 bytes
from SQLAlchemy_wrap.sql_factory import SqlalchemyFactory

class SqliteFactory(SqlalchemyFactory):

    def db(self, db_name, db_file=None, *args, **kw):
        if db_file is not None:
            sql_url = 'sqlite:///' + db_file
            super().connect(db_name, sql_url, *args, **kw)
        return super().db(db_name)