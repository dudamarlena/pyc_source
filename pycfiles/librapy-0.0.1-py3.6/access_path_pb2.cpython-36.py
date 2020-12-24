# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/librapy/proto/access_path_pb2.py
# Compiled at: 2019-09-11 21:20:08
# Size of source mod 2**32: 2323 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='access_path.proto',
  package='types',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=(_b('\n\x11access_path.proto\x12\x05types"+\n\nAccessPath\x12\x0f\n\x07address\x18\x01 \x01(\x0c\x12\x0c\n\x04path\x18\x02 \x01(\x0cb\x06proto3')))
_ACCESSPATH = _descriptor.Descriptor(name='AccessPath',
  full_name='types.AccessPath',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='address',
   full_name='types.AccessPath.address',
   index=0,
   number=1,
   type=12,
   cpp_type=9,
   label=1,
   has_default_value=False,
   default_value=(_b('')),
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='path',
   full_name='types.AccessPath.path',
   index=1,
   number=2,
   type=12,
   cpp_type=9,
   label=1,
   has_default_value=False,
   default_value=(_b('')),
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
  serialized_start=28,
  serialized_end=71)
DESCRIPTOR.message_types_by_name['AccessPath'] = _ACCESSPATH
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
AccessPath = _reflection.GeneratedProtocolMessageType('AccessPath', (_message.Message,), {'DESCRIPTOR':_ACCESSPATH, 
 '__module__':'access_path_pb2'})
_sym_db.RegisterMessage(AccessPath)