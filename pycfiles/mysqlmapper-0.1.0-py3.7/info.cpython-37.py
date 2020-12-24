# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mysqlmapper\mysql\info\info.py
# Compiled at: 2020-04-03 04:05:31
# Size of source mod 2**32: 1327 bytes
from mysqlmapper.mysql.builder.xml_config import parse_config_from_string
from mysqlmapper.mysql.info.xml_info import index_xml, table_xml, column_xml, key_xml
from mysqlmapper.mysql.manager import Manager

def get_db_info(conn, database_name):
    """
    Get database information
    :param conn: Database connection
    :param database_name: Database name
    :return: database information
    """
    table_config = parse_config_from_string(table_xml)
    column_config = parse_config_from_string(column_xml)
    index_config = parse_config_from_string(index_xml)
    key_config = parse_config_from_string(key_xml)
    tables = Manager(conn, table_config).query('GetList', {'data_base_name': database_name})
    for table in tables:
        table['columns'] = Manager(conn, column_config).query('GetList', {'data_base_name':database_name,  'table_name':table['Name']})
        table['indexs'] = Manager(conn, index_config).query('GetList', {'data_base_name':database_name,  'table_name':table['Name']})
        table['keys'] = Manager(conn, key_config).query('GetList', {'data_base_name':database_name,  'table_name':table['Name']})

    return {'Name':database_name, 
     'tables':tables}