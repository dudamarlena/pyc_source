# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\mysqlmapper\mysql\mvc\service.py
# Compiled at: 2020-04-03 04:05:31
# Size of source mod 2**32: 1668 bytes
from mysqlmapper.mysql.mvc.dao import DAO

class Service:
    """Service"""
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