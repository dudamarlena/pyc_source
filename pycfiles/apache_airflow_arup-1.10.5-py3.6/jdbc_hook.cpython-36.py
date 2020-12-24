# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/hooks/jdbc_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2159 bytes
from builtins import str
import jaydebeapi
from airflow.hooks.dbapi_hook import DbApiHook

class JdbcHook(DbApiHook):
    __doc__ = '\n    General hook for jdbc db access.\n\n    JDBC URL, username and password will be taken from the predefined connection.\n    Note that the whole JDBC URL must be specified in the "host" field in the DB.\n    Raises an airflow error if the given connection id doesn\'t exist.\n    '
    conn_name_attr = 'jdbc_conn_id'
    default_conn_name = 'jdbc_default'
    supports_autocommit = True

    def get_conn(self):
        conn = self.get_connection(getattr(self, self.conn_name_attr))
        host = conn.host
        login = conn.login
        psw = conn.password
        jdbc_driver_loc = conn.extra_dejson.get('extra__jdbc__drv_path')
        jdbc_driver_name = conn.extra_dejson.get('extra__jdbc__drv_clsname')
        conn = jaydebeapi.connect(jclassname=jdbc_driver_name, url=(str(host)),
          driver_args=[
         str(login), str(psw)],
          jars=(jdbc_driver_loc.split(',')))
        return conn

    def set_autocommit(self, conn, autocommit):
        """
        Enable or disable autocommit for the given connection.

        :param conn: The connection
        :return:
        """
        conn.jconn.setAutoCommit(autocommit)