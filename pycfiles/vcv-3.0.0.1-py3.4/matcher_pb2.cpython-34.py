# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/protos/matcher_pb2.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 3916 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
_sym_db = _symbol_database.Default()
from object_detection.protos import argmax_matcher_pb2 as object__detection_dot_protos_dot_argmax__matcher__pb2
from object_detection.protos import bipartite_matcher_pb2 as object__detection_dot_protos_dot_bipartite__matcher__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='object_detection/protos/matcher.proto', package='object_detection.protos', syntax='proto2', serialized_pb=_b('\n%object_detection/protos/matcher.proto\x12\x17object_detection.protos\x1a,object_detection/protos/argmax_matcher.proto\x1a/object_detection/protos/bipartite_matcher.proto"¤\x01\n\x07Matcher\x12@\n\x0eargmax_matcher\x18\x01 \x01(\x0b2&.object_detection.protos.ArgMaxMatcherH\x00\x12F\n\x11bipartite_matcher\x18\x02 \x01(\x0b2).object_detection.protos.BipartiteMatcherH\x00B\x0f\n\rmatcher_oneof'), dependencies=[
 object__detection_dot_protos_dot_argmax__matcher__pb2.DESCRIPTOR, object__detection_dot_protos_dot_bipartite__matcher__pb2.DESCRIPTOR])
_MATCHER = _descriptor.Descriptor(name='Matcher', full_name='object_detection.protos.Matcher', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='argmax_matcher', full_name='object_detection.protos.Matcher.argmax_matcher', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='bipartite_matcher', full_name='object_detection.protos.Matcher.bipartite_matcher', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='matcher_oneof', full_name='object_detection.protos.Matcher.matcher_oneof', index=0, containing_type=None, fields=[])], serialized_start=162, serialized_end=326)
_MATCHER.fields_by_name['argmax_matcher'].message_type = object__detection_dot_protos_dot_argmax__matcher__pb2._ARGMAXMATCHER
_MATCHER.fields_by_name['bipartite_matcher'].message_type = object__detection_dot_protos_dot_bipartite__matcher__pb2._BIPARTITEMATCHER
_MATCHER.oneofs_by_name['matcher_oneof'].fields.append(_MATCHER.fields_by_name['argmax_matcher'])
_MATCHER.fields_by_name['argmax_matcher'].containing_oneof = _MATCHER.oneofs_by_name['matcher_oneof']
_MATCHER.oneofs_by_name['matcher_oneof'].fields.append(_MATCHER.fields_by_name['bipartite_matcher'])
_MATCHER.fields_by_name['bipartite_matcher'].containing_oneof = _MATCHER.oneofs_by_name['matcher_oneof']
DESCRIPTOR.message_types_by_name['Matcher'] = _MATCHER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
Matcher = _reflection.GeneratedProtocolMessageType('Matcher', (_message.Message,), dict(DESCRIPTOR=_MATCHER, __module__='object_detection.protos.matcher_pb2'))
_sym_db.RegisterMessage(Matcher)