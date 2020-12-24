# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/mrp/protobuf/KeyboardMessage_pb2.py
# Compiled at: 2019-09-30 07:18:14
# Size of source mod 2**32: 4224 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from pyatv.mrp.protobuf import ProtocolMessage_pb2 as pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2
from pyatv.mrp.protobuf import TextEditingAttributesMessage_pb2 as pyatv_dot_mrp_dot_protobuf_dot_TextEditingAttributesMessage__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='pyatv/mrp/protobuf/KeyboardMessage.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=(_b('\n(pyatv/mrp/protobuf/KeyboardMessage.proto\x1a(pyatv/mrp/protobuf/ProtocolMessage.proto\x1a5pyatv/mrp/protobuf/TextEditingAttributesMessage.proto"m\n\x0fKeyboardMessage\x12\r\n\x05state\x18\x01 \x01(\x05\x12*\n\nattributes\x18\x03 \x01(\x0b2\x16.TextEditingAttributes\x12\x1f\n\x17encryptedTextCyphertext\x18\x04 \x01(\x0c:;\n\x0fkeyboardMessage\x12\x10.ProtocolMessage\x18\x1c \x01(\x0b2\x10.KeyboardMessage')),
  dependencies=[
 pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.DESCRIPTOR, pyatv_dot_mrp_dot_protobuf_dot_TextEditingAttributesMessage__pb2.DESCRIPTOR])
KEYBOARDMESSAGE_FIELD_NUMBER = 28
keyboardMessage = _descriptor.FieldDescriptor(name='keyboardMessage',
  full_name='keyboardMessage',
  index=0,
  number=28,
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
_KEYBOARDMESSAGE = _descriptor.Descriptor(name='KeyboardMessage',
  full_name='KeyboardMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='state',
   full_name='KeyboardMessage.state',
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
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='attributes',
   full_name='KeyboardMessage.attributes',
   index=1,
   number=3,
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
 _descriptor.FieldDescriptor(name='encryptedTextCyphertext',
   full_name='KeyboardMessage.encryptedTextCyphertext',
   index=2,
   number=4,
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
  serialized_start=141,
  serialized_end=250)
_KEYBOARDMESSAGE.fields_by_name['attributes'].message_type = pyatv_dot_mrp_dot_protobuf_dot_TextEditingAttributesMessage__pb2._TEXTEDITINGATTRIBUTES
DESCRIPTOR.message_types_by_name['KeyboardMessage'] = _KEYBOARDMESSAGE
DESCRIPTOR.extensions_by_name['keyboardMessage'] = keyboardMessage
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
KeyboardMessage = _reflection.GeneratedProtocolMessageType('KeyboardMessage', (_message.Message,), {'DESCRIPTOR':_KEYBOARDMESSAGE, 
 '__module__':'pyatv.mrp.protobuf.KeyboardMessage_pb2'})
_sym_db.RegisterMessage(KeyboardMessage)
keyboardMessage.message_type = _KEYBOARDMESSAGE
pyatv_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.ProtocolMessage.RegisterExtension(keyboardMessage)