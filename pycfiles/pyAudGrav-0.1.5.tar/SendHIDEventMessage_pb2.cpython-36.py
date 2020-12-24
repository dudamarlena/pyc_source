# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/mrp/protobuf/SendHIDEventMessage_pb2.py
# Compiled at: 2019-09-30 07:18:14
# Size of source mod 2**32: 3058 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from pyatv.mrp.protobuf import ProtocolMessage_pb2 as pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='pyatv/mrp/protobuf/SendHIDEventMessage.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=(_b('\n,pyatv/mrp/protobuf/SendHIDEventMessage.proto\x1a(pyatv/mrp/protobuf/ProtocolMessage.proto"+\n\x13SendHIDEventMessage\x12\x14\n\x0chidEventData\x18\x01 \x01(\x0c:C\n\x13sendHIDEventMessage\x12\x10.ProtocolMessage\x18\r \x01(\x0b2\x14.SendHIDEventMessage')),
  dependencies=[
 pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.DESCRIPTOR])
SENDHIDEVENTMESSAGE_FIELD_NUMBER = 13
sendHIDEventMessage = _descriptor.FieldDescriptor(name='sendHIDEventMessage',
  full_name='sendHIDEventMessage',
  index=0,
  number=13,
  type=11,
  cpp_type=10,
  label=1,
  has_default_value=False,
  default_value=None,
  message_type=None,
  enum_type=None,
  containing_type=None,
  is_extension=True,
  extension_scope=None,
  serialized_options=None,
  file=DESCRIPTOR)
_SENDHIDEVENTMESSAGE = _descriptor.Descriptor(name='SendHIDEventMessage',
  full_name='SendHIDEventMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='hidEventData',
   full_name='SendHIDEventMessage.hidEventData',
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
   file=DESCRIPTOR)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=90,
  serialized_end=133)
DESCRIPTOR.message_types_by_name['SendHIDEventMessage'] = _SENDHIDEVENTMESSAGE
DESCRIPTOR.extensions_by_name['sendHIDEventMessage'] = sendHIDEventMessage
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
SendHIDEventMessage = _reflection.GeneratedProtocolMessageType('SendHIDEventMessage', (_message.Message,), {'DESCRIPTOR':_SENDHIDEVENTMESSAGE, 
 '__module__':'pyatv.mrp.protobuf.SendHIDEventMessage_pb2'})
_sym_db.RegisterMessage(SendHIDEventMessage)
sendHIDEventMessage.message_type = _SENDHIDEVENTMESSAGE
pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.ProtocolMessage.RegisterExtension(sendHIDEventMessage)