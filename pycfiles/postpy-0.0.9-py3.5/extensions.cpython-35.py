# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/postpy/extensions.py
# Compiled at: 2017-02-01 10:25:44
# Size of source mod 2**32: 999 bytes
import psycopg2
from psycopg2._psycopg import AsIs

def install_extension(conn, extension: str):
    """Install Postgres extension."""
    query = 'CREATE EXTENSION IF NOT EXISTS "%s";'
    with conn.cursor() as (cursor):
        cursor.execute(query, (AsIs(extension),))
    installed = check_extension(conn, extension)
    if not installed:
        raise psycopg2.ProgrammingError('Postgres extension failed installation.', extension)


def check_extension(conn, extension: str) -> bool:
    """Check to see if an extension is installed."""
    query = 'SELECT installed_version FROM pg_available_extensions WHERE name=%s;'
    with conn.cursor() as (cursor):
        cursor.execute(query, (extension,))
        result = cursor.fetchone()
    if result is None:
        raise psycopg2.ProgrammingError('Extension is not available for installation.', extension)
    else:
        extension_version = result[0]
        return bool(extension_version)