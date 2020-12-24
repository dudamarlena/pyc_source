# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/hooks/presto_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4772 bytes
from builtins import str
from pyhive import presto
from pyhive.exc import DatabaseError
from requests.auth import HTTPBasicAuth
from airflow.hooks.dbapi_hook import DbApiHook

class PrestoException(Exception):
    pass


class PrestoHook(DbApiHook):
    """PrestoHook"""
    conn_name_attr = 'presto_conn_id'
    default_conn_name = 'presto_default'

    def get_conn(self):
        """Returns a connection object"""
        db = self.get_connection(self.presto_conn_id)
        reqkwargs = None
        if db.password is not None:
            reqkwargs = {'auth': HTTPBasicAuth(db.login, db.password)}
        return presto.connect(host=(db.host),
          port=(db.port),
          username=(db.login),
          source=(db.extra_dejson.get('source', 'airflow')),
          protocol=(db.extra_dejson.get('protocol', 'http')),
          catalog=(db.extra_dejson.get('catalog', 'hive')),
          requests_kwargs=reqkwargs,
          schema=(db.schema))

    @staticmethod
    def _strip_sql(sql):
        return sql.strip().rstrip(';')

    @staticmethod
    def _get_pretty_exception_message(e):
        """
        Parses some DatabaseError to provide a better error message
        """
        if hasattr(e, 'message'):
            if 'errorName' in e.message:
                if 'message' in e.message:
                    return '{name}: {message}'.format(name=(e.message['errorName']),
                      message=(e.message['message']))
        return str(e)

    def get_records(self, hql, parameters=None):
        """
        Get a set of records from Presto
        """
        try:
            return super(PrestoHook, self).get_records(self._strip_sql(hql), parameters)
        except DatabaseError as e:
            raise PrestoException(self._get_pretty_exception_message(e))

    def get_first(self, hql, parameters=None):
        """
        Returns only the first row, regardless of how many rows the query
        returns.
        """
        try:
            return super(PrestoHook, self).get_first(self._strip_sql(hql), parameters)
        except DatabaseError as e:
            raise PrestoException(self._get_pretty_exception_message(e))

    def get_pandas_df(self, hql, parameters=None):
        """
        Get a pandas dataframe from a sql query.
        """
        import pandas
        cursor = self.get_cursor()
        try:
            cursor.execute(self._strip_sql(hql), parameters)
            data = cursor.fetchall()
        except DatabaseError as e:
            raise PrestoException(self._get_pretty_exception_message(e))

        column_descriptions = cursor.description
        if data:
            df = pandas.DataFrame(data)
            df.columns = [c[0] for c in column_descriptions]
        else:
            df = pandas.DataFrame()
        return df

    def run(self, hql, parameters=None):
        """
        Execute the statement against Presto. Can be used to create views.
        """
        return super(PrestoHook, self).run(self._strip_sql(hql), parameters)

    def insert_rows(self, table, rows, target_fields=None):
        """
        A generic way to insert a set of tuples into a table.

        :param table: Name of the target table
        :type table: str
        :param rows: The rows to insert into the table
        :type rows: iterable of tuples
        :param target_fields: The names of the columns to fill in the table
        :type target_fields: iterable of strings
        """
        super(PrestoHook, self).insert_rows(table, rows, target_fields, 0)