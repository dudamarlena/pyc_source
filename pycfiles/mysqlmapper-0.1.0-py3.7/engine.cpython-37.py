# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mysqlmapper\mysql\engine.py
# Compiled at: 2020-04-03 04:14:01
# Size of source mod 2**32: 2788 bytes
from threading import Lock
_lock = Lock()

class Engine:
    __doc__ = '\n    SQL Execution Engine\n    '

    @staticmethod
    def query(conn, sql, parameter):
        """
        Query list information
        :param conn: Database connection
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Query results
        """
        _lock.acquire()
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        exception = None
        try:
            cursor.execute(sql, parameter)
        except Exception as e:
            try:
                print(e)
                exception = e
            finally:
                e = None
                del e

        conn.commit()
        names = []
        for i in cursor.description:
            names.append(i[0])

        results = []
        for i in cursor.fetchall():
            result = {}
            for j in range(len(i)):
                result[names[j]] = i[j]

            results.append(result)

        cursor.close()
        _lock.release()
        if exception is not None:
            raise exception
        return results

    @staticmethod
    def count(conn, sql, parameter):
        """
        Query quantity information
        :param conn: Database connection
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Query results
        """
        result = Engine.query(conn, sql, parameter)
        if len(result) == 0:
            return 0
        for value in result[0].values():
            return value

    @staticmethod
    def exec(conn, sql, parameter):
        """
        Execute SQL statement
        :param conn: Database connection
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Last inserted ID, affecting number of rows
        """
        _lock.acquire()
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        exception = None
        try:
            cursor.execute(sql, parameter)
        except Exception as e:
            try:
                print(e)
                exception = e
            finally:
                e = None
                del e

        conn.commit()
        rowcount = cursor.rowcount
        lastrowid = cursor.lastrowid
        cursor.close()
        _lock.release()
        if exception is not None:
            raise exception
        return (
         lastrowid, rowcount)