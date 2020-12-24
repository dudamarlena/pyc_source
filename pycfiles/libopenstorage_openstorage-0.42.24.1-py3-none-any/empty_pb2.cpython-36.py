# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/empty_pb2.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 1791 bytes
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='google/protobuf/empty.proto',
  package='google.protobuf',
  syntax='proto3',
  serialized_options=b"\n\x13com.google.protobufB\nEmptyProtoP\x01Z'github.com/golang/protobuf/ptypes/empty\xf8\x01\x01\xa2\x02\x03GPB\xaa\x02\x1eGoogle.Protobuf.WellKnownTypes",
  serialized_pb=b'\n\x1bgoogle/protobuf/empty.proto\x12\x0fgoogle.protobuf"\x07\n\x05EmptyBv\n\x13com.google.protobufB\nEmptyProtoP\x01Z\'github.com/golang/protobuf/ptypes/empty\xf8\x01\x01\xa2\x02\x03GPB\xaa\x02\x1eGoogle.Protobuf.WellKnownTypesb\x06proto3')
_EMPTY = _descriptor.Descriptor(name='Empty',
  full_name='google.protobuf.Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[],
  extensions=[],
  nested_types=[],
  enum_types=[],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[],
  serialized_start=48,
  serialized_end=55)
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {'DESCRIPTOR':_EMPTY, 
 '__module__':'google.protobuf.empty_pb2'})
_sym_db.RegisterMessage(Empty)
DESCRIPTOR._options = None