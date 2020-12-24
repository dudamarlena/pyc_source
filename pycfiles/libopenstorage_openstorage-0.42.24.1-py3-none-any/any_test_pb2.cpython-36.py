# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/any_test_pb2.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 3168 bytes
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='google/protobuf/any_test.proto',
  package='protobuf_unittest',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x1egoogle/protobuf/any_test.proto\x12\x11protobuf_unittest\x1a\x19google/protobuf/any.proto"y\n\x07TestAny\x12\x13\n\x0bint32_value\x18\x01 \x01(\x05\x12\'\n\tany_value\x18\x02 \x01(\x0b2\x14.google.protobuf.Any\x120\n\x12repeated_any_value\x18\x03 \x03(\x0b2\x14.google.protobuf.Anyb\x06proto3',
  dependencies=[
 google_dot_protobuf_dot_any__pb2.DESCRIPTOR])
_TESTANY = _descriptor.Descriptor(name='TestAny',
  full_name='protobuf_unittest.TestAny',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='int32_value',
   full_name='protobuf_unittest.TestAny.int32_value',
   index=0,
   number=1,
   type=5,
   cpp_type=1,
   label=1,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='any_value',
   full_name='protobuf_unittest.TestAny.any_value',
   index=1,
   number=2,
   type=11,
   cpp_type=10,
   label=1,
   has_default_value=False,
   default_value=None,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='repeated_any_value',
   full_name='protobuf_unittest.TestAny.repeated_any_value',
   index=2,
   number=3,
   type=11,
   cpp_type=10,
   label=3,
   has_default_value=False,
   default_value=[],
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[],
  serialized_start=80,
  serialized_end=201)
_TESTANY.fields_by_name['any_value'].message_type = google_dot_protobuf_dot_any__pb2._ANY
_TESTANY.fields_by_name['repeated_any_value'].message_type = google_dot_protobuf_dot_any__pb2._ANY
DESCRIPTOR.message_types_by_name['TestAny'] = _TESTANY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
TestAny = _reflection.GeneratedProtocolMessageType('TestAny', (_message.Message,), {'DESCRIPTOR':_TESTANY, 
 '__module__':'google.protobuf.any_test_pb2'})
_sym_db.RegisterMessage(TestAny)