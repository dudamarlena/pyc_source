# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/site-packages/cothority/status_pb2.py
# Compiled at: 2017-05-18 05:01:33
# Size of source mod 2**32: 7986 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
_sym_db = _symbol_database.Default()
import network_pb2 as network__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='status.proto',
  package='',
  syntax='proto2',
  serialized_pb=(_b('\n\x0cstatus.proto\x1a\rnetwork.proto"\t\n\x07Request"ÿ\x01\n\x08Response\x12%\n\x06system\x18\x01 \x03(\x0b2\x15.Response.SystemEntry\x12\'\n\x06server\x18\x02 \x01(\x0b2\x17.network.ServerIdentity\x1a?\n\x0bSystemEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1f\n\x05value\x18\x02 \x01(\x0b2\x10.Response.Status:\x028\x01\x1ab\n\x06Status\x12*\n\x05field\x18\x01 \x03(\x0b2\x1b.Response.Status.FieldEntry\x1a,\n\nFieldEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x028\x01')),
  dependencies=[
 network__pb2.DESCRIPTOR])
_REQUEST = _descriptor.Descriptor(name='Request',
  full_name='Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=31,
  serialized_end=40)
_RESPONSE_SYSTEMENTRY = _descriptor.Descriptor(name='SystemEntry',
  full_name='Response.SystemEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='key',
   full_name='Response.SystemEntry.key',
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
   options=None),
 _descriptor.FieldDescriptor(name='value',
   full_name='Response.SystemEntry.value',
   index=1,
   number=2,
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
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=(_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\x01'))),
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=135,
  serialized_end=198)
_RESPONSE_STATUS_FIELDENTRY = _descriptor.Descriptor(name='FieldEntry',
  full_name='Response.Status.FieldEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='key',
   full_name='Response.Status.FieldEntry.key',
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
   options=None),
 _descriptor.FieldDescriptor(name='value',
   full_name='Response.Status.FieldEntry.value',
   index=1,
   number=2,
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
   options=None)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  options=(_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\x01'))),
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=254,
  serialized_end=298)
_RESPONSE_STATUS = _descriptor.Descriptor(name='Status',
  full_name='Response.Status',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='field',
   full_name='Response.Status.field',
   index=0,
   number=1,
   type=11,
   cpp_type=10,
   label=3,
   has_default_value=False,
   default_value=[],
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None)],
  extensions=[],
  nested_types=[
 _RESPONSE_STATUS_FIELDENTRY],
  enum_types=[],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=200,
  serialized_end=298)
_RESPONSE = _descriptor.Descriptor(name='Response',
  full_name='Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='system',
   full_name='Response.system',
   index=0,
   number=1,
   type=11,
   cpp_type=10,
   label=3,
   has_default_value=False,
   default_value=[],
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   options=None),
 _descriptor.FieldDescriptor(name='server',
   full_name='Response.server',
   index=1,
   number=2,
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
   options=None)],
  extensions=[],
  nested_types=[
 _RESPONSE_SYSTEMENTRY, _RESPONSE_STATUS],
  enum_types=[],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=43,
  serialized_end=298)
_RESPONSE_SYSTEMENTRY.fields_by_name['value'].message_type = _RESPONSE_STATUS
_RESPONSE_SYSTEMENTRY.containing_type = _RESPONSE
_RESPONSE_STATUS_FIELDENTRY.containing_type = _RESPONSE_STATUS
_RESPONSE_STATUS.fields_by_name['field'].message_type = _RESPONSE_STATUS_FIELDENTRY
_RESPONSE_STATUS.containing_type = _RESPONSE
_RESPONSE.fields_by_name['system'].message_type = _RESPONSE_SYSTEMENTRY
_RESPONSE.fields_by_name['server'].message_type = network__pb2._SERVERIDENTITY
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(DESCRIPTOR=_REQUEST,
  __module__='status_pb2'))
_sym_db.RegisterMessage(Request)
Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(SystemEntry=(_reflection.GeneratedProtocolMessageType('SystemEntry', (_message.Message,), dict(DESCRIPTOR=_RESPONSE_SYSTEMENTRY,
  __module__='status_pb2'))),
  Status=(_reflection.GeneratedProtocolMessageType('Status', (_message.Message,), dict(FieldEntry=(_reflection.GeneratedProtocolMessageType('FieldEntry', (_message.Message,), dict(DESCRIPTOR=_RESPONSE_STATUS_FIELDENTRY,
  __module__='status_pb2'))),
  DESCRIPTOR=_RESPONSE_STATUS,
  __module__='status_pb2'))),
  DESCRIPTOR=_RESPONSE,
  __module__='status_pb2'))
_sym_db.RegisterMessage(Response)
_sym_db.RegisterMessage(Response.SystemEntry)
_sym_db.RegisterMessage(Response.Status)
_sym_db.RegisterMessage(Response.Status.FieldEntry)
_RESPONSE_SYSTEMENTRY.has_options = True
_RESPONSE_SYSTEMENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\x01'))
_RESPONSE_STATUS_FIELDENTRY.has_options = True
_RESPONSE_STATUS_FIELDENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\x01'))