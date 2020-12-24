# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/postpy/sql.py
# Compiled at: 2017-01-31 21:59:16
# Size of source mod 2**32: 3006 bytes
from contextlib import closing
from typing import Iterable
import psycopg2
from psycopg2.extras import NamedTupleCursor, RealDictCursor
from postpy import connect

def execute_transaction(conn, statements: Iterable):
    """Execute several statements in single DB transaction."""
    with conn:
        with conn.cursor() as (cursor):
            for statement in statements:
                cursor.execute(statement)

        conn.commit()


def execute_transactions(conn, statements: Iterable):
    """Execute several statements each as a single DB transaction."""
    with conn.cursor() as (cursor):
        for statement in statements:
            try:
                cursor.execute(statement)
                conn.commit()
            except psycopg2.ProgrammingError:
                conn.rollback()


def execute_closing_transaction(statements: Iterable):
    """Open a connection, commit a transaction, and close it."""
    with closing(connect()) as (conn):
        with conn.cursor() as (cursor):
            for statement in statements:
                cursor.execute(statement)


def select(conn, query: str, params=None,
           name=None, itersize=5000):
    """Return a select statement's results as a namedtuple.

    Parameters
    ----------
    conn : database connection
    query : select query string
    params : query parameters.
    name : server side cursor name. defaults to client side.
    itersize : number of records fetched by server.
    """
    with conn.cursor(name, cursor_factory=NamedTupleCursor) as (cursor):
        cursor.itersize = itersize
        cursor.execute(query, params)
        for result in cursor:
            yield result


def select_dict(conn, query: str, params=None, name=None, itersize=5000):
    """Return a select statement's results as dictionary.

    Parameters
    ----------
    conn : database connection
    query : select query string
    params : query parameters.
    name : server side cursor name. defaults to client side.
    itersize : number of records fetched by server.
    """
    with conn.cursor(name, cursor_factory=RealDictCursor) as (cursor):
        cursor.itersize = itersize
        cursor.execute(query, params)
        for result in cursor:
            yield result


def select_each(conn, query: str, parameter_groups, name=None):
    """Run select query for each parameter set in single transaction."""
    with conn:
        with conn.cursor(name=name) as (cursor):
            for parameters in parameter_groups:
                cursor.execute(query, parameters)
                yield cursor.fetchone()


def query_columns(conn, query, name=None):
    """Lightweight query to retrieve column list of select query.

    Notes
    -----
    Strongly urged to specify a cursor name for performance.
    """
    with conn.cursor(name) as (cursor):
        cursor.itersize = 1
        cursor.execute(query)
        cursor.fetchmany(0)
        column_names = [column.name for column in cursor.description]
    return column_names