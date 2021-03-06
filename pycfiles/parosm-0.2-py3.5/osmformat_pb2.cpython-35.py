# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parosm/parse/osmformat_pb2.py
# Compiled at: 2018-04-05 13:14:55
# Size of source mod 2**32: 39639 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='osmformat.proto', package='OSMPBF', syntax='proto2', serialized_pb=_b('\n\x0fosmformat.proto\x12\x06OSMPBF"\x87\x02\n\x0bHeaderBlock\x12 \n\x04bbox\x18\x01 \x01(\x0b2\x12.OSMPBF.HeaderBBox\x12\x19\n\x11required_features\x18\x04 \x03(\t\x12\x19\n\x11optional_features\x18\x05 \x03(\t\x12\x16\n\x0ewritingprogram\x18\x10 \x01(\t\x12\x0e\n\x06source\x18\x11 \x01(\t\x12%\n\x1dosmosis_replication_timestamp\x18  \x01(\x03\x12+\n#osmosis_replication_sequence_number\x18! \x01(\x03\x12$\n\x1cosmosis_replication_base_url\x18" \x01(\t"F\n\nHeaderBBox\x12\x0c\n\x04left\x18\x01 \x02(\x12\x12\r\n\x05right\x18\x02 \x02(\x12\x12\x0b\n\x03top\x18\x03 \x02(\x12\x12\x0e\n\x06bottom\x18\x04 \x02(\x12"Ò\x01\n\x0ePrimitiveBlock\x12(\n\x0bstringtable\x18\x01 \x02(\x0b2\x13.OSMPBF.StringTable\x12.\n\x0eprimitivegroup\x18\x02 \x03(\x0b2\x16.OSMPBF.PrimitiveGroup\x12\x18\n\x0bgranularity\x18\x11 \x01(\x05:\x03100\x12\x15\n\nlat_offset\x18\x13 \x01(\x03:\x010\x12\x15\n\nlon_offset\x18\x14 \x01(\x03:\x010\x12\x1e\n\x10date_granularity\x18\x12 \x01(\x05:\x041000"·\x01\n\x0ePrimitiveGroup\x12\x1b\n\x05nodes\x18\x01 \x03(\x0b2\x0c.OSMPBF.Node\x12!\n\x05dense\x18\x02 \x01(\x0b2\x12.OSMPBF.DenseNodes\x12\x19\n\x04ways\x18\x03 \x03(\x0b2\x0b.OSMPBF.Way\x12#\n\trelations\x18\x04 \x03(\x0b2\x10.OSMPBF.Relation\x12%\n\nchangesets\x18\x05 \x03(\x0b2\x11.OSMPBF.ChangeSet"\x18\n\x0bStringTable\x12\t\n\x01s\x18\x01 \x03(\x0c"q\n\x04Info\x12\x13\n\x07version\x18\x01 \x01(\x05:\x02-1\x12\x11\n\ttimestamp\x18\x02 \x01(\x03\x12\x11\n\tchangeset\x18\x03 \x01(\x03\x12\x0b\n\x03uid\x18\x04 \x01(\x05\x12\x10\n\x08user_sid\x18\x05 \x01(\r\x12\x0f\n\x07visible\x18\x06 \x01(\x08"\x8a\x01\n\tDenseInfo\x12\x13\n\x07version\x18\x01 \x03(\x05B\x02\x10\x01\x12\x15\n\ttimestamp\x18\x02 \x03(\x12B\x02\x10\x01\x12\x15\n\tchangeset\x18\x03 \x03(\x12B\x02\x10\x01\x12\x0f\n\x03uid\x18\x04 \x03(\x11B\x02\x10\x01\x12\x14\n\x08user_sid\x18\x05 \x03(\x11B\x02\x10\x01\x12\x13\n\x07visible\x18\x06 \x03(\x08B\x02\x10\x01"\x17\n\tChangeSet\x12\n\n\x02id\x18\x01 \x02(\x03"l\n\x04Node\x12\n\n\x02id\x18\x01 \x02(\x12\x12\x10\n\x04keys\x18\x02 \x03(\rB\x02\x10\x01\x12\x10\n\x04vals\x18\x03 \x03(\rB\x02\x10\x01\x12\x1a\n\x04info\x18\x04 \x01(\x0b2\x0c.OSMPBF.Info\x12\x0b\n\x03lat\x18\x08 \x02(\x12\x12\x0b\n\x03lon\x18\t \x02(\x12"{\n\nDenseNodes\x12\x0e\n\x02id\x18\x01 \x03(\x12B\x02\x10\x01\x12$\n\tdenseinfo\x18\x05 \x01(\x0b2\x11.OSMPBF.DenseInfo\x12\x0f\n\x03lat\x18\x08 \x03(\x12B\x02\x10\x01\x12\x0f\n\x03lon\x18\t \x03(\x12B\x02\x10\x01\x12\x15\n\tkeys_vals\x18\n \x03(\x05B\x02\x10\x01"c\n\x03Way\x12\n\n\x02id\x18\x01 \x02(\x03\x12\x10\n\x04keys\x18\x02 \x03(\rB\x02\x10\x01\x12\x10\n\x04vals\x18\x03 \x03(\rB\x02\x10\x01\x12\x1a\n\x04info\x18\x04 \x01(\x0b2\x0c.OSMPBF.Info\x12\x10\n\x04refs\x18\x08 \x03(\x12B\x02\x10\x01"à\x01\n\x08Relation\x12\n\n\x02id\x18\x01 \x02(\x03\x12\x10\n\x04keys\x18\x02 \x03(\rB\x02\x10\x01\x12\x10\n\x04vals\x18\x03 \x03(\rB\x02\x10\x01\x12\x1a\n\x04info\x18\x04 \x01(\x0b2\x0c.OSMPBF.Info\x12\x15\n\troles_sid\x18\x08 \x03(\x05B\x02\x10\x01\x12\x12\n\x06memids\x18\t \x03(\x12B\x02\x10\x01\x12.\n\x05types\x18\n \x03(\x0e2\x1b.OSMPBF.Relation.MemberTypeB\x02\x10\x01"-\n\nMemberType\x12\x08\n\x04NODE\x10\x00\x12\x07\n\x03WAY\x10\x01\x12\x0c\n\x08RELATION\x10\x02B\x11\n\rcrosby.binaryH\x03'))
_RELATION_MEMBERTYPE = _descriptor.EnumDescriptor(name='MemberType', full_name='OSMPBF.Relation.MemberType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='NODE', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='WAY', index=1, number=1, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='RELATION', index=2, number=2, options=None, type=None)], containing_type=None, options=None, serialized_start=1587, serialized_end=1632)
_sym_db.RegisterEnumDescriptor(_RELATION_MEMBERTYPE)
_HEADERBLOCK = _descriptor.Descriptor(name='HeaderBlock', full_name='OSMPBF.HeaderBlock', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='bbox', full_name='OSMPBF.HeaderBlock.bbox', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='required_features', full_name='OSMPBF.HeaderBlock.required_features', index=1, number=4, type=9, cpp_type=9, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='optional_features', full_name='OSMPBF.HeaderBlock.optional_features', index=2, number=5, type=9, cpp_type=9, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='writingprogram', full_name='OSMPBF.HeaderBlock.writingprogram', index=3, number=16, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='source', full_name='OSMPBF.HeaderBlock.source', index=4, number=17, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='osmosis_replication_timestamp', full_name='OSMPBF.HeaderBlock.osmosis_replication_timestamp', index=5, number=32, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='osmosis_replication_sequence_number', full_name='OSMPBF.HeaderBlock.osmosis_replication_sequence_number', index=6, number=33, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='osmosis_replication_base_url', full_name='OSMPBF.HeaderBlock.osmosis_replication_base_url', index=7, number=34, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[], serialized_start=28, serialized_end=291)
_HEADERBBOX = _descriptor.Descriptor(name='HeaderBBox', full_name='OSMPBF.HeaderBBox', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='left', full_name='OSMPBF.HeaderBBox.left', index=0, number=1, type=18, cpp_type=2, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='right', full_name='OSMPBF.HeaderBBox.right', index=1, number=2, type=18, cpp_type=2, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='top', full_name='OSMPBF.HeaderBBox.top', index=2, number=3, type=18, cpp_type=2, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='bottom', full_name='OSMPBF.HeaderBBox.bottom', index=3, number=4, type=18, cpp_type=2, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[], serialized_start=293, serialized_end=363)
_PRIMITIVEBLOCK = _descriptor.Descriptor(name='PrimitiveBlock', full_name='OSMPBF.PrimitiveBlock', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='stringtable', full_name='OSMPBF.PrimitiveBlock.stringtable', index=0, number=1, type=11, cpp_type=10, label=2, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='primitivegroup', full_name='OSMPBF.PrimitiveBlock.primitivegroup', index=1, number=2, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='granularity', full_name='OSMPBF.PrimitiveBlock.granularity', index=2, number=17, type=5, cpp_type=1, label=1, has_default_value=True, default_value=100, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='lat_offset', full_name='OSMPBF.PrimitiveBlock.lat_offset', index=3, number=19, type=3, cpp_type=2, label=1, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='lon_offset', full_name='OSMPBF.PrimitiveBlock.lon_offset', index=4, number=20, type=3, cpp_type=2, label=1, has_default_value=True, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='date_granularity', full_name='OSMPBF.PrimitiveBlock.date_granularity', index=5, number=18, type=5, cpp_type=1, label=1, has_default_value=True, default_value=1000, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[], serialized_start=366, serialized_end=576)
_PRIMITIVEGROUP = _descriptor.Descriptor(name='PrimitiveGroup', full_name='OSMPBF.PrimitiveGroup', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='nodes', full_name='OSMPBF.PrimitiveGroup.nodes', index=0, number=1, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='dense', full_name='OSMPBF.PrimitiveGroup.dense', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='ways', full_name='OSMPBF.PrimitiveGroup.ways', index=2, number=3, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='relations', full_name='OSMPBF.PrimitiveGroup.relations', index=3, number=4, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='changesets', full_name='OSMPBF.PrimitiveGroup.changesets', index=4, number=5, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[], serialized_start=579, serialized_end=762)
_STRINGTABLE = _descriptor.Descriptor(name='StringTable', full_name='OSMPBF.StringTable', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='s', full_name='OSMPBF.StringTable.s', index=0, number=1, type=12, cpp_type=9, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[], serialized_start=764, serialized_end=788)
_INFO = _descriptor.Descriptor(name='Info', full_name='OSMPBF.Info', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='version', full_name='OSMPBF.Info.version', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=True, default_value=-1, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='timestamp', full_name='OSMPBF.Info.timestamp', index=1, number=2, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='changeset', full_name='OSMPBF.Info.changeset', index=2, number=3, type=3, cpp_type=2, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='uid', full_name='OSMPBF.Info.uid', index=3, number=4, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='user_sid', full_name='OSMPBF.Info.user_sid', index=4, number=5, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='visible', full_name='OSMPBF.Info.visible', index=5, number=6, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[], serialized_start=790, serialized_end=903)
_DENSEINFO = _descriptor.Descriptor(name='DenseInfo', full_name='OSMPBF.DenseInfo', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='version', full_name='OSMPBF.DenseInfo.version', index=0, number=1, type=5, cpp_type=1, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='timestamp', full_name='OSMPBF.DenseInfo.timestamp', index=1, number=2, type=18, cpp_type=2, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='changeset', full_name='OSMPBF.DenseInfo.changeset', index=2, number=3, type=18, cpp_type=2, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='uid', full_name='OSMPBF.DenseInfo.uid', index=3, number=4, type=17, cpp_type=1, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='user_sid', full_name='OSMPBF.DenseInfo.user_sid', index=4, number=5, type=17, cpp_type=1, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='visible', full_name='OSMPBF.DenseInfo.visible', index=5, number=6, type=8, cpp_type=7, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[], serialized_start=906, serialized_end=1044)
_CHANGESET = _descriptor.Descriptor(name='ChangeSet', full_name='OSMPBF.ChangeSet', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='id', full_name='OSMPBF.ChangeSet.id', index=0, number=1, type=3, cpp_type=2, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[], serialized_start=1046, serialized_end=1069)
_NODE = _descriptor.Descriptor(name='Node', full_name='OSMPBF.Node', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='id', full_name='OSMPBF.Node.id', index=0, number=1, type=18, cpp_type=2, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='keys', full_name='OSMPBF.Node.keys', index=1, number=2, type=13, cpp_type=3, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='vals', full_name='OSMPBF.Node.vals', index=2, number=3, type=13, cpp_type=3, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='info', full_name='OSMPBF.Node.info', index=3, number=4, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='lat', full_name='OSMPBF.Node.lat', index=4, number=8, type=18, cpp_type=2, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='lon', full_name='OSMPBF.Node.lon', index=5, number=9, type=18, cpp_type=2, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[], serialized_start=1071, serialized_end=1179)
_DENSENODES = _descriptor.Descriptor(name='DenseNodes', full_name='OSMPBF.DenseNodes', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='id', full_name='OSMPBF.DenseNodes.id', index=0, number=1, type=18, cpp_type=2, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='denseinfo', full_name='OSMPBF.DenseNodes.denseinfo', index=1, number=5, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='lat', full_name='OSMPBF.DenseNodes.lat', index=2, number=8, type=18, cpp_type=2, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='lon', full_name='OSMPBF.DenseNodes.lon', index=3, number=9, type=18, cpp_type=2, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='keys_vals', full_name='OSMPBF.DenseNodes.keys_vals', index=4, number=10, type=5, cpp_type=1, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[], serialized_start=1181, serialized_end=1304)
_WAY = _descriptor.Descriptor(name='Way', full_name='OSMPBF.Way', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='id', full_name='OSMPBF.Way.id', index=0, number=1, type=3, cpp_type=2, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='keys', full_name='OSMPBF.Way.keys', index=1, number=2, type=13, cpp_type=3, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='vals', full_name='OSMPBF.Way.vals', index=2, number=3, type=13, cpp_type=3, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='info', full_name='OSMPBF.Way.info', index=3, number=4, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='refs', full_name='OSMPBF.Way.refs', index=4, number=8, type=18, cpp_type=2, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[], serialized_start=1306, serialized_end=1405)
_RELATION = _descriptor.Descriptor(name='Relation', full_name='OSMPBF.Relation', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='id', full_name='OSMPBF.Relation.id', index=0, number=1, type=3, cpp_type=2, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='keys', full_name='OSMPBF.Relation.keys', index=1, number=2, type=13, cpp_type=3, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='vals', full_name='OSMPBF.Relation.vals', index=2, number=3, type=13, cpp_type=3, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='info', full_name='OSMPBF.Relation.info', index=3, number=4, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='roles_sid', full_name='OSMPBF.Relation.roles_sid', index=4, number=8, type=5, cpp_type=1, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='memids', full_name='OSMPBF.Relation.memids', index=5, number=9, type=18, cpp_type=2, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='types', full_name='OSMPBF.Relation.types', index=6, number=10, type=14, cpp_type=8, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01')), file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[
 _RELATION_MEMBERTYPE], options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[], serialized_start=1408, serialized_end=1632)
