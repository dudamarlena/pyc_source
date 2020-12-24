# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/immutable_collection/collection_test.py
# Compiled at: 2018-07-25 10:04:16
import unittest
from six import iteritems
from collections import namedtuple
from immutable_collection import ImmutableCollection
from immutable_collection.collection import merge_dict

class ImmutableCollection_Test(unittest.TestCase):
    """Tests for `collection.py`."""
    dict_a = {'key1': 'val1'}
    dict_b = {'key2': 'val2'}
    dict_m = {'key1': 'val1', 'key2': 'val2'}

    def test_merge_dict(self):
        """Test the merge_dict method"""
        self.assertIsInstance(merge_dict(self.dict_a, self.dict_b), dict)

    def test_merge_dict_w_path(self):
        """Test merge_dict path parameter"""
        self.assertIsInstance(merge_dict(self.dict_a, self.dict_b, path=['one', 'two']), dict)

    def test_create_collection_data(self):
        """Test creating a new collection with data"""
        self.assertIsInstance(ImmutableCollection.create(self.dict_a), tuple)

    def test_create_collection_map_data(self):
        """Test creating and mapping additional data to a collection"""
        collection = ImmutableCollection(self.dict_a)
        self.assertTrue(collection.map(self.dict_b), self.dict_m)
        self.assertFalse(collection.map({}))
        self.assertIsInstance(collection.get(), tuple)

    def test_collection_map_data_structure(self):
        """Make sure data structure is what we expect post-merge"""
        collection = ImmutableCollection(self.dict_a)
        collection.map(self.dict_b)
        merged = collection.get()
        for k, v in iteritems(self.dict_m):
            self.assertEqual(v, getattr(merged, k, None))

        return


if __name__ == '__main__':
    unittest.main()