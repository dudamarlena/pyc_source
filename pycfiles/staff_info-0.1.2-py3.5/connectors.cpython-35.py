# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/db/connectors.py
# Compiled at: 2018-05-16 09:41:14
# Size of source mod 2**32: 2649 bytes
import mysql.connector
from mysql.connector import errorcode
from tkinter.messagebox import askokcancel, showerror

class MySQLConnector:

    def __init__(self, **credentials):
        self.credentials = credentials
        self.last_row_id = None

    @property
    def connection(self):
        cnx = None
        try:
            cnx = mysql.connector.connect(**self.credentials)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Wrong username/passwrod credential')
            else:
                if err.errno == errorcode.ER_BAD_DB_ERROR:
                    print('Database does not exist')
                else:
                    print(err)

        return cnx

    def execute_sql(self, sql, *params, change=True):
        """
        Execute raw sql with provided parameters
        :param sql: raw sql string;
        :param params: placeholders in sql query
        :param change: flag, that indicates whether query is select or make changes to DB
        :return: results of executed query
        """
        cnx = self.connection
        cursor = cnx.cursor()
        result = None
        print(sql, params)
        try:
            result = cursor.execute(sql, params)
        except mysql.connector.errors.DataError:
            showerror('Type error', 'Incorrect data type')
        else:
            if change:
                if askokcancel('SQL changes', 'Commit changes?'):
                    cnx.commit()
                else:
                    cnx.rollback()
            else:
                if cursor.with_rows:
                    result = cursor.fetchall()
                self.last_row_id = cursor.lastrowid
                cursor.close()
            return result

    def execute_sql_in_transaction(self, *sql):
        cnx = self.connection
        cnx.start_transaction()
        cursor = cnx.cursor()
        try:
            for sql_row in sql:
                print(sql_row[0], sql_row[1])
                cursor.execute(sql_row[0], sql_row[1])

        except mysql.connector.errors.DataError:
            showerror('Type error', 'Incorrect data type')
        else:
            if askokcancel('SQL changes', 'Commit changes?'):
                cnx.commit()
            else:
                cnx.rollback()

    def close(self):
        self.connection.close()


def connection_factory(db_type, **credentials):
    if db_type == 'mysql':
        connector = MySQLConnector
    else:
        raise ValueError('Connector for DB Type {} not implemented yet'.format(db_type))
    return connector(**credentials)