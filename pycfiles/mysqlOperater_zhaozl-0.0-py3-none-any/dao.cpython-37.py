# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\mysqlmapper\mysql\mvc\dao.py
# Compiled at: 2020-04-03 04:05:31
# Size of source mod 2**32: 2138 bytes
from mysqlmapper.mysql.manager import get_manager_by_dbinfo

class DAO:
    _manager = None
    _get_list = 'GetList'
    _get_count = 'GetCount'
    _get_model = 'GetModel'
    _update = 'Update'
    _insert = 'Insert'
    _delete = 'Delete'

    def __init__(self, conn, database_info, table_name):
        """
        Initialize Dao layer
        :param conn: Database connection
        :param database_info: database information
        :param table_name: Table name
        """
        self._manager = get_manager_by_dbinfo(conn, database_info, table_name)

    def get_list(self, parameter):
        """
        Get data list
        :param parameter: Search parameters
        :return: Data list
        """
        return self._manager.query(self._get_list, parameter)

    def get_count(self, parameter):
        """
        Quantity acquisition
        :param parameter: Search parameters
        :return: Number
        """
        return self._manager.count(self._get_count, parameter)

    def get_model(self, parameter):
        """
        Get record entity
        :param parameter: Search parameters
        :return: Record entity
        """
        list_dict = self._manager.query(self._get_model, parameter)
        if len(list_dict) == 0:
            return
        return list_dict[0]

    def update(self, parameter):
        """
        Update record
        :param parameter: Update data
        :return: Update results
        """
        _, number = self._manager.exec(self._update, parameter)
        return number

    def insert(self, parameter):
        """
        insert record
        :param parameter: insert data
        :return: Insert results
        """
        id, _ = self._manager.exec(self._insert, parameter)
        return id

    def delete(self, parameter):
        """
        Delete data
        :param parameter: Delete data
        :return: Delete result
        """
        _, number = self._manager.exec(self._delete, parameter)
        return number