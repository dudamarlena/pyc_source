# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/wiki_node_disambiguation/wiki_node_disambiguation/initialize_mysql_connector.py
# Compiled at: 2016-12-02 06:37:21
# Size of source mod 2**32: 805 bytes


def initialize_mysql_connector(hostname: str, user_name: str, password: str, dbname: str):
    """
    """
    import MySQLdb
    conn = MySQLdb.connect(hostname, user_name, password, dbname)
    return conn


def initialize_pymysql_connector(hostname: str, user_name: str, password: str, dbname: str):
    import pymysql.cursors
    connection = pymysql.connect(host=hostname, user=user_name, password=password, db=dbname, charset='utf8')
    return connection