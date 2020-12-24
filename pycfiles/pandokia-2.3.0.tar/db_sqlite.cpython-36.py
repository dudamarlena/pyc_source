# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/db_sqlite.py
# Compiled at: 2018-06-04 12:38:26
# Size of source mod 2**32: 5221 bytes
__all__ = [
 'db_module',
 'db_driver',
 'PandokiaDB',
 'threadsafety']
import os
try:
    import StringIO
except ImportError:
    import io as StringIO

import pandokia.db
try:
    import sqlite3 as db_module
except ImportError:
    import pysqlite2.dbapi2 as db_module

threadsafety = db_module.threadsafety
db_driver = 'sqlite'

class PandokiaDB(pandokia.db.where_dict_base):
    IntegrityError = db_module.IntegrityError
    ProgrammingError = db_module.ProgrammingError
    OperationalError = db_module.OperationalError
    DatabaseError = db_module.DatabaseError
    pandokia_driver_name = __module__.split('db_')[1]
    db = None

    def __init__(self, access_arg):
        if isinstance(access_arg, dict):
            access_arg['database'] = os.path.abspath(access_arg['database'])
        else:
            access_arg = {'database': os.path.abspath(access_arg)}
        self.db_access_arg = access_arg

    def open(self):
        if self.db is None:
            self.db = (db_module.connect)(**self.db_access_arg)
            self.db.execute('PRAGMA synchronous = NORMAL;')
            self.db.text_factory = str
            self.db.execute('PRAGMA case_sensitive_like = true;')
            return

    def start_transaction(self):
        if self.db is None:
            self.open()
        self.execute('BEGIN TRANSACTION')

    def commit(self):
        if self.db is None:
            return
        self.db.commit()

    def rollback(self):
        if self.db is None:
            return
        self.db.rollback()

    def rollback_or_reconnect(self):
        return self.rollback()

    def explain_query(self, text, query_dict=None):
        print('TEXT %s' % text)
        print('DICT %s' % query_dict)
        f = StringIO.StringIO()
        c = self.execute('EXPLAIN QUERY PLAN ' + text, query_dict)
        for x in c:
            f.write(str(x))

        return f.getvalue()

    def execute(self, statement, parameters=[], db=None):
        if self.db is None:
            self.open()
        if isinstance(parameters, dict):
            pass
        else:
            if isinstance(parameters, list) or isinstance(parameters, tuple):
                tmp = {}
                for x in range(0, len(parameters)):
                    tmp[str(x + 1)] = parameters[x]

                parameters = tmp
            else:
                if parameters is None:
                    parameters = []
                else:
                    raise self.ProgrammingError
            c = self.db.cursor()
            c.execute(statement, parameters)
            return c

    def table_usage(self):
        return os.path.getsize(self.db_access_arg)

    next = None