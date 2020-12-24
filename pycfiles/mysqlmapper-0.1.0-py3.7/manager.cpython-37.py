# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mysqlmapper\mysql\manager.py
# Compiled at: 2020-04-03 04:05:31
# Size of source mod 2**32: 3586 bytes
import mysqlmapper.mysql.builder.sql_builder as sql_builder
from mysqlmapper.mysql.builder.xml_config import parse_config_from_string, parse_config_from_file
from mysqlmapper.mysql.engine import Engine
from mysqlmapper.mysql.generate.mapper import get_mapper_xml

class Manager:
    conn = None
    xml_config = None

    def __init__(self, conn, xml_config):
        """
        Initialize Manager
        :param conn: Database connection
        :param xml_config: XML profile information
        """
        self.conn = conn
        self.xml_config = xml_config

    def query(self, key, parameter):
        """
        Query result set
        :param key: SQL alias
        :param parameter: Execution parameter
        :return: results of enforcement
        """
        sql = self.xml_config['sqls'][key]
        result, parameters = sql_builder(sql, parameter)
        print('Currently executing SQL>>>', result, parameters)
        query_list = Engine.query(self.conn, result, parameters)
        list = []
        for query_item in query_list:
            item = {}
            for t in query_item.items():
                if t[0] in self.xml_config['mappers']:
                    item[self.xml_config['mappers'][t[0]]] = t[1]
                    continue
                item[t[0]] = t[1]

            list.append(item)

        return list

    def count(self, key, parameter):
        """
        Query quantity
        :param key: SQL alias
        :param parameter: Execution parameter
        :return: results of enforcement
        """
        sql = self.xml_config['sqls'][key]
        result, parameters = sql_builder(sql, parameter)
        print('Currently executing SQL>>>', result, parameters)
        return Engine.count(self.conn, result, parameters)

    def exec(self, key, parameter):
        """
        Implementation of SQL
        :param key: SQL alias
        :param parameter: Execution parameter
        :return: results of enforcement
        """
        sql = self.xml_config['sqls'][key]
        result, parameters = sql_builder(sql, parameter)
        print('Currently executing SQL>>>', result, parameters)
        return Engine.exec(self.conn, result, parameters)


def get_manager_by_string(conn, xml_string):
    """
    Get manager using string
    :param conn: Database connection
    :param xml_string: xml Character string
    :return: Manager
    """
    config = parse_config_from_string(xml_string)
    return Manager(conn, config)


def get_manager_by_file(conn, xml_path):
    """
    Get manager using XML file
    :param conn: Database connection
    :param xml_path: XML file path
    :return: Manager
    """
    config = parse_config_from_file(xml_path)
    return Manager(conn, config)


def get_manager_by_dbinfo(conn, database_info, table_name):
    """
    Get manager with database information
    :param conn: Database connection
    :param database_info: database information
    :param table_name: Table name
    :return: Manager
    """
    xml_string = get_mapper_xml(database_info, table_name)
    return get_manager_by_string(conn, xml_string)