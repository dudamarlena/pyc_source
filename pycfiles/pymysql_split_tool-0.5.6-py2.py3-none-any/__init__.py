# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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