# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/mrp/protobuf/RegisterForGameControllerEventsMessage_pb2.py
# Compiled at: 2019-09-30 07:18:14
# Size of source mod 2**32: 4540 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from pyatv.mrp.protobuf import ProtocolMessage_pb2 as pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='pyatv/mrp/protobuf/RegisterForGameControllerEventsMessage.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=(_b('\n?pyatv/mrp/protobuf/RegisterForGameControllerEventsMessage.proto\x1a(pyatv/mrp/protobuf/ProtocolMessage.proto"\x94\x01\n&RegisterForGameControllerEventsMessage\x12N\n\x0einputModeFlags\x18\x01 \x01(\x0e26.RegisterForGameControllerEventsMessage.InputModeFlags"\x1a\n\x0eInputModeFlags\x12\x08\n\x04None\x10\x00:i\n&registerForGameControllerEventsMessage\x12\x10.ProtocolMessage\x18\x1b \x01(\x0b2\'.RegisterForGameControllerEventsMessage')),
  dependencies=[
 pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.DESCRIPTOR])
REGISTERFORGAMECONTROLLEREVENTSMESSAGE_FIELD_NUMBER = 27
registerForGameControllerEventsMessage = _descriptor.FieldDescriptor(name='registerForGameControllerEventsMessage',
  full_name='registerForGameControllerEventsMessage',
  index=0,
  number=27,
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
_REGISTERFORGAMECONTROLLEREVENTSMESSAGE_INPUTMODEFLAGS = _descriptor.EnumDescriptor(name='InputModeFlags',
  full_name='RegisterForGameControllerEventsMessage.InputModeFlags',
  filename=None,
  file=DESCRIPTOR,
  values=[
 _descriptor.EnumValueDescriptor(name='None',
   index=0,
   number=0,
   serialized_options=None,
   type=None)],
  containing_type=None,
  serialized_options=None,
  serialized_start=232,
  serialized_end=258)
_sym_db.RegisterEnumDescriptor(_REGISTERFORGAMECONTROLLEREVENTSMESSAGE_INPUTMODEFLAGS)
_REGISTERFORGAMECONTROLLEREVENTSMESSAGE = _descriptor.Descriptor(name='RegisterForGameControllerEventsMessage',
  full_name='RegisterForGameControllerEventsMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='inputModeFlags',
   full_name='RegisterForGameControllerEventsMessage.inputModeFlags',
   index=0,
   number=1,
   type=14,
   cpp_type=8,
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
  enum_types=[
 _REGISTERFORGAMECONTROLLEREVENTSMESSAGE_INPUTMODEFLAGS],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=110,
  serialized_end=258)
_REGISTERFORGAMECONTROLLEREVENTSMESSAGE.fields_by_name['inputModeFlags'].enum_type = _REGISTERFORGAMECONTROLLEREVENTSMESSAGE_INPUTMODEFLAGS
_REGISTERFORGAMECONTROLLEREVENTSMESSAGE_INPUTMODEFLAGS.containing_type = _REGISTERFORGAMECONTROLLEREVENTSMESSAGE
DESCRIPTOR.message_types_by_name['RegisterForGameControllerEventsMessage'] = _REGISTERFORGAMECONTROLLEREVENTSMESSAGE
DESCRIPTOR.extensions_by_name['registerForGameControllerEventsMessage'] = registerForGameControllerEventsMessage
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
RegisterForGameControllerEventsMessage = _reflection.GeneratedProtocolMessageType('RegisterForGameControllerEventsMessage', (_message.Message,), {'DESCRIPTOR':_REGISTERFORGAMECONTROLLEREVENTSMESSAGE, 
 '__module__':'pyatv.mrp.protobuf.RegisterForGameControllerEventsMessage_pb2'})
_sym_db.RegisterMessage(RegisterForGameControllerEventsMessage)
registerForGameControllerEventsMessage.message_type = _REGISTERFORGAMECONTROLLEREVENTSMESSAGE
pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.ProtocolMessage.RegisterExtension(registerForGameControllerEventsMessage)