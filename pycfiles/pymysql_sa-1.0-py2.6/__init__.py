# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/__init__.py
# Compiled at: 2010-12-01 13:27:58
import unittest

class TestDialect(unittest.TestCase):

    def runTest(self):
        from sqlalchemy import create_engine
        engine = create_engine('pymysql://root@localhost/test')
        self.assertEqual(engine.dialect.name, 'mysql')
        self.assertEqual(engine.driver, 'pymysql')


class TestDialectAsDefault(unittest.TestCase):

    def runTest(self):
        import pymysql_sa
        pymysql_sa.make_default_mysql_dialect()
        from sqlalchemy import create_engine
        engine = create_engine('mysql://root@localhost/test')
        self.assertEqual(engine.dialect.name, 'mysql')
        self.assertEqual(engine.driver, 'pymysql')


all_tests = unittest.TestSuite([TestDialect(), TestDialectAsDefault()])