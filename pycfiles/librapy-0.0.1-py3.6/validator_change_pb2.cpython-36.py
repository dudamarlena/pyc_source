# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/librapy/proto/validator_change_pb2.py
# Compiled at: 2019-09-11 21:20:08
# Size of source mod 2**32: 3154 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
import events_pb2 as events__pb2, ledger_info_pb2 as ledger__info__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='validator_change.proto',
  package='types',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=(_b('\n\x16validator_change.proto\x12\x05types\x1a\x0cevents.proto\x1a\x11ledger_info.proto"\x90\x01\n\x1dValidatorChangeEventWithProof\x12>\n\x15ledger_info_with_sigs\x18\x01 \x01(\x0b2\x1f.types.LedgerInfoWithSignatures\x12/\n\x10event_with_proof\x18\x02 \x01(\x0b2\x15.types.EventWithProofb\x06proto3')),
  dependencies=[
 events__pb2.DESCRIPTOR, ledger__info__pb2.DESCRIPTOR])
_VALIDATORCHANGEEVENTWITHPROOF = _descriptor.Descriptor(name='ValidatorChangeEventWithProof',
  full_name='types.ValidatorChangeEventWithProof',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='ledger_info_with_sigs',
   full_name='types.ValidatorChangeEventWithProof.ledger_info_with_sigs',
   index=0,
   number=1,
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
 _descriptor.FieldDescriptor(name='event_with_proof',
   full_name='types.ValidatorChangeEventWithProof.event_with_proof',
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
  serialized_start=67,
  serialized_end=211)
_VALIDATORCHANGEEVENTWITHPROOF.fields_by_name['ledger_info_with_sigs'].message_type = ledger__info__pb2._LEDGERINFOWITHSIGNATURES
_VALIDATORCHANGEEVENTWITHPROOF.fields_by_name['event_with_proof'].message_type = events__pb2._EVENTWITHPROOF
DESCRIPTOR.message_types_by_name['ValidatorChangeEventWithProof'] = _VALIDATORCHANGEEVENTWITHPROOF
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
ValidatorChangeEventWithProof = _reflection.GeneratedProtocolMessageType('ValidatorChangeEventWithProof', (_message.Message,), {'DESCRIPTOR':_VALIDATORCHANGEEVENTWITHPROOF, 
 '__module__':'validator_change_pb2'})
_sym_db.RegisterMessage(ValidatorChangeEventWithProof)