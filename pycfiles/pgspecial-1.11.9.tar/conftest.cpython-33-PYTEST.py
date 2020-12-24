# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/irina/src/pgspecial/tests/conftest.py
# Compiled at: 2016-06-20 18:05:41
# Size of source mod 2**32: 894 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from dbutils import create_db, db_connection, setup_db, teardown_db
from pgspecial.main import PGSpecial

@pytest.yield_fixture(scope='module')
def connection():
    create_db('_test_db')
    connection = db_connection('_test_db')
    setup_db(connection)
    yield connection
    teardown_db(connection)
    connection.close()


@pytest.fixture
def cursor(connection):
    with connection.cursor() as (cur):
        return cur


@pytest.fixture
def executor(connection):
    cur = connection.cursor()
    pgspecial = PGSpecial()

    def query_runner(sql):
        results = []
        for title, rows, headers, status in pgspecial.execute(cur=cur, sql=sql):
            if rows:
                results.extend((title, list(rows), headers, status))
            else:
                results.extend((title, None, headers, status))

        return results

    return query_runner