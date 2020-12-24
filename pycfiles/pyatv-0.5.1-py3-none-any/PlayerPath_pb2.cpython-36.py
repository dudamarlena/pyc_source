# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/mrp/protobuf/PlayerPath_pb2.py
# Compiled at: 2019-09-30 07:18:14
# Size of source mod 2**32: 3757 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from pyatv.mrp.protobuf import Origin_pb2 as pyatv_dot_mrp_dot_protobuf_dot_Origin__pb2
from pyatv.mrp.protobuf import NowPlayingClient_pb2 as pyatv_dot_mrp_dot_protobuf_dot_NowPlayingClient__pb2
from pyatv.mrp.protobuf import NowPlayingPlayer_pb2 as pyatv_dot_mrp_dot_protobuf_dot_NowPlayingPlayer__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='pyatv/mrp/protobuf/PlayerPath.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=(_b('\n#pyatv/mrp/protobuf/PlayerPath.proto\x1a\x1fpyatv/mrp/protobuf/Origin.proto\x1a)pyatv/mrp/protobuf/NowPlayingClient.proto\x1a)pyatv/mrp/protobuf/NowPlayingPlayer.proto"k\n\nPlayerPath\x12\x17\n\x06origin\x18\x01 \x01(\x0b2\x07.Origin\x12!\n\x06client\x18\x02 \x01(\x0b2\x11.NowPlayingClient\x12!\n\x06player\x18\x03 \x01(\x0b2\x11.NowPlayingPlayer')),
  dependencies=[
 pyatv_dot_mrp_dot_protobuf_dot_Origin__pb2.DESCRIPTOR, pyatv_dot_mrp_dot_protobuf_dot_NowPlayingClient__pb2.DESCRIPTOR, pyatv_dot_mrp_dot_protobuf_dot_NowPlayingPlayer__pb2.DESCRIPTOR])
_PLAYERPATH = _descriptor.Descriptor(name='PlayerPath',
  full_name='PlayerPath',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='origin',
   full_name='PlayerPath.origin',
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
 _descriptor.FieldDescriptor(name='client',
   full_name='PlayerPath.client',
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
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='player',
   full_name='PlayerPath.player',
   index=2,
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
   file=DESCRIPTOR)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=158,
  serialized_end=265)
_PLAYERPATH.fields_by_name['origin'].message_type = pyatv_dot_mrp_dot_protobuf_dot_Origin__pb2._ORIGIN
_PLAYERPATH.fields_by_name['client'].message_type = pyatv_dot_mrp_dot_protobuf_dot_NowPlayingClient__pb2._NOWPLAYINGCLIENT
_PLAYERPATH.fields_by_name['player'].message_type = pyatv_dot_mrp_dot_protobuf_dot_NowPlayingPlayer__pb2._NOWPLAYINGPLAYER
DESCRIPTOR.message_types_by_name['PlayerPath'] = _PLAYERPATH
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
PlayerPath = _reflection.GeneratedProtocolMessageType('PlayerPath', (_message.Message,), {'DESCRIPTOR':_PLAYERPATH, 
 '__module__':'pyatv.mrp.protobuf.PlayerPath_pb2'})
_sym_db.RegisterMessage(PlayerPath)