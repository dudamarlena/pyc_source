# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/pinot_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3483 bytes
import six
from pinotdb import connect
from airflow.hooks.dbapi_hook import DbApiHook

class PinotDbApiHook(DbApiHook):
    """PinotDbApiHook"""
    conn_name_attr = 'pinot_broker_conn_id'
    default_conn_name = 'pinot_broker_default'
    supports_autocommit = False

    def __init__(self, *args, **kwargs):
        (super(PinotDbApiHook, self).__init__)(*args, **kwargs)

    def get_conn(self):
        """
        Establish a connection to pinot broker through pinot dbqpi.
        """
        conn = self.get_connection(self.pinot_broker_conn_id)
        pinot_broker_conn = connect(host=(conn.host),
          port=(conn.port),
          path=(conn.extra_dejson.get('endpoint', '/pql')),
          scheme=(conn.extra_dejson.get('schema', 'http')))
        self.log.info('Get the connection to pinot broker on {host}'.format(host=(conn.host)))
        return pinot_broker_conn

    def get_uri(self):
        """
        Get the connection uri for pinot broker.

        e.g: http://localhost:9000/pql
        """
        conn = self.get_connection(getattr(self, self.conn_name_attr))
        host = conn.host
        if conn.port is not None:
            host += ':{port}'.format(port=(conn.port))
        conn_type = 'http' if not conn.conn_type else conn.conn_type
        endpoint = conn.extra_dejson.get('endpoint', 'pql')
        return '{conn_type}://{host}/{endpoint}'.format(conn_type=conn_type,
          host=host,
          endpoint=endpoint)

    def get_records(self, sql):
        """
        Executes the sql and returns a set of records.

        :param sql: the sql statement to be executed (str) or a list of
            sql statements to execute
        :type sql: str
        """
        if six.PY2:
            sql = sql.encode('utf-8')
        with self.get_conn() as (cur):
            cur.execute(sql)
            return cur.fetchall()

    def get_first(self, sql):
        """
        Executes the sql and returns the first resulting row.

        :param sql: the sql statement to be executed (str) or a list of
            sql statements to execute
        :type sql: str or list
        """
        if six.PY2:
            sql = sql.encode('utf-8')
        with self.get_conn() as (cur):
            cur.execute(sql)
            return cur.fetchone()

    def set_autocommit(self, conn, autocommit):
        raise NotImplementedError()

    def get_pandas_df(self, sql, parameters=None):
        raise NotImplementedError()

    def insert_rows(self, table, rows, target_fields=None, commit_every=1000):
        raise NotImplementedError()