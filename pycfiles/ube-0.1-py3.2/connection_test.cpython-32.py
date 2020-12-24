# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ube/concerns/tests/connection_test.py
# Compiled at: 2013-09-01 17:36:06
"""
Created on Nov 6, 2012

@author: Nicklas Boerjesson
"""
import unittest
from qal.dal.tests.framework import default_dal
from ube.concerns.connection import set_connection, connection
from qal.dal.dal_types import DB_POSTGRESQL
test_sql = 'SELECT 1'

@default_dal(DB_POSTGRESQL)
class concern_connection_tests(unittest.TestCase):
    _dal = None

    def setUp(self):
        set_connection(self._dal)

    def tearDown(self):
        pass

    @connection
    def test_function_connection(self, _connection=None):
        _connection.execute(test_sql)

    def test_class_connection(self, _connection=None):
        """ This import has to be done here and the decorated class has to be in a separate module. 
        For some stupid reason, the decorator is called on import."""
        from .connection_check_c import connection_check_class
        test_class = connection_check_class()
        test_class.connection_check(test_sql)


if __name__ == '__main__':
    unittest.main()