# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/protos/matcher_pb2.py
# Compiled at: 2020-04-05 21:16:38
# Size of source mod 2**32: 3868 bytes
import google.protobuf as _descriptor
import google.protobuf as _message
import google.protobuf as _reflection
import google.protobuf as _symbol_database
_sym_db = _symbol_database.Default()
import object_detection.protos as object__detection_dot_protos_dot_argmax__matcher__pb2
import object_detection.protos as object__detection_dot_protos_dot_bipartite__matcher__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='object_detection/protos/matcher.proto',
  package='object_detection.protos',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=b'\n%object_detection/protos/matcher.proto\x12\x17object_detection.protos\x1a,object_detection/protos/argmax_matcher.proto\x1a/object_detection/protos/bipartite_matcher.proto"\xa4\x01\n\x07Matcher\x12@\n\x0eargmax_matcher\x18\x01 \x01(\x0b2&.object_detection.protos.ArgMaxMatcherH\x00\x12F\n\x11bipartite_matcher\x18\x02 \x01(\x0b2).object_detection.protos.BipartiteMatcherH\x00B\x0f\n\rmatcher_oneof',
  dependencies=[
 object__detection_dot_protos_dot_argmax__matcher__pb2.DESCRIPTOR, object__detection_dot_protos_dot_bipartite__matcher__pb2.DESCRIPTOR])
_MATCHER = _descriptor.Descriptor(name='Matcher',
  full_name='object_detection.protos.Matcher',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='argmax_matcher',
   full_name='object_detection.protos.Matcher.argmax_matcher',
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
 _descriptor.FieldDescriptor(name='bipartite_matcher',
   full_name='object_detection.protos.Matcher.bipartite_matcher',
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
 _descriptor.OneofDescriptor(name='matcher_oneof',
   full_name='object_detection.protos.Matcher.matcher_oneof',
   index=0,
   containing_type=None,
   fields=[])],
  serialized_start=162,
  serialized_end=326)
_MATCHER.fields_by_name['argmax_matcher'].message_type = object__detection_dot_protos_dot_argmax__matcher__pb2._ARGMAXMATCHER
_MATCHER.fields_by_name['bipartite_matcher'].message_type = object__detection_dot_protos_dot_bipartite__matcher__pb2._BIPARTITEMATCHER
_MATCHER.oneofs_by_name['matcher_oneof'].fields.append(_MATCHER.fields_by_name['argmax_matcher'])
_MATCHER.fields_by_name['argmax_matcher'].containing_oneof = _MATCHER.oneofs_by_name['matcher_oneof']
_MATCHER.oneofs_by_name['matcher_oneof'].fields.append(_MATCHER.fields_by_name['bipartite_matcher'])
_MATCHER.fields_by_name['bipartite_matcher'].containing_oneof = _MATCHER.oneofs_by_name['matcher_oneof']
DESCRIPTOR.message_types_by_name['Matcher'] = _MATCHER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
Matcher = _reflection.GeneratedProtocolMessageType('Matcher', (_message.Message,), {'DESCRIPTOR':_MATCHER, 
 '__module__':'object_detection.protos.matcher_pb2'})
_sym_db.RegisterMessage(Matcher)