# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\mysqlmapper\mysql\client.py
# Compiled at: 2020-04-03 04:05:31
# Size of source mod 2**32: 771 bytes
import pymysql

class ConnHolder:
    """ConnHolder"""
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