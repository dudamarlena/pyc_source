# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/connection.py
# Compiled at: 2011-01-01 23:58:31
import unittest
from mongate.connection import Connection, ConnectionError
from tests import SLEEPY_HOST, SLEEPY_PORT, MONGO_HOST, MONGO_PORT

class TestConnection(unittest.TestCase):

    def setUp(self):
        pass

    def test_connection_initialized_properly(self):
        connection = Connection('localhost', 27080)
        self.assertEqual(27080, connection.get_port())
        self.assertEqual('localhost', connection.get_host())

    def test_connection_should_return_db_when_array_access_used(self):
        connection = Connection('localhost', '27080')
        db = connection['foo']
        self.assertEqual('foo', db.get_name())

    def test_connection_should_return_db_when_attribute_access_used(self):
        connection = Connection('localhost', '27080')
        db = connection.foo
        self.assertEqual('foo', db.get_name())

    def test_connect_to_mongo_with_invalid_host(self):
        connection = Connection('localhostgggg', 27080)
        error_occurred = False
        try:
            connection.connect_to_mongo(host='localhost', port=27017)
        except ConnectionError:
            error_occurred = True

        self.assertTrue(error_occurred)

    def test_connect_to_mongo_with_valid_info(self):
        connection = Connection(SLEEPY_HOST, SLEEPY_PORT)
        self.assertTrue(connection.connect_to_mongo(host=MONGO_HOST, port=MONGO_PORT))


if __name__ == '__main__':
    unittest.main()