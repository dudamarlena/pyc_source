# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Python27\Lib\site-packages\CodeLibWrapper\Src\Database\SQLServerHelper.py
# Compiled at: 2016-12-29 00:49:38
import pymssql

class SQLServerHelper:
    server = ''
    user = ''
    password = ''

    def __init__(self, server_instance, login_user, login_password):
        global password
        global server
        global user
        server = server_instance
        user = login_user
        password = login_password

    def execute_sql_script_with_no_return(self, database_name, script):
        u"""
        :param database_name: 要连接的数据库名，例如： tempdb
        :param script: 要执行的SQL命令文本。例如：

        IF OBJECT_ID('persons', 'U') IS NOT NULL
            DROP TABLE persons
        CREATE TABLE persons (
            id INT NOT NULL,
            name VARCHAR(100),
            salesrep VARCHAR(100),
            PRIMARY KEY(id)
        )
        :return:
        """
        conn = pymssql.connect(server, user, password, database_name)
        cursor = conn.cursor()
        cursor.execute(script)
        conn.commit()
        conn.close()

    def execute_sql_query_return_many_record(self, database_name, script):
        conn = pymssql.connect(server, user, password, database_name)
        cursor = conn.cursor()
        cursor.execute(script)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def execute_sql_query_return_one_record(self, database_name, script):
        u"""
        :param database_name: 要连接的数据库名，例如： tempdb
        :param script: 要执行的SQL命令文本。例如：
        :return:
        """
        conn = pymssql.connect(server, user, password, database_name)
        cursor = conn.cursor()
        cursor.execute(script)
        row = cursor.fetchone()
        conn.close()
        return row


def main():
    print 'SQL Server Test'


if __name__ == '__main__':
    main()