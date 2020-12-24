# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/postpy/admin.py
# Compiled at: 2017-09-15 11:41:37
# Size of source mod 2**32: 2946 bytes
__doc__ = '\nDatabase administration queries\n'
import psycopg2
from postpy.base import Table, Column, Database, PrimaryKey
from postpy.ddl import compile_qualified_name
from postpy.extensions import install_extension
from postpy.sql import select_dict

def get_user_tables(conn):
    """Retrieve all user tables."""
    query_string = 'select schemaname, relname from pg_stat_user_tables;'
    with conn.cursor() as (cursor):
        cursor.execute(query_string)
        tables = cursor.fetchall()
    return tables


def get_primary_keys(conn, table: str, schema='public'):
    """Returns primary key columns for a specific table."""
    query = "SELECT\n  c.constraint_name AS pkey_constraint_name,\n  c.column_name     AS column_name\nFROM\n  information_schema.key_column_usage AS c\n  JOIN information_schema.table_constraints AS t\n    ON t.constraint_name = c.constraint_name\n       AND t.table_catalog = c.table_catalog\n       AND t.table_schema = c.table_schema\n       AND t.table_name = c.table_name\nWHERE t.constraint_type = 'PRIMARY KEY'\n  AND c.table_schema=%s\n  AND c.table_name=%s\nORDER BY c.ordinal_position"
    for record in select_dict(conn, query, params=(schema, table)):
        yield record['column_name']


def get_column_metadata(conn, table: str, schema='public'):
    """Returns column data following db.Column parameter specification."""
    query = 'SELECT\n  attname as name,\n  format_type(atttypid, atttypmod) AS data_type,\n  NOT attnotnull AS nullable\nFROM pg_catalog.pg_attribute\nWHERE attrelid=%s::regclass\n  AND attnum > 0 AND NOT attisdropped\nORDER BY attnum;'
    qualified_name = compile_qualified_name(table, schema=schema)
    for record in select_dict(conn, query, params=(qualified_name,)):
        yield record


def reflect_table(conn, table_name, schema='public'):
    """Reflect basic table attributes."""
    column_meta = list(get_column_metadata(conn, table_name, schema=schema))
    primary_key_columns = list(get_primary_keys(conn, table_name, schema=schema))
    columns = [Column(**column_data) for column_data in column_meta]
    primary_key = PrimaryKey(primary_key_columns)
    return Table(table_name, columns, primary_key, schema=schema)


def reset(db_name):
    """Reset database."""
    conn = psycopg2.connect(database='postgres')
    db = Database(db_name)
    conn.autocommit = True
    with conn.cursor() as (cursor):
        cursor.execute(db.drop_statement())
        cursor.execute(db.create_statement())
    conn.close()


def install_extensions(extensions, **connection_parameters):
    """Install Postgres extension if available.

    Notes
    -----
    - superuser is generally required for installing extensions.
    - Currently does not support specific schema.
    """
    from postpy.connections import connect
    conn = connect(**connection_parameters)
    conn.autocommit = True
    for extension in extensions:
        install_extension(conn, extension)