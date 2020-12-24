# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/internal/import_test_package/outer_pb2.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 2629 bytes
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.protobuf.internal.import_test_package import inner_pb2 as google_dot_protobuf_dot_internal_dot_import__test__package_dot_inner__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='google/protobuf/internal/import_test_package/outer.proto',
  package='google.protobuf.python.internal.import_test_package',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=b'\n8google/protobuf/internal/import_test_package/outer.proto\x123google.protobuf.python.internal.import_test_package\x1a8google/protobuf/internal/import_test_package/inner.proto"R\n\x05Outer\x12I\n\x05inner\x18\x01 \x01(\x0b2:.google.protobuf.python.internal.import_test_package.Inner',
  dependencies=[
 google_dot_protobuf_dot_internal_dot_import__test__package_dot_inner__pb2.DESCRIPTOR])
_OUTER = _descriptor.Descriptor(name='Outer',
  full_name='google.protobuf.python.internal.import_test_package.Outer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='inner',
   full_name='google.protobuf.python.internal.import_test_package.Outer.inner',
   index=0,
   number=1,
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
   file=DESCRIPTOR)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=171,
  serialized_end=253)
_OUTER.fields_by_name['inner'].message_type = google_dot_protobuf_dot_internal_dot_import__test__package_dot_inner__pb2._INNER
DESCRIPTOR.message_types_by_name['Outer'] = _OUTER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
Outer = _reflection.GeneratedProtocolMessageType('Outer', (_message.Message,), {'DESCRIPTOR':_OUTER, 
 '__module__':'google.protobuf.internal.import_test_package.outer_pb2'})
_sym_db.RegisterMessage(Outer)