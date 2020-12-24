# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dexter/git/tensorboardX/tensorboardX/proto/graph_pb2.py
# Compiled at: 2019-12-25 07:50:25
# Size of source mod 2**32: 3648 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
import google.protobuf as _descriptor
import google.protobuf as _message
import google.protobuf as _reflection
import google.protobuf as _symbol_database
_sym_db = _symbol_database.Default()
import tensorboardX.proto as tensorboardX_dot_proto_dot_node__def__pb2
import tensorboardX.proto as tensorboardX_dot_proto_dot_versions__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='tensorboardX/proto/graph.proto',
  package='tensorboardX',
  syntax='proto3',
  serialized_options=(_b('\n\x18org.tensorflow.frameworkB\x0bGraphProtosP\x01ø\x01\x01')),
  serialized_pb=(_b('\n\x1etensorboardX/proto/graph.proto\x12\x0ctensorboardX\x1a!tensorboardX/proto/node_def.proto\x1a!tensorboardX/proto/versions.proto"p\n\x08GraphDef\x12#\n\x04node\x18\x01 \x03(\x0b2\x15.tensorboardX.NodeDef\x12*\n\x08versions\x18\x04 \x01(\x0b2\x18.tensorboardX.VersionDef\x12\x13\n\x07version\x18\x03 \x01(\x05B\x02\x18\x01B,\n\x18org.tensorflow.frameworkB\x0bGraphProtosP\x01ø\x01\x01b\x06proto3')),
  dependencies=[
 tensorboardX_dot_proto_dot_node__def__pb2.DESCRIPTOR, tensorboardX_dot_proto_dot_versions__pb2.DESCRIPTOR])
_GRAPHDEF = _descriptor.Descriptor(name='GraphDef',
  full_name='tensorboardX.GraphDef',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='node',
   full_name='tensorboardX.GraphDef.node',
   index=0,
   number=1,
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
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='versions',
   full_name='tensorboardX.GraphDef.versions',
   index=1,
   number=4,
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
 _descriptor.FieldDescriptor(name='version',
   full_name='tensorboardX.GraphDef.version',
   index=2,
   number=3,
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
   serialized_options=(_b('\x18\x01')),
   file=DESCRIPTOR)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[],
  serialized_start=118,
  serialized_end=230)
_GRAPHDEF.fields_by_name['node'].message_type = tensorboardX_dot_proto_dot_node__def__pb2._NODEDEF
_GRAPHDEF.fields_by_name['versions'].message_type = tensorboardX_dot_proto_dot_versions__pb2._VERSIONDEF
DESCRIPTOR.message_types_by_name['GraphDef'] = _GRAPHDEF
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
GraphDef = _reflection.GeneratedProtocolMessageType('GraphDef', (_message.Message,), {'DESCRIPTOR':_GRAPHDEF, 
 '__module__':'tensorboardX.proto.graph_pb2'})
_sym_db.RegisterMessage(GraphDef)
DESCRIPTOR._options = None
_GRAPHDEF.fields_by_name['version']._options = None