# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/factories/sql_connection.py
# Compiled at: 2012-10-12 07:02:39


class SQLConnection(object):

    def __init__(self, params):
        self._db = None
        return

    def connect(self):
        pass

    def cursor(self):
        pass

    def get_type_from_code(string, code):
        return code

    def bind_param(self, offset):
        return (':{0}').format(offset)

    def commit(self):
        self._db.commit()

    def rollback(self):
        self._db.rollback()

    def close(self):
        self._db.close()