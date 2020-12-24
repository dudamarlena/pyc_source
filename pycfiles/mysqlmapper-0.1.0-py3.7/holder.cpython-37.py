# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mysqlmapper\mysql\mvc\holder.py
# Compiled at: 2020-04-03 04:05:31
# Size of source mod 2**32: 1046 bytes
from mysqlmapper.mysql.client import ConnHolder
from mysqlmapper.mysql.info.info import get_db_info
from mysqlmapper.mysql.mvc.service import Service

class MVCHolder:
    __doc__ = '\n    MVC retainer\n    '
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