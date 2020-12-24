# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/internal/proto_builder_test.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 3770 bytes
"""Tests for google.protobuf.proto_builder."""
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from google.protobuf import descriptor_pb2
from google.protobuf import descriptor_pool
from google.protobuf import proto_builder
from google.protobuf import text_format

class ProtoBuilderTest(unittest.TestCase):

    def setUp(self):
        self.ordered_fields = OrderedDict([
         (
          'foo', descriptor_pb2.FieldDescriptorProto.TYPE_INT64),
         (
          'bar', descriptor_pb2.FieldDescriptorProto.TYPE_STRING)])
        self._fields = dict(self.ordered_fields)

    def testMakeSimpleProtoClass(self):
        """Test that we can create a proto class."""
        proto_cls = proto_builder.MakeSimpleProtoClass((self._fields),
          full_name='net.proto2.python.public.proto_builder_test.Test')
        proto = proto_cls()
        proto.foo = 12345
        proto.bar = 'asdf'
        self.assertMultiLineEqual('bar: "asdf"\nfoo: 12345\n', text_format.MessageToString(proto))

    def testOrderedFields(self):
        """Test that the field order is maintained when given an OrderedDict."""
        proto_cls = proto_builder.MakeSimpleProtoClass((self.ordered_fields),
          full_name='net.proto2.python.public.proto_builder_test.OrderedTest')
        proto = proto_cls()
        proto.foo = 12345
        proto.bar = 'asdf'
        self.assertMultiLineEqual('foo: 12345\nbar: "asdf"\n', text_format.MessageToString(proto))

    def testMakeSameProtoClassTwice(self):
        """Test that the DescriptorPool is used."""
        pool = descriptor_pool.DescriptorPool()
        proto_cls1 = proto_builder.MakeSimpleProtoClass((self._fields),
          full_name='net.proto2.python.public.proto_builder_test.Test',
          pool=pool)
        proto_cls2 = proto_builder.MakeSimpleProtoClass((self._fields),
          full_name='net.proto2.python.public.proto_builder_test.Test',
          pool=pool)
        self.assertIs(proto_cls1.DESCRIPTOR, proto_cls2.DESCRIPTOR)


if __name__ == '__main__':
    unittest.main()