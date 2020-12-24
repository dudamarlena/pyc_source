# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mysqlmapper\mysql\client.py
# Compiled at: 2020-04-03 04:05:31
# Size of source mod 2**32: 771 bytes
import pymysql

class ConnHolder:
    __doc__ = '\n    Database connection holder\n    '
    _conn = None

    def __init__(self, host, user, password, database, charset='utf8'):
        """
        Initialize database connection
        :param host: host
        :param user: user
        :param password: password
        :param database: database
        :param charset: charset
        :return:
        """
        self._conn = pymysql.connect(host=host,
          user=user,
          password=password,
          database=database,
          charset=charset)

    def get_conn(self):
        """
        Get database connection
        :return: Database connection
        """
        return self._conn