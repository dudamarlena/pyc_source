# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alexander/machinekit/projects/pymachinetalk/examples/c++_ipc/ipcmsg_pb2.py
# Compiled at: 2017-04-22 13:14:04
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='ipcmsg.proto', package='pb', serialized_pb=_b(b'\n\x0cipcmsg.proto\x12\x02pb"\xa2\x01\n\x07Message\x12\x1d\n\x04type\x18\x01 \x02(\x0e2\x0f.pb.MessageType\x12\x0c\n\x04axis\x18\x02 \x01(\x05\x12\x10\n\x08velocity\x18\x03 \x01(\x01\x12\x10\n\x08distance\x18\x04 \x01(\x01\x12\x1d\n\x08jog_type\x18\x05 \x01(\x0e2\x0b.pb.JogType\x12\t\n\x01x\x18\x06 \x01(\x01\x12\t\n\x01y\x18\x07 \x01(\x01\x12\x11\n\tconnected\x18\x08 \x01(\x08*?\n\x0bMessageType\x12\x0b\n\x07IPC_JOG\x10\x01\x12\x10\n\x0cIPC_POSITION\x10\x02\x12\x11\n\rIPC_CONNECTED\x10\x03*@\n\x07JogType\x12\x0c\n\x08JOG_STOP\x10\x00\x12\x12\n\x0eJOG_CONTINUOUS\x10\x01\x12\x13\n\x0fJOG_INCREMENTAL\x10\x02'))
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
_MESSAGETYPE = _descriptor.EnumDescriptor(name='MessageType', full_name='pb.MessageType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='IPC_JOG', index=0, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='IPC_POSITION', index=1, number=2, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='IPC_CONNECTED', index=2, number=3, options=None, type=None)], containing_type=None, options=None, serialized_start=185, serialized_end=248)
_sym_db.RegisterEnumDescriptor(_MESSAGETYPE)
MessageType = enum_type_wrapper.EnumTypeWrapper(_MESSAGETYPE)
_JOGTYPE = _descriptor.EnumDescriptor(name='JogType', full_name='pb.JogType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='JOG_STOP', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='JOG_CONTINUOUS', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='JOG_INCREMENTAL', index=2, number=2, options=None, type=None)], containing_type=None, options=None, serialized_start=250, serialized_end=314)
_sym_db.RegisterEnumDescriptor(_JOGTYPE)
JogType = enum_type_wrapper.EnumTypeWrapper(_JOGTYPE)
IPC_JOG = 1
IPC_POSITION = 2
IPC_CONNECTED = 3
JOG_STOP = 0
JOG_CONTINUOUS = 1
JOG_INCREMENTAL = 2
_MESSAGE = _descriptor.Descriptor(name='Message', full_name='pb.Message', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='type', full_name='pb.Message.type', index=0, number=1, type=14, cpp_type=8, label=2, has_default_value=False, default_value=1, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='axis', full_name='pb.Message.axis', index=1, number=2, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='velocity', full_name='pb.Message.velocity', index=2, number=3, type=1, cpp_type=5, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='distance', full_name='pb.Message.distance', index=3, number=4, type=1, cpp_type=5, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='jog_type', full_name='pb.Message.jog_type', index=4, number=5, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='x', full_name='pb.Message.x', index=5, number=6, type=1, cpp_type=5, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='y', full_name='pb.Message.y', index=6, number=7, type=1, cpp_type=5, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='connected', full_name='pb.Message.connected', index=7, number=8, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], oneofs=[], serialized_start=21, serialized_end=183)
_MESSAGE.fields_by_name['type'].enum_type = _MESSAGETYPE
_MESSAGE.fields_by_name['jog_type'].enum_type = _JOGTYPE
DESCRIPTOR.message_types_by_name['Message'] = _MESSAGE
DESCRIPTOR.enum_types_by_name['MessageType'] = _MESSAGETYPE
DESCRIPTOR.enum_types_by_name['JogType'] = _JOGTYPE
Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), dict(DESCRIPTOR=_MESSAGE, __module__='ipcmsg_pb2'))
_sym_db.RegisterMessage(Message)