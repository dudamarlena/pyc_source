# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/protos/anchor_generator_pb2.py
# Compiled at: 2020-04-05 21:16:38
# Size of source mod 2**32: 6890 bytes
import google.protobuf as _descriptor
import google.protobuf as _message
import google.protobuf as _reflection
import google.protobuf as _symbol_database
_sym_db = _symbol_database.Default()
import object_detection.protos as object__detection_dot_protos_dot_flexible__grid__anchor__generator__pb2
import object_detection.protos as object__detection_dot_protos_dot_grid__anchor__generator__pb2
import object_detection.protos as object__detection_dot_protos_dot_multiscale__anchor__generator__pb2
import object_detection.protos as object__detection_dot_protos_dot_ssd__anchor__generator__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='object_detection/protos/anchor_generator.proto',
  package='object_detection.protos',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=b'\n.object_detection/protos/anchor_generator.proto\x12\x17object_detection.protos\x1a<object_detection/protos/flexible_grid_anchor_generator.proto\x1a3object_detection/protos/grid_anchor_generator.proto\x1a9object_detection/protos/multiscale_anchor_generator.proto\x1a2object_detection/protos/ssd_anchor_generator.proto"\x82\x03\n\x0fAnchorGenerator\x12M\n\x15grid_anchor_generator\x18\x01 \x01(\x0b2,.object_detection.protos.GridAnchorGeneratorH\x00\x12K\n\x14ssd_anchor_generator\x18\x02 \x01(\x0b2+.object_detection.protos.SsdAnchorGeneratorH\x00\x12Y\n\x1bmultiscale_anchor_generator\x18\x03 \x01(\x0b22.object_detection.protos.MultiscaleAnchorGeneratorH\x00\x12^\n\x1eflexible_grid_anchor_generator\x18\x04 \x01(\x0b24.object_detection.protos.FlexibleGridAnchorGeneratorH\x00B\x18\n\x16anchor_generator_oneof',
  dependencies=[
 object__detection_dot_protos_dot_flexible__grid__anchor__generator__pb2.DESCRIPTOR, object__detection_dot_protos_dot_grid__anchor__generator__pb2.DESCRIPTOR, object__detection_dot_protos_dot_multiscale__anchor__generator__pb2.DESCRIPTOR, object__detection_dot_protos_dot_ssd__anchor__generator__pb2.DESCRIPTOR])
_ANCHORGENERATOR = _descriptor.Descriptor(name='AnchorGenerator',
  full_name='object_detection.protos.AnchorGenerator',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='grid_anchor_generator',
   full_name='object_detection.protos.AnchorGenerator.grid_anchor_generator',
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
 _descriptor.FieldDescriptor(name='ssd_anchor_generator',
   full_name='object_detection.protos.AnchorGenerator.ssd_anchor_generator',
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
 _descriptor.FieldDescriptor(name='multiscale_anchor_generator',
   full_name='object_detection.protos.AnchorGenerator.multiscale_anchor_generator',
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
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='flexible_grid_anchor_generator',
   full_name='object_detection.protos.AnchorGenerator.flexible_grid_anchor_generator',
   index=3,
   number=4,
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
 _descriptor.OneofDescriptor(name='anchor_generator_oneof',
   full_name='object_detection.protos.AnchorGenerator.anchor_generator_oneof',
   index=0,
   containing_type=None,
   fields=[])],
  serialized_start=302,
  serialized_end=688)
_ANCHORGENERATOR.fields_by_name['grid_anchor_generator'].message_type = object__detection_dot_protos_dot_grid__anchor__generator__pb2._GRIDANCHORGENERATOR
_ANCHORGENERATOR.fields_by_name['ssd_anchor_generator'].message_type = object__detection_dot_protos_dot_ssd__anchor__generator__pb2._SSDANCHORGENERATOR
_ANCHORGENERATOR.fields_by_name['multiscale_anchor_generator'].message_type = object__detection_dot_protos_dot_multiscale__anchor__generator__pb2._MULTISCALEANCHORGENERATOR
_ANCHORGENERATOR.fields_by_name['flexible_grid_anchor_generator'].message_type = object__detection_dot_protos_dot_flexible__grid__anchor__generator__pb2._FLEXIBLEGRIDANCHORGENERATOR
_ANCHORGENERATOR.oneofs_by_name['anchor_generator_oneof'].fields.append(_ANCHORGENERATOR.fields_by_name['grid_anchor_generator'])
_ANCHORGENERATOR.fields_by_name['grid_anchor_generator'].containing_oneof = _ANCHORGENERATOR.oneofs_by_name['anchor_generator_oneof']
_ANCHORGENERATOR.oneofs_by_name['anchor_generator_oneof'].fields.append(_ANCHORGENERATOR.fields_by_name['ssd_anchor_generator'])
_ANCHORGENERATOR.fields_by_name['ssd_anchor_generator'].containing_oneof = _ANCHORGENERATOR.oneofs_by_name['anchor_generator_oneof']
_ANCHORGENERATOR.oneofs_by_name['anchor_generator_oneof'].fields.append(_ANCHORGENERATOR.fields_by_name['multiscale_anchor_generator'])
_ANCHORGENERATOR.fields_by_name['multiscale_anchor_generator'].containing_oneof = _ANCHORGENERATOR.oneofs_by_name['anchor_generator_oneof']
_ANCHORGENERATOR.oneofs_by_name['anchor_generator_oneof'].fields.append(_ANCHORGENERATOR.fields_by_name['flexible_grid_anchor_generator'])
_ANCHORGENERATOR.fields_by_name['flexible_grid_anchor_generator'].containing_oneof = _ANCHORGENERATOR.oneofs_by_name['anchor_generator_oneof']
DESCRIPTOR.message_types_by_name['AnchorGenerator'] = _ANCHORGENERATOR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
AnchorGenerator = _reflection.GeneratedProtocolMessageType('AnchorGenerator', (_message.Message,), {'DESCRIPTOR':_ANCHORGENERATOR, 
 '__module__':'object_detection.protos.anchor_generator_pb2'})
_sym_db.RegisterMessage(AnchorGenerator)