# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\mysqlmapper\mysql\mvc\holder.py
# Compiled at: 2020-04-03 04:05:31
# Size of source mod 2**32: 1046 bytes
from mysqlmapper.mysql.client import ConnHolder
from mysqlmapper.mysql.info.info import get_db_info
from mysqlmapper.mysql.mvc.service import Service

class MVCHolder:
    """MVCHolder"""
    conn_holder = None
    database_info = None
    services = None

    def __init__(self, host, user, password, database, charset='utf8'):
        """
        Initialize MVC holder
        :param host: host name
        :param user: User name
        :param password: Password
        :param database: Database name
        :param charset: Encoding format
        """
        self.conn_holder = ConnHolder(host, user, password, database, charset)
        self.database_info = get_db_info(self.conn_holder.get_conn(), database)
        self.services = {}
        for table in self.database_info['tables']:
            self.services[table['Name']] = Service(self.conn_holder.get_conn(), self.database_info, table['Name'])