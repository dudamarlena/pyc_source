# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\core\storage\test_postgresql.py
# Compiled at: 2016-03-08 18:42:10
import os, nose, unittest2 as unittest
from b3.functions import splitDSN
from b3.storage.postgresql import PostgresqlStorage
from tests import B3TestCase
from tests.core.storage.common import StorageAPITest
POSTGRESQL_TEST_HOST = os.environ.get('POSTGRESQL_TEST_HOST', 'localhost')
POSTGRESQL_TEST_USER = os.environ.get('POSTGRESQL_TEST_USER', 'b3test')
POSTGRESQL_TEST_PASSWORD = os.environ.get('POSTGRESQL_TEST_PASSWORD', 'test')
POSTGRESQL_TEST_DB = os.environ.get('POSTGRESQL_TEST_DB', 'b3_test')
is_postgresql_ready = True
no_postgresql_reason = ''
try:
    import psycopg2
except ImportError:
    psycopg2 = None
    is_postgresql_ready = False
    no_postgresql_reason = 'no psycopg2 module available'
else:
    try:
        psycopg2.connect(host=POSTGRESQL_TEST_HOST, user=POSTGRESQL_TEST_USER, password=POSTGRESQL_TEST_PASSWORD, database='postgres')
    except psycopg2.Error as err:
        is_postgresql_ready = False
        no_postgresql_reason = '%r' % err
    except Exception as err:
        is_postgresql_ready = False
        no_postgresql_reason = '%r' % err

@unittest.skipIf(not is_postgresql_ready, no_postgresql_reason)
class Test_PostgreSQL(B3TestCase, StorageAPITest):

    def setUp(self):
        """this method is called before each test"""
        B3TestCase.setUp(self)
        try:
            dsn = 'postgresql://%s:%s@%s/%s' % (POSTGRESQL_TEST_USER, POSTGRESQL_TEST_PASSWORD, POSTGRESQL_TEST_HOST, POSTGRESQL_TEST_DB)
            self.storage = self.console.storage = PostgresqlStorage(dsn, splitDSN(dsn), self.console)
            self.storage.connect()
            tables = self.storage.getTables()
            if tables:
                tables.remove('groups')
                self.storage.truncateTable(tables)
        except Exception as e:
            self.fail('Error: %s' % e)

    def tearDown(self):
        """this method is called after each test"""
        B3TestCase.tearDown(self)
        self.storage.shutdown()


if __name__ == '__main__':
    nose.main()