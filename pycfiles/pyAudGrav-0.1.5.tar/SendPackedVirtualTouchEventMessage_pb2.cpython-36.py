# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/mrp/protobuf/SendPackedVirtualTouchEventMessage_pb2.py
# Compiled at: 2019-09-30 07:18:14
# Size of source mod 2**32: 4740 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from pyatv.mrp.protobuf import ProtocolMessage_pb2 as pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='pyatv/mrp/protobuf/SendPackedVirtualTouchEventMessage.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=(_b('\n;pyatv/mrp/protobuf/SendPackedVirtualTouchEventMessage.proto\x1a(pyatv/mrp/protobuf/ProtocolMessage.proto"{\n"SendPackedVirtualTouchEventMessage\x12\x0c\n\x04data\x18\x01 \x01(\x0c"G\n\x05Phase\x12\t\n\x05Began\x10\x01\x12\t\n\x05Moved\x10\x02\x12\x0e\n\nStationary\x10\x03\x12\t\n\x05Ended\x10\x04\x12\r\n\tCancelled\x10\x05:a\n"sendPackedVirtualTouchEventMessage\x12\x10.ProtocolMessage\x18/ \x01(\x0b2#.SendPackedVirtualTouchEventMessage')),
  dependencies=[
 pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.DESCRIPTOR])
SENDPACKEDVIRTUALTOUCHEVENTMESSAGE_FIELD_NUMBER = 47
sendPackedVirtualTouchEventMessage = _descriptor.FieldDescriptor(name='sendPackedVirtualTouchEventMessage',
  full_name='sendPackedVirtualTouchEventMessage',
  index=0,
  number=47,
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
_SENDPACKEDVIRTUALTOUCHEVENTMESSAGE_PHASE = _descriptor.EnumDescriptor(name='Phase',
  full_name='SendPackedVirtualTouchEventMessage.Phase',
  filename=None,
  file=DESCRIPTOR,
  values=[
 _descriptor.EnumValueDescriptor(name='Began',
   index=0,
   number=1,
   serialized_options=None,
   type=None),
 _descriptor.EnumValueDescriptor(name='Moved',
   index=1,
   number=2,
   serialized_options=None,
   type=None),
 _descriptor.EnumValueDescriptor(name='Stationary',
   index=2,
   number=3,
   serialized_options=None,
   type=None),
 _descriptor.EnumValueDescriptor(name='Ended',
   index=3,
   number=4,
   serialized_options=None,
   type=None),
 _descriptor.EnumValueDescriptor(name='Cancelled',
   index=4,
   number=5,
   serialized_options=None,
   type=None)],
  containing_type=None,
  serialized_options=None,
  serialized_start=157,
  serialized_end=228)
_sym_db.RegisterEnumDescriptor(_SENDPACKEDVIRTUALTOUCHEVENTMESSAGE_PHASE)
_SENDPACKEDVIRTUALTOUCHEVENTMESSAGE = _descriptor.Descriptor(name='SendPackedVirtualTouchEventMessage',
  full_name='SendPackedVirtualTouchEventMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='data',
   full_name='SendPackedVirtualTouchEventMessage.data',
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
  enum_types=[
 _SENDPACKEDVIRTUALTOUCHEVENTMESSAGE_PHASE],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=105,
  serialized_end=228)
_SENDPACKEDVIRTUALTOUCHEVENTMESSAGE_PHASE.containing_type = _SENDPACKEDVIRTUALTOUCHEVENTMESSAGE
DESCRIPTOR.message_types_by_name['SendPackedVirtualTouchEventMessage'] = _SENDPACKEDVIRTUALTOUCHEVENTMESSAGE
DESCRIPTOR.extensions_by_name['sendPackedVirtualTouchEventMessage'] = sendPackedVirtualTouchEventMessage
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
SendPackedVirtualTouchEventMessage = _reflection.GeneratedProtocolMessageType('SendPackedVirtualTouchEventMessage', (_message.Message,), {'DESCRIPTOR':_SENDPACKEDVIRTUALTOUCHEVENTMESSAGE, 
 '__module__':'pyatv.mrp.protobuf.SendPackedVirtualTouchEventMessage_pb2'})
_sym_db.RegisterMessage(SendPackedVirtualTouchEventMessage)
sendPackedVirtualTouchEventMessage.message_type = _SENDPACKEDVIRTUALTOUCHEVENTMESSAGE
pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.ProtocolMessage.RegisterExtension(sendPackedVirtualTouchEventMessage)