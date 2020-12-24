# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/librapy/proto/validator_public_keys_pb2.py
# Compiled at: 2019-09-11 21:20:08
# Size of source mod 2**32: 3483 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='validator_public_keys.proto',
  package='types',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=(_b('\n\x1bvalidator_public_keys.proto\x12\x05types"\x95\x01\n\x13ValidatorPublicKeys\x12\x17\n\x0faccount_address\x18\x01 \x01(\x0c\x12\x1c\n\x14consensus_public_key\x18\x02 \x01(\x0c\x12"\n\x1anetwork_signing_public_key\x18\x03 \x01(\x0c\x12#\n\x1bnetwork_identity_public_key\x18\x04 \x01(\x0cb\x06proto3')))
_VALIDATORPUBLICKEYS = _descriptor.Descriptor(name='ValidatorPublicKeys',
  full_name='types.ValidatorPublicKeys',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='account_address',
   full_name='types.ValidatorPublicKeys.account_address',
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
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='consensus_public_key',
   full_name='types.ValidatorPublicKeys.consensus_public_key',
   index=1,
   number=2,
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
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='network_signing_public_key',
   full_name='types.ValidatorPublicKeys.network_signing_public_key',
   index=2,
   number=3,
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
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='network_identity_public_key',
   full_name='types.ValidatorPublicKeys.network_identity_public_key',
   index=3,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[],
  serialized_start=39,
  serialized_end=188)
DESCRIPTOR.message_types_by_name['ValidatorPublicKeys'] = _VALIDATORPUBLICKEYS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
ValidatorPublicKeys = _reflection.GeneratedProtocolMessageType('ValidatorPublicKeys', (_message.Message,), {'DESCRIPTOR':_VALIDATORPUBLICKEYS, 
 '__module__':'validator_public_keys_pb2'})
_sym_db.RegisterMessage(ValidatorPublicKeys)