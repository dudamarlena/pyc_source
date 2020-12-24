# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dexter/git/tensorboardX/tensorboardX/proto/node_def_pb2.py
# Compiled at: 2019-08-01 11:57:19
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from tensorboardX.proto import attr_value_pb2 as tensorboardX_dot_proto_dot_attr__value__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='tensorboardX/proto/node_def.proto', package='tensorboardX', syntax='proto3', serialized_options=_b(b'\n\x18org.tensorflow.frameworkB\tNodeProtoP\x01\xf8\x01\x01'), serialized_pb=_b(b'\n!tensorboardX/proto/node_def.proto\x12\x0ctensorboardX\x1a#tensorboardX/proto/attr_value.proto"\xb7\x01\n\x07NodeDef\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\n\n\x02op\x18\x02 \x01(\t\x12\r\n\x05input\x18\x03 \x03(\t\x12\x0e\n\x06device\x18\x04 \x01(\t\x12-\n\x04attr\x18\x05 \x03(\x0b2\x1f.tensorboardX.NodeDef.AttrEntry\x1aD\n\tAttrEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12&\n\x05value\x18\x02 \x01(\x0b2\x17.tensorboardX.AttrValue:\x028\x01B*\n\x18org.tensorflow.frameworkB\tNodeProtoP\x01\xf8\x01\x01b\x06proto3'), dependencies=[
 tensorboardX_dot_proto_dot_attr__value__pb2.DESCRIPTOR])
_NODEDEF_ATTRENTRY = _descriptor.Descriptor(name='AttrEntry', full_name='tensorboardX.NodeDef.AttrEntry', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='key', full_name='tensorboardX.NodeDef.AttrEntry.key', index=0, number=1, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='value', full_name='tensorboardX.NodeDef.AttrEntry.value', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=_b('8\x01'), is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=204, serialized_end=272)
_NODEDEF = _descriptor.Descriptor(name='NodeDef', full_name='tensorboardX.NodeDef', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='name', full_name='tensorboardX.NodeDef.name', index=0, number=1, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='op', full_name='tensorboardX.NodeDef.op', index=1, number=2, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='input', full_name='tensorboardX.NodeDef.input', index=2, number=3, type=9, cpp_type=9, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='device', full_name='tensorboardX.NodeDef.device', index=3, number=4, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='attr', full_name='tensorboardX.NodeDef.attr', index=4, number=5, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[
 _NODEDEF_ATTRENTRY], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=89, serialized_end=272)
_NODEDEF_ATTRENTRY.fields_by_name['value'].message_type = tensorboardX_dot_proto_dot_attr__value__pb2._ATTRVALUE
_NODEDEF_ATTRENTRY.containing_type = _NODEDEF
_NODEDEF.fields_by_name['attr'].message_type = _NODEDEF_ATTRENTRY
DESCRIPTOR.message_types_by_name['NodeDef'] = _NODEDEF
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
NodeDef = _reflection.GeneratedProtocolMessageType('NodeDef', (_message.Message,), dict(AttrEntry=_reflection.GeneratedProtocolMessageType('AttrEntry', (_message.Message,), dict(DESCRIPTOR=_NODEDEF_ATTRENTRY, __module__='tensorboardX.proto.node_def_pb2')), DESCRIPTOR=_NODEDEF, __module__='tensorboardX.proto.node_def_pb2'))
_sym_db.RegisterMessage(NodeDef)
_sym_db.RegisterMessage(NodeDef.AttrEntry)
DESCRIPTOR._options = None
_NODEDEF_ATTRENTRY._options = None