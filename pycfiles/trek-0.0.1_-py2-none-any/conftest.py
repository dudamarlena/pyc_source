# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/brian.hicks/code/oss/migrate/build/lib/tests/runners/conftest.py
# Compiled at: 2014-10-06 14:43:12
import pytest
from psycopg2 import connect
import os

@pytest.fixture(scope='session')
def postgres_info():
    return {'database': os.environ.get('PGDATABASE', 'trek_test'), 
       'host': os.environ.get('PGHOST', 'localhost'), 
       'port': int(os.environ.get('PGPORT', '5432')), 
       'user': os.environ.get('PGUSER', 'trek_test'), 
       'password': os.environ.get('PGPASSWORD', None)}


@pytest.yield_fixture(scope='session')
def connection(postgres_info):
    conn = connect(**postgres_info)
    yield conn
    conn.close()


@pytest.yield_fixture
def cursor(connection):
    cur = connection.cursor()
    yield cur
    cur.close()