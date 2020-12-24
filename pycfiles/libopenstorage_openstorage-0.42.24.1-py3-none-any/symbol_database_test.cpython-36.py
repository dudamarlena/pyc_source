# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/internal/symbol_database_test.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 5650 bytes
"""Tests for google.protobuf.symbol_database."""
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from google.protobuf import unittest_pb2
from google.protobuf import descriptor
from google.protobuf import descriptor_pool
from google.protobuf import symbol_database

class SymbolDatabaseTest(unittest.TestCase):

    def _Database(self):
        if descriptor._USE_C_DESCRIPTORS:
            db = symbol_database.SymbolDatabase(pool=(descriptor_pool.Default()))
        else:
            db = symbol_database.SymbolDatabase()
        db.RegisterFileDescriptor(unittest_pb2.DESCRIPTOR)
        db.RegisterMessage(unittest_pb2.TestAllTypes)
        db.RegisterMessage(unittest_pb2.TestAllTypes.NestedMessage)
        db.RegisterMessage(unittest_pb2.TestAllTypes.OptionalGroup)
        db.RegisterMessage(unittest_pb2.TestAllTypes.RepeatedGroup)
        db.RegisterEnumDescriptor(unittest_pb2.ForeignEnum.DESCRIPTOR)
        db.RegisterEnumDescriptor(unittest_pb2.TestAllTypes.NestedEnum.DESCRIPTOR)
        db.RegisterServiceDescriptor(unittest_pb2._TESTSERVICE)
        return db

    def testGetPrototype(self):
        instance = self._Database().GetPrototype(unittest_pb2.TestAllTypes.DESCRIPTOR)
        self.assertTrue(instance is unittest_pb2.TestAllTypes)

    def testGetMessages(self):
        messages = self._Database().GetMessages([
         'google/protobuf/unittest.proto'])
        self.assertTrue(unittest_pb2.TestAllTypes is messages['protobuf_unittest.TestAllTypes'])

    def testGetSymbol(self):
        self.assertEqual(unittest_pb2.TestAllTypes, self._Database().GetSymbol('protobuf_unittest.TestAllTypes'))
        self.assertEqual(unittest_pb2.TestAllTypes.NestedMessage, self._Database().GetSymbol('protobuf_unittest.TestAllTypes.NestedMessage'))
        self.assertEqual(unittest_pb2.TestAllTypes.OptionalGroup, self._Database().GetSymbol('protobuf_unittest.TestAllTypes.OptionalGroup'))
        self.assertEqual(unittest_pb2.TestAllTypes.RepeatedGroup, self._Database().GetSymbol('protobuf_unittest.TestAllTypes.RepeatedGroup'))

    def testEnums(self):
        self.assertEqual('protobuf_unittest.ForeignEnum', self._Database().pool.FindEnumTypeByName('protobuf_unittest.ForeignEnum').full_name)
        self.assertEqual('protobuf_unittest.TestAllTypes.NestedEnum', self._Database().pool.FindEnumTypeByName('protobuf_unittest.TestAllTypes.NestedEnum').full_name)

    def testFindMessageTypeByName(self):
        self.assertEqual('protobuf_unittest.TestAllTypes', self._Database().pool.FindMessageTypeByName('protobuf_unittest.TestAllTypes').full_name)
        self.assertEqual('protobuf_unittest.TestAllTypes.NestedMessage', self._Database().pool.FindMessageTypeByName('protobuf_unittest.TestAllTypes.NestedMessage').full_name)

    def testFindServiceByName(self):
        self.assertEqual('protobuf_unittest.TestService', self._Database().pool.FindServiceByName('protobuf_unittest.TestService').full_name)

    def testFindFileContainingSymbol(self):
        self.assertEqual('google/protobuf/unittest.proto', self._Database().pool.FindFileContainingSymbol('protobuf_unittest.TestAllTypes.NestedEnum').name)
        self.assertEqual('google/protobuf/unittest.proto', self._Database().pool.FindFileContainingSymbol('protobuf_unittest.TestAllTypes').name)

    def testFindFileByName(self):
        self.assertEqual('google/protobuf/unittest.proto', self._Database().pool.FindFileByName('google/protobuf/unittest.proto').name)


if __name__ == '__main__':
    unittest.main()