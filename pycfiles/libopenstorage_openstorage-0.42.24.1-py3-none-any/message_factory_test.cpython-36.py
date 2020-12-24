# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/internal/message_factory_test.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 9673 bytes
"""Tests for google.protobuf.message_factory."""
__author__ = 'matthewtoia@google.com (Matt Toia)'
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from google.protobuf import descriptor_pb2
from google.protobuf.internal import api_implementation
from google.protobuf.internal import factory_test1_pb2
from google.protobuf.internal import factory_test2_pb2
from google.protobuf.internal import testing_refleaks
from google.protobuf import descriptor_database
from google.protobuf import descriptor_pool
from google.protobuf import message_factory

@testing_refleaks.TestCase
class MessageFactoryTest(unittest.TestCase):

    def setUp(self):
        self.factory_test1_fd = descriptor_pb2.FileDescriptorProto.FromString(factory_test1_pb2.DESCRIPTOR.serialized_pb)
        self.factory_test2_fd = descriptor_pb2.FileDescriptorProto.FromString(factory_test2_pb2.DESCRIPTOR.serialized_pb)

    def _ExerciseDynamicClass(self, cls):
        msg = cls()
        msg.mandatory = 42
        msg.nested_factory_2_enum = 0
        msg.nested_factory_2_message.value = 'nested message value'
        msg.factory_1_message.factory_1_enum = 1
        msg.factory_1_message.nested_factory_1_enum = 0
        msg.factory_1_message.nested_factory_1_message.value = 'nested message value'
        msg.factory_1_message.scalar_value = 22
        msg.factory_1_message.list_value.extend(['one', 'two', 'three'])
        msg.factory_1_message.list_value.append('four')
        msg.factory_1_enum = 1
        msg.nested_factory_1_enum = 0
        msg.nested_factory_1_message.value = 'nested message value'
        msg.circular_message.mandatory = 1
        msg.circular_message.circular_message.mandatory = 2
        msg.circular_message.scalar_value = 'one deep'
        msg.scalar_value = 'zero deep'
        msg.list_value.extend(['four', 'three', 'two'])
        msg.list_value.append('one')
        msg.grouped.add()
        msg.grouped[0].part_1 = 'hello'
        msg.grouped[0].part_2 = 'world'
        msg.grouped.add(part_1='testing', part_2='123')
        msg.loop.loop.mandatory = 2
        msg.loop.loop.loop.loop.mandatory = 4
        serialized = msg.SerializeToString()
        converted = factory_test2_pb2.Factory2Message.FromString(serialized)
        reserialized = converted.SerializeToString()
        self.assertEqual(serialized, reserialized)
        result = cls.FromString(reserialized)
        self.assertEqual(msg, result)

    def testGetPrototype(self):
        db = descriptor_database.DescriptorDatabase()
        pool = descriptor_pool.DescriptorPool(db)
        db.Add(self.factory_test1_fd)
        db.Add(self.factory_test2_fd)
        factory = message_factory.MessageFactory()
        cls = factory.GetPrototype(pool.FindMessageTypeByName('google.protobuf.python.internal.Factory2Message'))
        self.assertFalse(cls is factory_test2_pb2.Factory2Message)
        self._ExerciseDynamicClass(cls)
        cls2 = factory.GetPrototype(pool.FindMessageTypeByName('google.protobuf.python.internal.Factory2Message'))
        self.assertTrue(cls is cls2)

    def testGetMessages(self):
        for _ in range(2):
            self.assertIn(self.factory_test1_fd.name, self.factory_test2_fd.dependency)
            messages = message_factory.GetMessages([self.factory_test2_fd,
             self.factory_test1_fd])
            self.assertTrue(set(['google.protobuf.python.internal.Factory2Message',
             'google.protobuf.python.internal.Factory1Message']).issubset(set(messages.keys())))
            self._ExerciseDynamicClass(messages['google.protobuf.python.internal.Factory2Message'])
            factory_msg1 = messages['google.protobuf.python.internal.Factory1Message']
            self.assertTrue(set([
             'google.protobuf.python.internal.Factory2Message.one_more_field',
             'google.protobuf.python.internal.another_field']).issubset(set(ext.full_name for ext in factory_msg1.DESCRIPTOR.file.pool.FindAllExtensions(factory_msg1.DESCRIPTOR))))
            msg1 = messages['google.protobuf.python.internal.Factory1Message']()
            ext1 = msg1.Extensions._FindExtensionByName('google.protobuf.python.internal.Factory2Message.one_more_field')
            ext2 = msg1.Extensions._FindExtensionByName('google.protobuf.python.internal.another_field')
            self.assertEqual(0, len(msg1.Extensions))
            msg1.Extensions[ext1] = 'test1'
            msg1.Extensions[ext2] = 'test2'
            self.assertEqual('test1', msg1.Extensions[ext1])
            self.assertEqual('test2', msg1.Extensions[ext2])
            self.assertEqual(None, msg1.Extensions._FindExtensionByNumber(12321))
            self.assertEqual(2, len(msg1.Extensions))
            if api_implementation.Type() == 'cpp':
                self.assertRaises(TypeError, msg1.Extensions._FindExtensionByName, 0)
                self.assertRaises(TypeError, msg1.Extensions._FindExtensionByNumber, '')
            else:
                self.assertEqual(None, msg1.Extensions._FindExtensionByName(0))
                self.assertEqual(None, msg1.Extensions._FindExtensionByNumber(''))

    def testDuplicateExtensionNumber(self):
        pool = descriptor_pool.DescriptorPool()
        factory = message_factory.MessageFactory(pool=pool)
        f = descriptor_pb2.FileDescriptorProto()
        f.name = 'google/protobuf/internal/container.proto'
        f.package = 'google.protobuf.python.internal'
        msg = f.message_type.add()
        msg.name = 'Container'
        rng = msg.extension_range.add()
        rng.start = 1
        rng.end = 10
        pool.Add(f)
        msgs = factory.GetMessages([f.name])
        self.assertIn('google.protobuf.python.internal.Container', msgs)
        f = descriptor_pb2.FileDescriptorProto()
        f.name = 'google/protobuf/internal/extension.proto'
        f.package = 'google.protobuf.python.internal'
        f.dependency.append('google/protobuf/internal/container.proto')
        msg = f.message_type.add()
        msg.name = 'Extension'
        ext = msg.extension.add()
        ext.name = 'extension_field'
        ext.number = 2
        ext.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
        ext.type_name = 'Extension'
        ext.extendee = 'Container'
        pool.Add(f)
        msgs = factory.GetMessages([f.name])
        self.assertIn('google.protobuf.python.internal.Extension', msgs)
        f = descriptor_pb2.FileDescriptorProto()
        f.name = 'google/protobuf/internal/duplicate.proto'
        f.package = 'google.protobuf.python.internal'
        f.dependency.append('google/protobuf/internal/container.proto')
        msg = f.message_type.add()
        msg.name = 'Duplicate'
        ext = msg.extension.add()
        ext.name = 'extension_field'
        ext.number = 2
        ext.label = descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL
        ext.type_name = 'Duplicate'
        ext.extendee = 'Container'
        pool.Add(f)
        with self.assertRaises(Exception) as (cm):
            factory.GetMessages([f.name])
        self.assertIn(str(cm.exception), [
         'Extensions "google.protobuf.python.internal.Duplicate.extension_field" and "google.protobuf.python.internal.Extension.extension_field" both try to extend message type "google.protobuf.python.internal.Container" with field number 2.',
         'Double registration of Extensions'])


if __name__ == '__main__':
    unittest.main()