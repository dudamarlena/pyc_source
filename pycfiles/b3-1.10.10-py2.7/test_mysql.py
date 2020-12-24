# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\core\storage\test_mysql.py
# Compiled at: 2016-03-08 18:42:10
import os, nose, unittest2 as unittest
from b3.functions import splitDSN
from b3.storage.mysql import MysqlStorage
from tests import B3TestCase
from tests.core.storage.common import StorageAPITest
MYSQL_TEST_HOST = os.environ.get('MYSQL_TEST_HOST', 'localhost')
MYSQL_TEST_USER = os.environ.get('MYSQL_TEST_USER', 'b3test')
MYSQL_TEST_PASSWORD = os.environ.get('MYSQL_TEST_PASSWORD', 'test')
MYSQL_TEST_DB = os.environ.get('MYSQL_TEST_DB', 'b3_test')
is_mysql_ready = True
no_mysql_reason = ''
try:
    import pymysql as driver
except ImportError:
    try:
        import mysql.connector as driver
    except ImportError:
        driver = None
        is_mysql_ready = False
        no_mysql_reason = 'no pymysql or mysql.connector module available'

if is_mysql_ready:
    try:
        driver.connect(host=MYSQL_TEST_HOST, user=MYSQL_TEST_USER, passwd=MYSQL_TEST_PASSWORD)
    except driver.Error as err:
        is_mysql_ready = False
        no_mysql_reason = '%s' % err[1]
    except Exception as err:
        is_mysql_ready = False
        no_mysql_reason = '%s' % err

@unittest.skipIf(not is_mysql_ready, no_mysql_reason)
class Test_MySQL(B3TestCase, StorageAPITest):

    def setUp(self):
        """this method is called before each test"""
        B3TestCase.setUp(self)
        try:
            db = driver.connect(host=MYSQL_TEST_HOST, user=MYSQL_TEST_USER, password=MYSQL_TEST_PASSWORD)
        except driver.OperationalError as message:
            self.fail('Error %d:\n%s' % (message[0], message[1]))

        db.query('DROP DATABASE IF EXISTS `%s`' % MYSQL_TEST_DB)
        db.query('CREATE DATABASE `%s` CHARACTER SET utf8;' % MYSQL_TEST_DB)
        dsn = 'mysql://%s:%s@%s/%s' % (MYSQL_TEST_USER, MYSQL_TEST_PASSWORD, MYSQL_TEST_HOST, MYSQL_TEST_DB)
        self.storage = self.console.storage = MysqlStorage(dsn, splitDSN(dsn), self.console)
        self.storage.connect()

    def tearDown(self):
        """this method is called after each test"""
        B3TestCase.tearDown(self)
        self.storage.query('DROP DATABASE `%s`' % MYSQL_TEST_DB)
        self.storage.shutdown()

    def test_getTables(self):
        self.assertSetEqual(set([
         'aliases',
         'ipaliases',
         'clients',
         'groups',
         'penalties',
         'data']), set(self.storage.getTables()))


if __name__ == '__main__':
    nose.main()