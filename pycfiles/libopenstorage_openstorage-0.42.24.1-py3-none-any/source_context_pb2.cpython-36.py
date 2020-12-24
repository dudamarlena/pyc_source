# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/source_context_pb2.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 2385 bytes
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='google/protobuf/source_context.proto',
  package='google.protobuf',
  syntax='proto3',
  serialized_options=b'\n\x13com.google.protobufB\x12SourceContextProtoP\x01ZAgoogle.golang.org/genproto/protobuf/source_context;source_context\xa2\x02\x03GPB\xaa\x02\x1eGoogle.Protobuf.WellKnownTypes',
  serialized_pb=b'\n$google/protobuf/source_context.proto\x12\x0fgoogle.protobuf""\n\rSourceContext\x12\x11\n\tfile_name\x18\x01 \x01(\tB\x95\x01\n\x13com.google.protobufB\x12SourceContextProtoP\x01ZAgoogle.golang.org/genproto/protobuf/source_context;source_context\xa2\x02\x03GPB\xaa\x02\x1eGoogle.Protobuf.WellKnownTypesb\x06proto3')
_SOURCECONTEXT = _descriptor.Descriptor(name='SourceContext',
  full_name='google.protobuf.SourceContext',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='file_name',
   full_name='google.protobuf.SourceContext.file_name',
   index=0,
   number=1,
   type=9,
   cpp_type=9,
   label=1,
   has_default_value=False,
   default_value=((b'').decode('utf-8')),
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
  serialized_start=57,
  serialized_end=91)
DESCRIPTOR.message_types_by_name['SourceContext'] = _SOURCECONTEXT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
SourceContext = _reflection.GeneratedProtocolMessageType('SourceContext', (_message.Message,), {'DESCRIPTOR':_SOURCECONTEXT, 
 '__module__':'google.protobuf.source_context_pb2'})
_sym_db.RegisterMessage(SourceContext)
DESCRIPTOR._options = None