_HEADERBLOCK.fields_by_name['bbox'].message_type = _HEADERBBOX
_PRIMITIVEBLOCK.fields_by_name['stringtable'].message_type = _STRINGTABLE
_PRIMITIVEBLOCK.fields_by_name['primitivegroup'].message_type = _PRIMITIVEGROUP
_PRIMITIVEGROUP.fields_by_name['nodes'].message_type = _NODE
_PRIMITIVEGROUP.fields_by_name['dense'].message_type = _DENSENODES
_PRIMITIVEGROUP.fields_by_name['ways'].message_type = _WAY
_PRIMITIVEGROUP.fields_by_name['relations'].message_type = _RELATION
_PRIMITIVEGROUP.fields_by_name['changesets'].message_type = _CHANGESET
_NODE.fields_by_name['info'].message_type = _INFO
_DENSENODES.fields_by_name['denseinfo'].message_type = _DENSEINFO
_WAY.fields_by_name['info'].message_type = _INFO
_RELATION.fields_by_name['info'].message_type = _INFO
_RELATION.fields_by_name['types'].enum_type = _RELATION_MEMBERTYPE
_RELATION_MEMBERTYPE.containing_type = _RELATION
DESCRIPTOR.message_types_by_name['HeaderBlock'] = _HEADERBLOCK
DESCRIPTOR.message_types_by_name['HeaderBBox'] = _HEADERBBOX
DESCRIPTOR.message_types_by_name['PrimitiveBlock'] = _PRIMITIVEBLOCK
DESCRIPTOR.message_types_by_name['PrimitiveGroup'] = _PRIMITIVEGROUP
DESCRIPTOR.message_types_by_name['StringTable'] = _STRINGTABLE
DESCRIPTOR.message_types_by_name['Info'] = _INFO
DESCRIPTOR.message_types_by_name['DenseInfo'] = _DENSEINFO
DESCRIPTOR.message_types_by_name['ChangeSet'] = _CHANGESET
DESCRIPTOR.message_types_by_name['Node'] = _NODE
DESCRIPTOR.message_types_by_name['DenseNodes'] = _DENSENODES
DESCRIPTOR.message_types_by_name['Way'] = _WAY
DESCRIPTOR.message_types_by_name['Relation'] = _RELATION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
HeaderBlock = _reflection.GeneratedProtocolMessageType('HeaderBlock', (_message.Message,), dict(DESCRIPTOR=_HEADERBLOCK, __module__='osmformat_pb2'))
_sym_db.RegisterMessage(HeaderBlock)
HeaderBBox = _reflection.GeneratedProtocolMessageType('HeaderBBox', (_message.Message,), dict(DESCRIPTOR=_HEADERBBOX, __module__='osmformat_pb2'))
_sym_db.RegisterMessage(HeaderBBox)
PrimitiveBlock = _reflection.GeneratedProtocolMessageType('PrimitiveBlock', (_message.Message,), dict(DESCRIPTOR=_PRIMITIVEBLOCK, __module__='osmformat_pb2'))
_sym_db.RegisterMessage(PrimitiveBlock)
PrimitiveGroup = _reflection.GeneratedProtocolMessageType('PrimitiveGroup', (_message.Message,), dict(DESCRIPTOR=_PRIMITIVEGROUP, __module__='osmformat_pb2'))
_sym_db.RegisterMessage(PrimitiveGroup)
StringTable = _reflection.GeneratedProtocolMessageType('StringTable', (_message.Message,), dict(DESCRIPTOR=_STRINGTABLE, __module__='osmformat_pb2'))
_sym_db.RegisterMessage(StringTable)
Info = _reflection.GeneratedProtocolMessageType('Info', (_message.Message,), dict(DESCRIPTOR=_INFO, __module__='osmformat_pb2'))
_sym_db.RegisterMessage(Info)
DenseInfo = _reflection.GeneratedProtocolMessageType('DenseInfo', (_message.Message,), dict(DESCRIPTOR=_DENSEINFO, __module__='osmformat_pb2'))
_sym_db.RegisterMessage(DenseInfo)
ChangeSet = _reflection.GeneratedProtocolMessageType('ChangeSet', (_message.Message,), dict(DESCRIPTOR=_CHANGESET, __module__='osmformat_pb2'))
_sym_db.RegisterMessage(ChangeSet)
Node = _reflection.GeneratedProtocolMessageType('Node', (_message.Message,), dict(DESCRIPTOR=_NODE, __module__='osmformat_pb2'))
_sym_db.RegisterMessage(Node)
DenseNodes = _reflection.GeneratedProtocolMessageType('DenseNodes', (_message.Message,), dict(DESCRIPTOR=_DENSENODES, __module__='osmformat_pb2'))
_sym_db.RegisterMessage(DenseNodes)
Way = _reflection.GeneratedProtocolMessageType('Way', (_message.Message,), dict(DESCRIPTOR=_WAY, __module__='osmformat_pb2'))
_sym_db.RegisterMessage(Way)
Relation = _reflection.GeneratedProtocolMessageType('Relation', (_message.Message,), dict(DESCRIPTOR=_RELATION, __module__='osmformat_pb2'))
_sym_db.RegisterMessage(Relation)
DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\rcrosby.binaryH\x03'))
_DENSEINFO.fields_by_name['version'].has_options = True
_DENSEINFO.fields_by_name['version']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_DENSEINFO.fields_by_name['timestamp'].has_options = True
_DENSEINFO.fields_by_name['timestamp']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_DENSEINFO.fields_by_name['changeset'].has_options = True
_DENSEINFO.fields_by_name['changeset']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_DENSEINFO.fields_by_name['uid'].has_options = True
_DENSEINFO.fields_by_name['uid']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_DENSEINFO.fields_by_name['user_sid'].has_options = True
_DENSEINFO.fields_by_name['user_sid']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_DENSEINFO.fields_by_name['visible'].has_options = True
_DENSEINFO.fields_by_name['visible']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_NODE.fields_by_name['keys'].has_options = True
_NODE.fields_by_name['keys']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_NODE.fields_by_name['vals'].has_options = True
_NODE.fields_by_name['vals']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_DENSENODES.fields_by_name['id'].has_options = True
_DENSENODES.fields_by_name['id']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_DENSENODES.fields_by_name['lat'].has_options = True
_DENSENODES.fields_by_name['lat']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_DENSENODES.fields_by_name['lon'].has_options = True
_DENSENODES.fields_by_name['lon']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_DENSENODES.fields_by_name['keys_vals'].has_options = True
_DENSENODES.fields_by_name['keys_vals']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_WAY.fields_by_name['keys'].has_options = True
_WAY.fields_by_name['keys']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_WAY.fields_by_name['vals'].has_options = True
_WAY.fields_by_name['vals']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_WAY.fields_by_name['refs'].has_options = True
_WAY.fields_by_name['refs']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_RELATION.fields_by_name['keys'].has_options = True
_RELATION.fields_by_name['keys']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_RELATION.fields_by_name['vals'].has_options = True
_RELATION.fields_by_name['vals']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_RELATION.fields_by_name['roles_sid'].has_options = True
_RELATION.fields_by_name['roles_sid']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_RELATION.fields_by_name['memids'].has_options = True
_RELATION.fields_by_name['memids']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))
_RELATION.fields_by_name['types'].has_options = True
_RELATION.fields_by_name['types']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\x10\x01'))