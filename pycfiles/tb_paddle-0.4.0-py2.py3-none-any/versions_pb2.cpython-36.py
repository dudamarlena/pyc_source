# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/linshuliang/work_baidu/tb-paddle/tb_paddle/proto/versions_pb2.py
# Compiled at: 2020-01-08 07:01:22
# Size of source mod 2**32: 2881 bytes
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='tb_paddle/proto/versions.proto',
  package='tb_paddle',
  syntax='proto3',
  serialized_options=b'\n\x18org.tensorflow.frameworkB\x0eVersionsProtosP\x01\xf8\x01\x01',
  serialized_pb=b'\n\x1etb_paddle/proto/versions.proto\x12\ttb_paddle"K\n\nVersionDef\x12\x10\n\x08producer\x18\x01 \x01(\x05\x12\x14\n\x0cmin_consumer\x18\x02 \x01(\x05\x12\x15\n\rbad_consumers\x18\x03 \x03(\x05B/\n\x18org.tensorflow.frameworkB\x0eVersionsProtosP\x01\xf8\x01\x01b\x06proto3')
_VERSIONDEF = _descriptor.Descriptor(name='VersionDef',
  full_name='tb_paddle.VersionDef',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='producer',
   full_name='tb_paddle.VersionDef.producer',
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
 _descriptor.FieldDescriptor(name='min_consumer',
   full_name='tb_paddle.VersionDef.min_consumer',
   index=1,
   number=2,
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
 _descriptor.FieldDescriptor(name='bad_consumers',
   full_name='tb_paddle.VersionDef.bad_consumers',
   index=2,
   number=3,
   type=5,
   cpp_type=1,
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
  serialized_start=45,
  serialized_end=120)
DESCRIPTOR.message_types_by_name['VersionDef'] = _VERSIONDEF
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
VersionDef = _reflection.GeneratedProtocolMessageType('VersionDef', (_message.Message,), {'DESCRIPTOR':_VERSIONDEF, 
 '__module__':'tb_paddle.proto.versions_pb2'})
_sym_db.RegisterMessage(VersionDef)
DESCRIPTOR._options = None