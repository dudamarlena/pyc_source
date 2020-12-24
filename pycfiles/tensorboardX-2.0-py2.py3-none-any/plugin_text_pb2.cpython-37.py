# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dexter/git/tensorboardX/tensorboardX/proto/plugin_text_pb2.py
# Compiled at: 2019-12-25 07:50:25
# Size of source mod 2**32: 2063 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
import google.protobuf as _descriptor
import google.protobuf as _message
import google.protobuf as _reflection
import google.protobuf as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='tensorboardX/proto/plugin_text.proto',
  package='tensorboardX',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=(_b('\n$tensorboardX/proto/plugin_text.proto\x12\x0ctensorboardX"!\n\x0eTextPluginData\x12\x0f\n\x07version\x18\x01 \x01(\x05b\x06proto3')))
_TEXTPLUGINDATA = _descriptor.Descriptor(name='TextPluginData',
  full_name='tensorboardX.TextPluginData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='version',
   full_name='tensorboardX.TextPluginData.version',
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
  serialized_start=54,
  serialized_end=87)
DESCRIPTOR.message_types_by_name['TextPluginData'] = _TEXTPLUGINDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
TextPluginData = _reflection.GeneratedProtocolMessageType('TextPluginData', (_message.Message,), {'DESCRIPTOR':_TEXTPLUGINDATA, 
 '__module__':'tensorboardX.proto.plugin_text_pb2'})
_sym_db.RegisterMessage(TextPluginData)