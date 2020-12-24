# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/mrp/protobuf/SendCommandResultMessage_pb2.py
# Compiled at: 2019-09-30 07:18:14
# Size of source mod 2**32: 4064 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from pyatv.mrp.protobuf import ProtocolMessage_pb2 as pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='pyatv/mrp/protobuf/SendCommandResultMessage.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=(_b('\n1pyatv/mrp/protobuf/SendCommandResultMessage.proto\x1a(pyatv/mrp/protobuf/ProtocolMessage.proto"l\n\x18SendCommandResultMessage\x12\x11\n\terrorCode\x18\x01 \x01(\r\x12\x1b\n\x13handlerReturnStatus\x18\x02 \x01(\r\x12 \n\x18handlerReturnStatusDatas\x18\x03 \x03(\x0c:M\n\x18sendCommandResultMessage\x12\x10.ProtocolMessage\x18\x07 \x01(\x0b2\x19.SendCommandResultMessage')),
  dependencies=[
 pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.DESCRIPTOR])
SENDCOMMANDRESULTMESSAGE_FIELD_NUMBER = 7
sendCommandResultMessage = _descriptor.FieldDescriptor(name='sendCommandResultMessage',
  full_name='sendCommandResultMessage',
  index=0,
  number=7,
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
_SENDCOMMANDRESULTMESSAGE = _descriptor.Descriptor(name='SendCommandResultMessage',
  full_name='SendCommandResultMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='errorCode',
   full_name='SendCommandResultMessage.errorCode',
   index=0,
   number=1,
   type=13,
   cpp_type=3,
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
 _descriptor.FieldDescriptor(name='handlerReturnStatus',
   full_name='SendCommandResultMessage.handlerReturnStatus',
   index=1,
   number=2,
   type=13,
   cpp_type=3,
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
 _descriptor.FieldDescriptor(name='handlerReturnStatusDatas',
   full_name='SendCommandResultMessage.handlerReturnStatusDatas',
   index=2,
   number=3,
   type=12,
   cpp_type=9,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=95,
  serialized_end=203)
DESCRIPTOR.message_types_by_name['SendCommandResultMessage'] = _SENDCOMMANDRESULTMESSAGE
DESCRIPTOR.extensions_by_name['sendCommandResultMessage'] = sendCommandResultMessage
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
SendCommandResultMessage = _reflection.GeneratedProtocolMessageType('SendCommandResultMessage', (_message.Message,), {'DESCRIPTOR':_SENDCOMMANDRESULTMESSAGE, 
 '__module__':'pyatv.mrp.protobuf.SendCommandResultMessage_pb2'})
_sym_db.RegisterMessage(SendCommandResultMessage)
sendCommandResultMessage.message_type = _SENDCOMMANDRESULTMESSAGE
pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.ProtocolMessage.RegisterExtension(sendCommandResultMessage)