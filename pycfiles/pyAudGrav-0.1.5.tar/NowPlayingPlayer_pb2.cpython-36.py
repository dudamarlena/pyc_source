# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/mrp/protobuf/NowPlayingPlayer_pb2.py
# Compiled at: 2019-09-30 07:18:14
# Size of source mod 2**32: 2899 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='pyatv/mrp/protobuf/NowPlayingPlayer.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=(_b('\n)pyatv/mrp/protobuf/NowPlayingPlayer.proto"T\n\x10NowPlayingPlayer\x12\x12\n\nidentifier\x18\x01 \x01(\t\x12\x13\n\x0bdisplayName\x18\x02 \x01(\t\x12\x17\n\x0fisDefaultPlayer\x18\x03 \x01(\x08')))
_NOWPLAYINGPLAYER = _descriptor.Descriptor(name='NowPlayingPlayer',
  full_name='NowPlayingPlayer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='identifier',
   full_name='NowPlayingPlayer.identifier',
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
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='displayName',
   full_name='NowPlayingPlayer.displayName',
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
   serialized_options=None,
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='isDefaultPlayer',
   full_name='NowPlayingPlayer.isDefaultPlayer',
   index=2,
   number=3,
   type=8,
   cpp_type=7,
   label=1,
   has_default_value=False,
   default_value=False,
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
  serialized_start=45,
  serialized_end=129)
DESCRIPTOR.message_types_by_name['NowPlayingPlayer'] = _NOWPLAYINGPLAYER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
NowPlayingPlayer = _reflection.GeneratedProtocolMessageType('NowPlayingPlayer', (_message.Message,), {'DESCRIPTOR':_NOWPLAYINGPLAYER, 
 '__module__':'pyatv.mrp.protobuf.NowPlayingPlayer_pb2'})
_sym_db.RegisterMessage(NowPlayingPlayer)