# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/linshuliang/work_baidu/tb-paddle/tb_paddle/proto/plugin_text_pb2.py
# Compiled at: 2020-01-08 07:01:22
# Size of source mod 2**32: 1945 bytes
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='tb_paddle/proto/plugin_text.proto',
  package='tb_paddle',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n!tb_paddle/proto/plugin_text.proto\x12\ttb_paddle"!\n\x0eTextPluginData\x12\x0f\n\x07version\x18\x01 \x01(\x05b\x06proto3')
_TEXTPLUGINDATA = _descriptor.Descriptor(name='TextPluginData',
  full_name='tb_paddle.TextPluginData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='version',
   full_name='tb_paddle.TextPluginData.version',
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
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[],
  serialized_start=48,
  serialized_end=81)
DESCRIPTOR.message_types_by_name['TextPluginData'] = _TEXTPLUGINDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
TextPluginData = _reflection.GeneratedProtocolMessageType('TextPluginData', (_message.Message,), {'DESCRIPTOR':_TEXTPLUGINDATA, 
 '__module__':'tb_paddle.proto.plugin_text_pb2'})
_sym_db.RegisterMessage(TextPluginData)