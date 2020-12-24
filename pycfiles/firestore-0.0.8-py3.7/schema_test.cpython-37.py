# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/containers/schema_test.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 581 bytes
from unittest import TestCase
from firestore import Collection, String, Integer, Reference, Map, Array, MapSchema

class SchemaCollection(Collection):
    __schema__ = [
     'name']


class NoneSchemaCollection(Collection):
    pass


class SchemaTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_schema_is_none(self):
        nsc = NoneSchemaCollection()
        self.assertIsNone(nsc.__schema__)

    def test_schema_is_not_none(self):
        sc = SchemaCollection()
        self.assertIsNotNone(sc.get_json_schema())