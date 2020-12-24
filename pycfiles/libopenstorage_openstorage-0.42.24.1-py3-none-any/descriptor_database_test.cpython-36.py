# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/internal/descriptor_database_test.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 6034 bytes
"""Tests for google.protobuf.descriptor_database."""
__author__ = 'matthewtoia@google.com (Matt Toia)'
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import warnings
from google.protobuf import unittest_pb2
from google.protobuf import descriptor_pb2
from google.protobuf.internal import factory_test2_pb2
from google.protobuf.internal import no_package_pb2
from google.protobuf.internal import testing_refleaks
from google.protobuf import descriptor_database

@testing_refleaks.TestCase
class DescriptorDatabaseTest(unittest.TestCase):

    def testAdd(self):
        db = descriptor_database.DescriptorDatabase()
        file_desc_proto = descriptor_pb2.FileDescriptorProto.FromString(factory_test2_pb2.DESCRIPTOR.serialized_pb)
        file_desc_proto2 = descriptor_pb2.FileDescriptorProto.FromString(no_package_pb2.DESCRIPTOR.serialized_pb)
        db.Add(file_desc_proto)
        db.Add(file_desc_proto2)
        self.assertEqual(file_desc_proto, db.FindFileByName('google/protobuf/internal/factory_test2.proto'))
        self.assertEqual(file_desc_proto, db.FindFileContainingSymbol('google.protobuf.python.internal.Factory2Message'))
        self.assertEqual(file_desc_proto, db.FindFileContainingSymbol('google.protobuf.python.internal.Factory2Message.NestedFactory2Message'))
        self.assertEqual(file_desc_proto, db.FindFileContainingSymbol('google.protobuf.python.internal.Factory2Enum'))
        self.assertEqual(file_desc_proto, db.FindFileContainingSymbol('google.protobuf.python.internal.Factory2Message.NestedFactory2Enum'))
        self.assertEqual(file_desc_proto, db.FindFileContainingSymbol('google.protobuf.python.internal.MessageWithNestedEnumOnly.NestedEnum'))
        self.assertEqual(file_desc_proto, db.FindFileContainingSymbol('google.protobuf.python.internal.Factory2Message.list_field'))
        self.assertEqual(file_desc_proto, db.FindFileContainingSymbol('google.protobuf.python.internal.Factory2Enum.FACTORY_2_VALUE_0'))
        self.assertEqual(file_desc_proto, db.FindFileContainingSymbol('google.protobuf.python.internal.FACTORY_2_VALUE_0'))
        self.assertEqual(file_desc_proto2, db.FindFileContainingSymbol('.NO_PACKAGE_VALUE_0'))
        self.assertEqual(file_desc_proto, db.FindFileContainingSymbol('google.protobuf.python.internal.another_field'))
        self.assertEqual(file_desc_proto, db.FindFileContainingSymbol('google.protobuf.python.internal.Factory2Message.one_more_field'))
        file_desc_proto2 = descriptor_pb2.FileDescriptorProto.FromString(unittest_pb2.DESCRIPTOR.serialized_pb)
        db.Add(file_desc_proto2)
        self.assertEqual(file_desc_proto2, db.FindFileContainingSymbol('protobuf_unittest.TestService'))
        self.assertEqual(file_desc_proto2, db.FindFileContainingSymbol('protobuf_unittest.TestAllTypes.none_field'))
        with self.assertRaisesRegexp(KeyError, "\\'protobuf_unittest\\.NoneMessage\\'"):
            db.FindFileContainingSymbol('protobuf_unittest.NoneMessage')

    def testConflictRegister(self):
        db = descriptor_database.DescriptorDatabase()
        unittest_fd = descriptor_pb2.FileDescriptorProto.FromString(unittest_pb2.DESCRIPTOR.serialized_pb)
        db.Add(unittest_fd)
        conflict_fd = descriptor_pb2.FileDescriptorProto.FromString(unittest_pb2.DESCRIPTOR.serialized_pb)
        conflict_fd.name = 'other_file2'
        with warnings.catch_warnings(record=True) as (w):
            warnings.simplefilter('always')
            db.Add(conflict_fd)
            self.assertTrue(len(w))
            self.assertIs(w[0].category, RuntimeWarning)
            self.assertIn('Conflict register for file "other_file2": ', str(w[0].message))
            self.assertIn('already defined in file "google/protobuf/unittest.proto"', str(w[0].message))


if __name__ == '__main__':
    unittest.main()