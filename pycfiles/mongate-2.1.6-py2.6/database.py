# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/database.py
# Compiled at: 2011-01-01 21:21:26
import unittest
from mongate.connection import Connection
from mongate.database import Database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.connection = Connection('localhost', '27080')

    def test_db_should_return_collection_when_array_access_used(self):
        db = self.connection['foo']
        collection = db['bar']
        self.assertEqual('bar', collection.name)

    def test_db_should_return_collection_when_attribute_access_used(self):
        db = self.connection.foo
        collection = db.bar
        self.assertEqual('bar', collection.name)

    def test_drop_collection(self):
        db = self.connection.foo
        collection = db.test_collection
        collection.insert({'name': 'Benjamin & Company', 
           'profession': 'Software Developer?'})
        db.drop_collection('test_collection')
        retrieved_collection = collection.find({'name': 'Benjamin & Company'})
        self.assertFalse(retrieved_collection)


if __name__ == '__main__':
    unittest.main()