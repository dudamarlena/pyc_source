# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/protos/pipeline_pb2.py
# Compiled at: 2020-04-05 20:34:16
# Size of source mod 2**32: 6593 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
import google.protobuf as _descriptor
import google.protobuf as _message
import google.protobuf as _reflection
import google.protobuf as _symbol_database
_sym_db = _symbol_database.Default()
import object_detection.protos as object__detection_dot_protos_dot_eval__pb2
import object_detection.protos as object__detection_dot_protos_dot_graph__rewriter__pb2
import object_detection.protos as object__detection_dot_protos_dot_input__reader__pb2
import object_detection.protos as object__detection_dot_protos_dot_model__pb2
import object_detection.protos as object__detection_dot_protos_dot_train__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='object_detection/protos/pipeline.proto',
  package='object_detection.protos',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=(_b('\n&object_detection/protos/pipeline.proto\x12\x17object_detection.protos\x1a"object_detection/protos/eval.proto\x1a,object_detection/protos/graph_rewriter.proto\x1a*object_detection/protos/input_reader.proto\x1a#object_detection/protos/model.proto\x1a#object_detection/protos/train.proto"\x95\x03\n\x17TrainEvalPipelineConfig\x126\n\x05model\x18\x01 \x01(\x0b2\'.object_detection.protos.DetectionModel\x12:\n\x0ctrain_config\x18\x02 \x01(\x0b2$.object_detection.protos.TrainConfig\x12@\n\x12train_input_reader\x18\x03 \x01(\x0b2$.object_detection.protos.InputReader\x128\n\x0beval_config\x18\x04 \x01(\x0b2#.object_detection.protos.EvalConfig\x12?\n\x11eval_input_reader\x18\x05 \x03(\x0b2$.object_detection.protos.InputReader\x12>\n\x0egraph_rewriter\x18\x06 \x01(\x0b2&.object_detection.protos.GraphRewriter*\t\x08è\x07\x10\x80\x80\x80\x80\x02')),
  dependencies=[
 object__detection_dot_protos_dot_eval__pb2.DESCRIPTOR, object__detection_dot_protos_dot_graph__rewriter__pb2.DESCRIPTOR, object__detection_dot_protos_dot_input__reader__pb2.DESCRIPTOR, object__detection_dot_protos_dot_model__pb2.DESCRIPTOR, object__detection_dot_protos_dot_train__pb2.DESCRIPTOR])
_TRAINEVALPIPELINECONFIG = _descriptor.Descriptor(name='TrainEvalPipelineConfig',
  full_name='object_detection.protos.TrainEvalPipelineConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='model',
   full_name='object_detection.protos.TrainEvalPipelineConfig.model',
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
 _descriptor.FieldDescriptor(name='train_config',
   full_name='object_detection.protos.TrainEvalPipelineConfig.train_config',
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
 _descriptor.FieldDescriptor(name='train_input_reader',
   full_name='object_detection.protos.TrainEvalPipelineConfig.train_input_reader',
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
 _descriptor.FieldDescriptor(name='eval_config',
   full_name='object_detection.protos.TrainEvalPipelineConfig.eval_config',
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
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='eval_input_reader',
   full_name='object_detection.protos.TrainEvalPipelineConfig.eval_input_reader',
   index=4,
   number=5,
   type=11,
   cpp_type=10,
   label=3,
   has_default_value=False,
   default_value=[],
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='graph_rewriter',
   full_name='object_detection.protos.TrainEvalPipelineConfig.graph_rewriter',
   index=5,
   number=6,
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
  is_extendable=True,
  syntax='proto2',
  extension_ranges=[
 (1000, 536870912)],
  oneofs=[],
  serialized_start=268,
  serialized_end=673)
_TRAINEVALPIPELINECONFIG.fields_by_name['model'].message_type = object__detection_dot_protos_dot_model__pb2._DETECTIONMODEL
_TRAINEVALPIPELINECONFIG.fields_by_name['train_config'].message_type = object__detection_dot_protos_dot_train__pb2._TRAINCONFIG
_TRAINEVALPIPELINECONFIG.fields_by_name['train_input_reader'].message_type = object__detection_dot_protos_dot_input__reader__pb2._INPUTREADER
_TRAINEVALPIPELINECONFIG.fields_by_name['eval_config'].message_type = object__detection_dot_protos_dot_eval__pb2._EVALCONFIG
_TRAINEVALPIPELINECONFIG.fields_by_name['eval_input_reader'].message_type = object__detection_dot_protos_dot_input__reader__pb2._INPUTREADER
_TRAINEVALPIPELINECONFIG.fields_by_name['graph_rewriter'].message_type = object__detection_dot_protos_dot_graph__rewriter__pb2._GRAPHREWRITER
DESCRIPTOR.message_types_by_name['TrainEvalPipelineConfig'] = _TRAINEVALPIPELINECONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
TrainEvalPipelineConfig = _reflection.GeneratedProtocolMessageType('TrainEvalPipelineConfig', (_message.Message,), dict(DESCRIPTOR=_TRAINEVALPIPELINECONFIG,
  __module__='object_detection.protos.pipeline_pb2'))
_sym_db.RegisterMessage(TrainEvalPipelineConfig)