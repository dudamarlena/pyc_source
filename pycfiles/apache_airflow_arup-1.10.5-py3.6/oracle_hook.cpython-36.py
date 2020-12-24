# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/hooks/oracle_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 9816 bytes
import cx_Oracle
from airflow.hooks.dbapi_hook import DbApiHook
from builtins import str
from past.builtins import basestring
from datetime import datetime
import numpy

class OracleHook(DbApiHook):
    __doc__ = '\n    Interact with Oracle SQL.\n    '
    conn_name_attr = 'oracle_conn_id'
    default_conn_name = 'oracle_default'
    supports_autocommit = False

    def get_conn(self):
        """
        Returns a oracle connection object
        Optional parameters for using a custom DSN connection
        (instead of using a server alias from tnsnames.ora)
        The dsn (data source name) is the TNS entry
        (from the Oracle names server or tnsnames.ora file)
        or is a string like the one returned from makedsn().

        :param dsn: the host address for the Oracle server
        :param service_name: the db_unique_name of the database
              that you are connecting to (CONNECT_DATA part of TNS)

        You can set these parameters in the extra fields of your connection
        as in ``{ "dsn":"some.host.address" , "service_name":"some.service.name" }``
        see more param detail in
        `cx_Oracle.connect <https://cx-oracle.readthedocs.io/en/latest/module.html#cx_Oracle.connect>`_
        """
        conn = self.get_connection(self.oracle_conn_id)
        conn_config = {'user':conn.login, 
         'password':conn.password}
        dsn = conn.extra_dejson.get('dsn', None)
        sid = conn.extra_dejson.get('sid', None)
        mod = conn.extra_dejson.get('module', None)
        service_name = conn.extra_dejson.get('service_name', None)
        port = conn.port if conn.port else 1521
        if dsn:
            if sid:
                if not service_name:
                    conn_config['dsn'] = cx_Oracle.makedsn(dsn, port, sid)
        elif dsn:
            if service_name:
                if not sid:
                    conn_config['dsn'] = cx_Oracle.makedsn(dsn, port, service_name=service_name)
        else:
            conn_config['dsn'] = conn.host
        if 'encoding' in conn.extra_dejson:
            conn_config['encoding'] = conn.extra_dejson.get('encoding')
            if 'nencoding' not in conn.extra_dejson:
                conn_config['nencoding'] = conn.extra_dejson.get('encoding')
        if 'nencoding' in conn.extra_dejson:
            conn_config['nencoding'] = conn.extra_dejson.get('nencoding')
        if 'threaded' in conn.extra_dejson:
            conn_config['threaded'] = conn.extra_dejson.get('threaded')
        if 'events' in conn.extra_dejson:
            conn_config['events'] = conn.extra_dejson.get('events')
        mode = conn.extra_dejson.get('mode', '').lower()
        if mode == 'sysdba':
            conn_config['mode'] = cx_Oracle.SYSDBA
        else:
            if mode == 'sysasm':
                conn_config['mode'] = cx_Oracle.SYSASM
            else:
                if mode == 'sysoper':
                    conn_config['mode'] = cx_Oracle.SYSOPER
                else:
                    if mode == 'sysbkp':
                        conn_config['mode'] = cx_Oracle.SYSBKP
                    else:
                        if mode == 'sysdgd':
                            conn_config['mode'] = cx_Oracle.SYSDGD
                        else:
                            if mode == 'syskmt':
                                conn_config['mode'] = cx_Oracle.SYSKMT
                            else:
                                if mode == 'sysrac':
                                    conn_config['mode'] = cx_Oracle.SYSRAC
                    purity = conn.extra_dejson.get('purity', '').lower()
                    if purity == 'new':
                        conn_config['purity'] = cx_Oracle.ATTR_PURITY_NEW
                    else:
                        if purity == 'self':
                            conn_config['purity'] = cx_Oracle.ATTR_PURITY_SELF
                        elif purity == 'default':
                            conn_config['purity'] = cx_Oracle.ATTR_PURITY_DEFAULT
        conn = (cx_Oracle.connect)(**conn_config)
        if mod is not None:
            conn.module = mod
        return conn

    def insert_rows(self, table, rows, target_fields=None, commit_every=1000):
        """
        A generic way to insert a set of tuples into a table,
        the whole set of inserts is treated as one transaction
        Changes from standard DbApiHook implementation:

        - Oracle SQL queries in cx_Oracle can not be terminated with a semicolon (`;`)
        - Replace NaN values with NULL using `numpy.nan_to_num` (not using
          `is_nan()` because of input types error for strings)
        - Coerce datetime cells to Oracle DATETIME format during insert

        :param table: target Oracle table, use dot notation to target a
            specific database
        :type table: str
        :param rows: the rows to insert into the table
        :type rows: iterable of tuples
        :param target_fields: the names of the columns to fill in the table
        :type target_fields: iterable of str
        :param commit_every: the maximum number of rows to insert in one transaction
            Default 1000, Set greater than 0.
            Set 1 to insert each row in each single transaction
        :type commit_every: int
        """
        if target_fields:
            target_fields = ', '.join(target_fields)
            target_fields = '({})'.format(target_fields)
        else:
            target_fields = ''
        conn = self.get_conn()
        cur = conn.cursor()
        if self.supports_autocommit:
            cur.execute('SET autocommit = 0')
        conn.commit()
        i = 0
        for row in rows:
            i += 1
            lst = []
            for cell in row:
                if isinstance(cell, basestring):
                    lst.append("'" + str(cell).replace("'", "''") + "'")
                elif cell is None:
                    lst.append('NULL')
                elif type(cell) == float and numpy.isnan(cell):
                    lst.append('NULL')
                else:
                    if isinstance(cell, numpy.datetime64):
                        lst.append("'" + str(cell) + "'")
                    else:
                        if isinstance(cell, datetime):
                            lst.append("to_date('" + cell.strftime('%Y-%m-%d %H:%M:%S') + "','YYYY-MM-DD HH24:MI:SS')")
                        else:
                            lst.append(str(cell))

            values = tuple(lst)
            sql = 'INSERT /*+ APPEND */ INTO {0} {1} VALUES ({2})'.format(table, target_fields, ','.join(values))
            cur.execute(sql)
            if i % commit_every == 0:
                conn.commit()
                self.log.info('Loaded %s into %s rows so far', i, table)

        conn.commit()
        cur.close()
        conn.close()
        self.log.info('Done loading. Loaded a total of %s rows', i)

    def bulk_insert_rows(self, table, rows, target_fields=None, commit_every=5000):
        """
        A performant bulk insert for cx_Oracle
        that uses prepared statements via `executemany()`.
        For best performance, pass in `rows` as an iterator.

        :param table: target Oracle table, use dot notation to target a
            specific database
        :type table: str
        :param rows: the rows to insert into the table
        :type rows: iterable of tuples
        :param target_fields: the names of the columns to fill in the table, default None.
            If None, each rows should have some order as table columns name
        :type target_fields: iterable of str Or None
        :param commit_every: the maximum number of rows to insert in one transaction
            Default 5000. Set greater than 0. Set 1 to insert each row in each transaction
        :type commit_every: int
        """
        if not rows:
            raise ValueError('parameter rows could not be None or empty iterable')
        conn = self.get_conn()
        cursor = conn.cursor()
        values_base = target_fields if target_fields else rows[0]
        prepared_stm = 'insert into {tablename} {columns} values ({values})'.format(tablename=table,
          columns=('({})'.format(', '.join(target_fields)) if target_fields else ''),
          values=(', '.join(':%s' % i for i in range(1, len(values_base) + 1))))
        row_count = 0
        row_chunk = []
        for row in rows:
            row_chunk.append(row)
            row_count += 1
            if row_count % commit_every == 0:
                cursor.prepare(prepared_stm)
                cursor.executemany(None, row_chunk)
                conn.commit()
                self.log.info('[%s] inserted %s rows', table, row_count)
                row_chunk = []

        cursor.prepare(prepared_stm)
        cursor.executemany(None, row_chunk)
        conn.commit()
        self.log.info('[%s] inserted %s rows', table, row_count)
        cursor.close()
        conn.close()