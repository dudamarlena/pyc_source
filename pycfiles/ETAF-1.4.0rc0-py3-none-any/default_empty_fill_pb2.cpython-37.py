# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/arch/api/proto/default_empty_fill_pb2.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 2982 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
import google.protobuf as _descriptor
import google.protobuf as _message
import google.protobuf as _reflection
import google.protobuf as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='default-empty-fill.proto',
  package='com.webank.ai.fate.core.mlmodel.buffer',
  syntax='proto3',
  serialized_options=(_b('B\x15DefaultEmptyFillProto')),
  serialized_pb=(_b('\n\x18default-empty-fill.proto\x12&com.webank.ai.fate.core.mlmodel.buffer"\'\n\x17DefaultEmptyFillMessage\x12\x0c\n\x04flag\x18\x01 \x01(\tB\x17B\x15DefaultEmptyFillProtob\x06proto3')))
_DEFAULTEMPTYFILLMESSAGE = _descriptor.Descriptor(name='DefaultEmptyFillMessage',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.DefaultEmptyFillMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='flag',
   full_name='com.webank.ai.fate.core.mlmodel.buffer.DefaultEmptyFillMessage.flag',
   index=0,
   number=1,
   type=9,
   cpp_type=9,
   label=1,
   has_default_value=False,
   default_value=(_b('').decode('utf-8')),
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
  serialized_start=68,
  serialized_end=107)
DESCRIPTOR.message_types_by_name['DefaultEmptyFillMessage'] = _DEFAULTEMPTYFILLMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
DefaultEmptyFillMessage = _reflection.GeneratedProtocolMessageType('DefaultEmptyFillMessage', (_message.Message,), dict(DESCRIPTOR=_DEFAULTEMPTYFILLMESSAGE,
  __module__='default_empty_fill_pb2'))
_sym_db.RegisterMessage(DefaultEmptyFillMessage)
DESCRIPTOR._options = None