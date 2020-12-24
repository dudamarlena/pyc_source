# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/protos/model_pb2.py
# Compiled at: 2020-04-05 21:16:38
# Size of source mod 2**32: 5855 bytes
import google.protobuf as _descriptor
import google.protobuf as _message
import google.protobuf as _reflection
import google.protobuf as _symbol_database
_sym_db = _symbol_database.Default()
import object_detection.protos as object__detection_dot_protos_dot_faster__rcnn__pb2
import object_detection.protos as object__detection_dot_protos_dot_ssd__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='object_detection/protos/model.proto',
  package='object_detection.protos',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=b'\n#object_detection/protos/model.proto\x12\x17object_detection.protos\x1a)object_detection/protos/faster_rcnn.proto\x1a!object_detection/protos/ssd.proto"\xcc\x01\n\x0eDetectionModel\x12:\n\x0bfaster_rcnn\x18\x01 \x01(\x0b2#.object_detection.protos.FasterRcnnH\x00\x12+\n\x03ssd\x18\x02 \x01(\x0b2\x1c.object_detection.protos.SsdH\x00\x12H\n\x12experimental_model\x18\x03 \x01(\x0b2*.object_detection.protos.ExperimentalModelH\x00B\x07\n\x05model"!\n\x11ExperimentalModel\x12\x0c\n\x04name\x18\x01 \x01(\t',
  dependencies=[
 object__detection_dot_protos_dot_faster__rcnn__pb2.DESCRIPTOR, object__detection_dot_protos_dot_ssd__pb2.DESCRIPTOR])
_DETECTIONMODEL = _descriptor.Descriptor(name='DetectionModel',
  full_name='object_detection.protos.DetectionModel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='faster_rcnn',
   full_name='object_detection.protos.DetectionModel.faster_rcnn',
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
 _descriptor.FieldDescriptor(name='ssd',
   full_name='object_detection.protos.DetectionModel.ssd',
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
 _descriptor.FieldDescriptor(name='experimental_model',
   full_name='object_detection.protos.DetectionModel.experimental_model',
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
  oneofs=[
 _descriptor.OneofDescriptor(name='model',
   full_name='object_detection.protos.DetectionModel.model',
   index=0,
   containing_type=None,
   fields=[])],
  serialized_start=143,
  serialized_end=347)
_EXPERIMENTALMODEL = _descriptor.Descriptor(name='ExperimentalModel',
  full_name='object_detection.protos.ExperimentalModel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='name',
   full_name='object_detection.protos.ExperimentalModel.name',
   index=0,
   number=1,
   type=9,
   cpp_type=9,
   label=1,
   has_default_value=False,
   default_value=((b'').decode('utf-8')),
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
  serialized_start=349,
  serialized_end=382)
_DETECTIONMODEL.fields_by_name['faster_rcnn'].message_type = object__detection_dot_protos_dot_faster__rcnn__pb2._FASTERRCNN
_DETECTIONMODEL.fields_by_name['ssd'].message_type = object__detection_dot_protos_dot_ssd__pb2._SSD
_DETECTIONMODEL.fields_by_name['experimental_model'].message_type = _EXPERIMENTALMODEL
_DETECTIONMODEL.oneofs_by_name['model'].fields.append(_DETECTIONMODEL.fields_by_name['faster_rcnn'])
_DETECTIONMODEL.fields_by_name['faster_rcnn'].containing_oneof = _DETECTIONMODEL.oneofs_by_name['model']
_DETECTIONMODEL.oneofs_by_name['model'].fields.append(_DETECTIONMODEL.fields_by_name['ssd'])
_DETECTIONMODEL.fields_by_name['ssd'].containing_oneof = _DETECTIONMODEL.oneofs_by_name['model']
_DETECTIONMODEL.oneofs_by_name['model'].fields.append(_DETECTIONMODEL.fields_by_name['experimental_model'])
_DETECTIONMODEL.fields_by_name['experimental_model'].containing_oneof = _DETECTIONMODEL.oneofs_by_name['model']
DESCRIPTOR.message_types_by_name['DetectionModel'] = _DETECTIONMODEL
DESCRIPTOR.message_types_by_name['ExperimentalModel'] = _EXPERIMENTALMODEL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
DetectionModel = _reflection.GeneratedProtocolMessageType('DetectionModel', (_message.Message,), {'DESCRIPTOR':_DETECTIONMODEL, 
 '__module__':'object_detection.protos.model_pb2'})
_sym_db.RegisterMessage(DetectionModel)
ExperimentalModel = _reflection.GeneratedProtocolMessageType('ExperimentalModel', (_message.Message,), {'DESCRIPTOR':_EXPERIMENTALMODEL, 
 '__module__':'object_detection.protos.model_pb2'})
_sym_db.RegisterMessage(ExperimentalModel)