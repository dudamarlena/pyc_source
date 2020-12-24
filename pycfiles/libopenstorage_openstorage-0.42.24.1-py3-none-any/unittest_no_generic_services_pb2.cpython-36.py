# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/unittest_no_generic_services_pb2.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 4265 bytes
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='google/protobuf/unittest_no_generic_services.proto',
  package='protobuf_unittest.no_generic_services_test',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=b'\n2google/protobuf/unittest_no_generic_services.proto\x12*protobuf_unittest.no_generic_services_test"#\n\x0bTestMessage\x12\t\n\x01a\x18\x01 \x01(\x05*\t\x08\xe8\x07\x10\x80\x80\x80\x80\x02*\x13\n\x08TestEnum\x12\x07\n\x03FOO\x10\x012\x86\x01\n\x0bTestService\x12w\n\x03Foo\x127.protobuf_unittest.no_generic_services_test.TestMessage\x1a7.protobuf_unittest.no_generic_services_test.TestMessage:P\n\x0etest_extension\x127.protobuf_unittest.no_generic_services_test.TestMessage\x18\xe8\x07 \x01(\x05')
_TESTENUM = _descriptor.EnumDescriptor(name='TestEnum',
  full_name='protobuf_unittest.no_generic_services_test.TestEnum',
  filename=None,
  file=DESCRIPTOR,
  values=[
 _descriptor.EnumValueDescriptor(name='FOO',
   index=0,
   number=1,
   serialized_options=None,
   type=None)],
  containing_type=None,
  serialized_options=None,
  serialized_start=135,
  serialized_end=154)
_sym_db.RegisterEnumDescriptor(_TESTENUM)
TestEnum = enum_type_wrapper.EnumTypeWrapper(_TESTENUM)
FOO = 1
TEST_EXTENSION_FIELD_NUMBER = 1000
test_extension = _descriptor.FieldDescriptor(name='test_extension',
  full_name='protobuf_unittest.no_generic_services_test.test_extension',
  index=0,
  number=1000,
  type=5,
  cpp_type=1,
  label=1,
  has_default_value=False,
  default_value=0,
  message_type=None,
  enum_type=None,
  containing_type=None,
  is_extension=True,
  extension_scope=None,
  serialized_options=None,
  file=DESCRIPTOR)
_TESTMESSAGE = _descriptor.Descriptor(name='TestMessage',
  full_name='protobuf_unittest.no_generic_services_test.TestMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='a',
   full_name='protobuf_unittest.no_generic_services_test.TestMessage.a',
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
   file=DESCRIPTOR)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  serialized_options=None,
  is_extendable=True,
  syntax='proto2',
  extension_ranges=[
 (1000, 536870912)],
  oneofs=[],
  serialized_start=98,
  serialized_end=133)
DESCRIPTOR.message_types_by_name['TestMessage'] = _TESTMESSAGE
DESCRIPTOR.enum_types_by_name['TestEnum'] = _TESTENUM
DESCRIPTOR.extensions_by_name['test_extension'] = test_extension
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
TestMessage = _reflection.GeneratedProtocolMessageType('TestMessage', (_message.Message,), {'DESCRIPTOR':_TESTMESSAGE, 
 '__module__':'google.protobuf.unittest_no_generic_services_pb2'})
_sym_db.RegisterMessage(TestMessage)
TestMessage.RegisterExtension(test_extension)
_TESTSERVICE = _descriptor.ServiceDescriptor(name='TestService',
  full_name='protobuf_unittest.no_generic_services_test.TestService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=157,
  serialized_end=291,
  methods=[
 _descriptor.MethodDescriptor(name='Foo',
   full_name='protobuf_unittest.no_generic_services_test.TestService.Foo',
   index=0,
   containing_service=None,
   input_type=_TESTMESSAGE,
   output_type=_TESTMESSAGE,
   serialized_options=None)])
_sym_db.RegisterServiceDescriptor(_TESTSERVICE)
DESCRIPTOR.services_by_name['TestService'] = _TESTSERVICE