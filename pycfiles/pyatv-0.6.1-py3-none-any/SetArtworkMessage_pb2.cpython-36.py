# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/mrp/protobuf/SetArtworkMessage_pb2.py
# Compiled at: 2019-09-30 07:18:14
# Size of source mod 2**32: 2992 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from pyatv.mrp.protobuf import ProtocolMessage_pb2 as pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='pyatv/mrp/protobuf/SetArtworkMessage.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=(_b('\n*pyatv/mrp/protobuf/SetArtworkMessage.proto\x1a(pyatv/mrp/protobuf/ProtocolMessage.proto"%\n\x11SetArtworkMessage\x12\x10\n\x08jpegData\x18\x01 \x01(\x0c:?\n\x11setArtworkMessage\x12\x10.ProtocolMessage\x18\n \x01(\x0b2\x12.SetArtworkMessage')),
  dependencies=[
 pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.DESCRIPTOR])
SETARTWORKMESSAGE_FIELD_NUMBER = 10
setArtworkMessage = _descriptor.FieldDescriptor(name='setArtworkMessage',
  full_name='setArtworkMessage',
  index=0,
  number=10,
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
_SETARTWORKMESSAGE = _descriptor.Descriptor(name='SetArtworkMessage',
  full_name='SetArtworkMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='jpegData',
   full_name='SetArtworkMessage.jpegData',
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
  serialized_start=88,
  serialized_end=125)
DESCRIPTOR.message_types_by_name['SetArtworkMessage'] = _SETARTWORKMESSAGE
DESCRIPTOR.extensions_by_name['setArtworkMessage'] = setArtworkMessage
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
SetArtworkMessage = _reflection.GeneratedProtocolMessageType('SetArtworkMessage', (_message.Message,), {'DESCRIPTOR':_SETARTWORKMESSAGE, 
 '__module__':'pyatv.mrp.protobuf.SetArtworkMessage_pb2'})
_sym_db.RegisterMessage(SetArtworkMessage)
setArtworkMessage.message_type = _SETARTWORKMESSAGE
pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.ProtocolMessage.RegisterExtension(setArtworkMessage)