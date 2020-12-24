# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/dbpg/postgres.py
# Compiled at: 2020-05-05 20:41:57
# Size of source mod 2**32: 5378 bytes
"""Postgres implementation of the ``ConnectionManager``.

"""
__author__ = 'Paul Landes'
from dataclasses import dataclass, field
import logging, psycopg2
from psycopg2.extras import RealDictCursor
from zensols.db import DbPersister, ConnectionManager
logger = logging.getLogger(__name__)

@dataclass
class PostgresConnectionManager(ConnectionManager):
    __doc__ = 'An Postgres connection factory.\n\n    :param persister: the persister that will use this connection factory\n                      (needed to get the initialization DDL SQL)\n\n    :param db_name: database name on the server\n    :param host: the host name of the database\n    :param port: the host port of the database\n    :param user: the user (if any) to log in with\n    :param password: the login password\n    :param create_db: if ``True`` create the database if it does not already exist\n    :param capture_lastrowid: if ``True``, select the last row for each query\n    :param fast_insert: if ``True`` use `insertmany` on the cursor for fast\n                        insert in to the database\n\n    '
    EXISTS_SQL = "select count(*) from information_schema.tables where table_schema = 'public'"
    DROP_SQL = 'drop owned by {user}'
    db_name: str
    host: str
    port: str
    user: str
    password: str
    create_db = field(default=True)
    create_db: bool
    capture_lastrowid = field(default=False)
    capture_lastrowid: bool
    fast_insert = field(default=False)
    fast_insert: bool

    def _init_db(self, conn, cur):
        logger.info('initializing database...')
        for sql in self.persister.parser.get_init_db_sqls():
            logger.debug(f"invoking sql: {sql}")
            cur.execute(sql)
            conn.commit()

    def create(self):
        logger.debug(f"creating connection to {self.host}:{self.port} with " + f"{self.user} on database: {self.db_name}")
        conn = psycopg2.connect(host=(self.host),
          database=(self.db_name),
          port=(self.port),
          user=(self.user),
          password=(self.password))
        try:
            cur = conn.cursor()
            cur.execute(self.EXISTS_SQL, ())
            if cur.fetchone()[0] == 0:
                self._init_db(conn, cur)
        finally:
            cur.close()

        return conn

    def drop(self):
        conn = self.create()
        cur = conn.cursor()
        try:
            cur.execute((self.DROP_SQL.format)(**self.__dict__))
            conn.commit()
        finally:
            cur.close()
            conn.close()

    def execute(self, conn, sql, params, row_factory, map_fn):
        """See ``DbPersister.execute``.

        """

        def other_rf_fn(row):
            return row_factory(*row)

        create_fn = None
        if row_factory == 'dict':
            cur = conn.cursor(cursor_factory=RealDictCursor)
        else:
            if row_factory == 'tuple':
                cur = conn.cursor()
            else:
                create_fn = other_rf_fn
                cur = conn.cursor()
        try:
            cur.execute(sql, params)
            res = cur.fetchall()
            if create_fn is not None:
                res = map(create_fn, res)
            if map_fn is not None:
                res = map(map_fn, res)
            return tuple(res)
        finally:
            cur.close()

    def execute_no_read(self, conn, sql, params=()) -> int:
        cur = conn.cursor()
        logger.debug(f"execute no read: {sql}")
        try:
            cur.execute(sql, params)
            conn.commit()
            if self.capture_lastrowid:
                return cur.fetchone()[0]
        finally:
            cur.close()

    def _insert_row(self, conn, cur, sql, row):
        cur.execute(sql, row)
        conn.commit()
        if self.capture_lastrowid:
            return cur.fetchall()[0][0]

    def _insert_rows_slow(self, conn, sql, rows: list, errors: str, set_id_fn, map_fn) -> int:
        rowid = None
        cur = conn.cursor()
        try:
            for row in rows:
                if map_fn is not None:
                    org_row = row
                    row = map_fn(row)
                elif errors == 'raise':
                    rowid = self._insert_row(conn, cur, sql, row)
                else:
                    if errors == 'ignore':
                        try:
                            rowid = self._insert_row(conn, cur, sql, row)
                        except Exception as e:
                            try:
                                logger.error(f"could not insert row ({len(row)})", e)
                            finally:
                                e = None
                                del e

                    else:
                        raise ValueError(f"unknown errors value: {errors}")
                if set_id_fn is not None:
                    set_id_fn(org_row, cur.lastrowid)

        finally:
            cur.close()

        logger.debug(f"inserted with rowid: {rowid}")
        return rowid

    def _insert_rows_fast(self, conn, sql, rows: list, map_fn) -> int:
        cur = conn.cursor()
        logger.debug('inserting rows fast')
        try:
            if map_fn is not None:
                rows = map(map_fn, rows)
            cur.executemany(sql, rows)
            conn.commit()
        finally:
            cur.close()

    def insert_rows(self, conn, sql, rows: list, errors: str, set_id_fn, map_fn) -> int:
        if self.fast_insert:
            return self._insert_rows_fast(conn, sql, rows, map_fn)
        return self._insert_rows_slow(conn, sql, rows, errors, set_id_fn, map_fn)