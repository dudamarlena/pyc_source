# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/protos/mean_stddev_box_coder_pb2.py
# Compiled at: 2020-04-05 21:16:38
# Size of source mod 2**32: 2142 bytes
import google.protobuf as _descriptor
import google.protobuf as _message
import google.protobuf as _reflection
import google.protobuf as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='object_detection/protos/mean_stddev_box_coder.proto',
  package='object_detection.protos',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=b'\n3object_detection/protos/mean_stddev_box_coder.proto\x12\x17object_detection.protos"*\n\x12MeanStddevBoxCoder\x12\x14\n\x06stddev\x18\x01 \x01(\x02:\x040.01')
_MEANSTDDEVBOXCODER = _descriptor.Descriptor(name='MeanStddevBoxCoder',
  full_name='object_detection.protos.MeanStddevBoxCoder',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='stddev',
   full_name='object_detection.protos.MeanStddevBoxCoder.stddev',
   index=0,
   number=1,
   type=2,
   cpp_type=6,
   label=1,
   has_default_value=True,
   default_value=(float(0.01)),
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
  serialized_start=80,
  serialized_end=122)
DESCRIPTOR.message_types_by_name['MeanStddevBoxCoder'] = _MEANSTDDEVBOXCODER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
MeanStddevBoxCoder = _reflection.GeneratedProtocolMessageType('MeanStddevBoxCoder', (_message.Message,), {'DESCRIPTOR':_MEANSTDDEVBOXCODER, 
 '__module__':'object_detection.protos.mean_stddev_box_coder_pb2'})
_sym_db.RegisterMessage(MeanStddevBoxCoder)