# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mysqlmapper\mysql\mvc\service.py
# Compiled at: 2020-04-03 04:05:31
# Size of source mod 2**32: 1668 bytes
from mysqlmapper.mysql.mvc.dao import DAO

class Service:
    __doc__ = '\n    Basic service layer\n    '
    _dao = None

    def __init__(self, conn, database_info, table_name):
        """
        Initialize service layer
        :param conn: Database connection
        :param database_info: database information
        :param table_name: Table name
        """
        self._dao = DAO(conn, database_info, table_name)

    def get_list(self, parameter):
        """
        Get data list
        :param parameter: Search parameters
        :return: Data list
        """
        return self._dao.get_list(parameter)

    def get_count(self, parameter):
        """
        Quantity acquisition
        :param parameter: Search parameters
        :return: Number
        """
        return self._dao.get_count(parameter)

    def get_model(self, parameter):
        """
        Get record entity
        :param parameter: Search parameters
        :return: Record entity
        """
        return self._dao.get_model(parameter)

    def update(self, parameter):
        """
        Update record
        :param parameter: Update data
        :return: Update results
        """
        return self._dao.update(parameter)

    def insert(self, parameter):
        """
        insert record
        :param parameter: insert data
        :return: Insert results
        """
        return self._dao.insert(parameter)

    def delete(self, parameter):
        """
        Delete data
        :param parameter: Delete data
        :return: Delete result
        """
        return self._dao.delete(parameter)