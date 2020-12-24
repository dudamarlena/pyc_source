# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/datatypes/array_test.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 871 bytes
from unittest import TestCase
from firestore import Array, Collection
from firestore.containers.collection import Cache
from firestore.errors import ValidationError

class ArrayDocument(Collection):
    children_ages = Array(minimum=3, maximum=5)


class TestArray(TestCase):

    def setUp(self):
        self.ad = ArrayDocument()
        self._ = [5, 10, 'Yes', True]

    def tearDown(self):
        pass

    def test_array_in_collection_document(self):
        self.ad.children_ages = self._
        cache = Cache()
        cache.add('children_ages', self._)
        self.assertEqual(self.ad._data, cache)

    def test_array_boundary_exceptions(self):
        with self.assertRaises(ValidationError):
            self.ad.children_ages = self._ + ['You', None]
        with self.assertRaises(ValidationError):
            self.ad.children_ages = [
             'a']