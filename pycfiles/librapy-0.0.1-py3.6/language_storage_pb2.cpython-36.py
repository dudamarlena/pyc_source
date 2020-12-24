# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/librapy/proto/language_storage_pb2.py
# Compiled at: 2019-09-11 21:20:08
# Size of source mod 2**32: 2317 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='language_storage.proto',
  package='types',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=(_b('\n\x16language_storage.proto\x12\x05types")\n\x08ModuleId\x12\x0f\n\x07address\x18\x01 \x01(\x0c\x12\x0c\n\x04name\x18\x02 \x01(\tb\x06proto3')))
_MODULEID = _descriptor.Descriptor(name='ModuleId',
  full_name='types.ModuleId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='address',
   full_name='types.ModuleId.address',
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
 _descriptor.FieldDescriptor(name='name',
   full_name='types.ModuleId.name',
   index=1,
   number=2,
   type=9,
   cpp_type=9,
   label=1,
   has_default_value=False,
   default_value=(_b('').decode('utf-8')),
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
  serialized_start=33,
  serialized_end=74)
DESCRIPTOR.message_types_by_name['ModuleId'] = _MODULEID
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
ModuleId = _reflection.GeneratedProtocolMessageType('ModuleId', (_message.Message,), {'DESCRIPTOR':_MODULEID, 
 '__module__':'language_storage_pb2'})
_sym_db.RegisterMessage(ModuleId)