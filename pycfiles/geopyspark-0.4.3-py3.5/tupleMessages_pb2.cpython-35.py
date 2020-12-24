# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/geopyspark/geotrellis/protobuf/tupleMessages_pb2.py
# Compiled at: 2018-11-28 11:44:02
# Size of source mod 2**32: 4937 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
_sym_db = _symbol_database.Default()
from geopyspark.geotrellis.protobuf import extentMessages_pb2 as extentMessages__pb2
from geopyspark.geotrellis.protobuf import keyMessages_pb2 as keyMessages__pb2
from geopyspark.geotrellis.protobuf import tileMessages_pb2 as tileMessages__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='tupleMessages.proto', package='protos', syntax='proto3', serialized_pb=_b('\n\x13tupleMessages.proto\x12\x06protos\x1a\x14extentMessages.proto\x1a\x11keyMessages.proto\x1a\x12tileMessages.proto"§\x02\n\nProtoTuple\x125\n\x0fprojectedExtent\x18\x01 \x01(\x0b2\x1c.protos.ProtoProjectedExtent\x12E\n\x17temporalProjectedExtent\x18\x02 \x01(\x0b2$.protos.ProtoTemporalProjectedExtent\x12+\n\nspatialKey\x18\x03 \x01(\x0b2\x17.protos.ProtoSpatialKey\x12/\n\x0cspaceTimeKey\x18\x04 \x01(\x0b2\x19.protos.ProtoSpaceTimeKey\x12)\n\x05tiles\x18\x05 \x01(\x0b2\x1a.protos.ProtoMultibandTile\x12\x12\n\nimageBytes\x18\x06 \x01(\x0cb\x06proto3'), dependencies=[
 extentMessages__pb2.DESCRIPTOR, keyMessages__pb2.DESCRIPTOR, tileMessages__pb2.DESCRIPTOR])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
_PROTOTUPLE = _descriptor.Descriptor(name='ProtoTuple', full_name='protos.ProtoTuple', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='projectedExtent', full_name='protos.ProtoTuple.projectedExtent', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='temporalProjectedExtent', full_name='protos.ProtoTuple.temporalProjectedExtent', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='spatialKey', full_name='protos.ProtoTuple.spatialKey', index=2, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='spaceTimeKey', full_name='protos.ProtoTuple.spaceTimeKey', index=3, number=4, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='tiles', full_name='protos.ProtoTuple.tiles', index=4, number=5, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='imageBytes', full_name='protos.ProtoTuple.imageBytes', index=5, number=6, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=93, serialized_end=388)
_PROTOTUPLE.fields_by_name['projectedExtent'].message_type = extentMessages__pb2._PROTOPROJECTEDEXTENT
_PROTOTUPLE.fields_by_name['temporalProjectedExtent'].message_type = extentMessages__pb2._PROTOTEMPORALPROJECTEDEXTENT
_PROTOTUPLE.fields_by_name['spatialKey'].message_type = keyMessages__pb2._PROTOSPATIALKEY
_PROTOTUPLE.fields_by_name['spaceTimeKey'].message_type = keyMessages__pb2._PROTOSPACETIMEKEY
_PROTOTUPLE.fields_by_name['tiles'].message_type = tileMessages__pb2._PROTOMULTIBANDTILE
DESCRIPTOR.message_types_by_name['ProtoTuple'] = _PROTOTUPLE
ProtoTuple = _reflection.GeneratedProtocolMessageType('ProtoTuple', (_message.Message,), dict(DESCRIPTOR=_PROTOTUPLE, __module__='tupleMessages_pb2'))
_sym_db.RegisterMessage(ProtoTuple)